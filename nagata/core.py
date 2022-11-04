"""
core: base classes for file management
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2022, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Contents:
    FileFormat (object): base class for defining rules and methods for different
        file formats.
    FileFramework (object): Stores default settings, all file formats, and any
        other shared information used by FileManager.
    FileManager (object): interface for nagata file management. It provides a
        one-stop place for loading and saving all files of supported file types 
        in an organizational structure specified by the user.
    
ToDo:

    
"""
from __future__ import annotations
import abc
from collections.abc import Hashable, Mapping, MutableMapping, Sequence
import contextlib
import dataclasses
import pathlib
import types
from typing import Any, ClassVar, Optional, Type

import amos
import miller

from . import transfer
from . import lazy


@dataclasses.dataclass
class FileFormat(object):
    """File format information, loader, and saver.

    Args:
        name (str): the format name which should match the key when a FileFormat 
            instance is stored. 'name' is required so that the automatic 
            registration of all FileFormat instances works properly.
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first 
            one is used for saving new files and all will be used for loading. 
            Defaults to None.
        loader (str | types.FunctionType): if a str, it is the name of the 
            loading method in 'module' to use, name of attribute of the loading
            method on the FileFormat instance, or the name of a method in the
            'transfer' module of nagata. Otherwise, it should be a function for 
            loading.
        saver (str | types.FunctionType): if a str, it is the name of the 
            saving method in 'module' to use, name of attribute of the saving
            method on the FileFormat instance, or the name of a method in the
            'transfer' module of nagata. Otherwise, it should be a function for 
            saving.
        module (Optional[str]): name of module where the relevant loader and 
            saver are located. If 'module' is None, nagata will first look to
            see if 'loader' or 'saver' is attached to the FileFormat instance
            and then check for a function in the 'transfer' module. Defaults to
            None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool 
            of settings in FileFramework.settings where the key is the parameter 
            name that the load or save method should use and the value is the 
            key for the argument in the shared parameters. Defaults to an empty 
            dict. 
        
    """
    name: str
    extensions: str | Sequence[str]
    saver: str | types.FunctionType
    loader: Optional[str | types.FunctionType] = None
    module: Optional[str] = None
    parameters: Optional[Mapping[str, str]] = dataclasses.field(
        default_factory = dict)
    
    """ Initialization Methods """
            
    def __post_init__(self) -> None:
        """Automatically registers subclass."""
        with contextlib.suppress(AttributeError):
            super().__post_init__(*args, **kwargs) # type: ignore
        key = amos.namify(item = self)
        FileFramework.formats[key] = self

    """ Public Methods """
    
    def load(self, path: pathlib.Path | str, **kwargs) -> Any:
        """Loads a file of the included file format.

        Args:
            path (pathlib.Path | str): path of file to load from disk.

        Returns:
            Any: content of loaded file.
            
        """             
        method = self._validate_io_method(attribute = 'loader')
        return method(path, **kwargs)
    
    def save(self, item: Any, path: pathlib.Path | str, **kwargs) -> None:
        """Saves a file of the included file format.

        Args:
            item (Any): item to save to disk.
            path (pathlib.Path | str): path where the file should be saved.
            
        """        
        method = self._validate_io_method(attribute = 'saver')
        method(item, path, **kwargs)
        return self
    
    """ Private Methods """
    
    def _validate_io_method(self, attribute: str) -> types.FunctionType:
        """[summary]

        Args:
            attribute (str): [description]

        Raises:
            AttributeError: [description]
            ValueError: [description]

        Returns:
            types.FunctionType: [description]
            
        """        
        value = getattr(self, attribute)
        if isinstance(value, str):
            if self.module is None:
                try:
                    method = getattr(self, value)
                except AttributeError:
                    try:
                        method = getattr(transfer, value)
                    except AttributeError:
                        raise AttributeError(f'{value} could not be found')
            else:
                method = lazy.from_import_path(
                    path = value, 
                    package = self.module)
            setattr(self, attribute, method)
        if not isinstance(value, types.FunctionType):
            raise ValueError(
                f'{attribute} must be a str, function, or method')
        return method
        
        
@dataclasses.dataclass
class FileFramework(abc.ABC):
    """Default values and classes for file management
    
    Every attribute in FilingFramework should be a class attribute so that it
    is accessible without instancing it (which it cannot be).

    Args:
        settings (ClassVar[dict[Hashable, Any]]): default settings for 
            file management.      
        
    """
    settings: ClassVar[dict[Hashable, Any]] = {
        'file_encoding': 'windows-1252',
        'index_column': True,
        'include_header': True,
        'conserve_memory': False,
        'test_size': 1000,
        'threads': -1,
        'visual_tightness': 'tight', 
        'visual_format': 'png'}
    formats: amos.Dictionary[str, FileFormat] = amos.Dictionary()
  
   
@dataclasses.dataclass
class FileManager(object):
    """File and folder management for nagata.

    Creates and stores dynamic and static file paths, properly formats files
    for import and export, and provides methods for loading and saving
    nagata, pandas, and numpy objects.

    Args:
        root_folder (pathlib.Path | str): the complete path from which the 
            other paths and folders used by FileManager are ordinarily derived 
            (unless you decide to use full paths for all other options). 
            Defaults to None. If not passed, the parent folder of the current 
            working workery is used.
        input_folder (pathlib.Path | str]): the input_folder subfolder 
            name or a complete path if the 'input_folder' is not off of
            'root_folder'. Defaults to 'input'.
        output_folder (pathlib.Path | str]): the output_folder subfolder
            name or a complete path if the 'output_folder' is not off of
            'root_folder'. Defaults to 'output'.
        framework (Type[FileFramework]): class with default settings, dict of
            supported file formats, and any other information needed for file
            management. Defaults to FileFramework.

    """
    root_folder: pathlib.Path | str = pathlib.Path('.')
    input_folder: pathlib.Path | str = 'root'
    interim_folder: pathlib.Path | str = 'root'
    output_folder: pathlib.Path | str = 'root'
    framework: Type[FileFramework] = FileFramework
    
    """ Initialization Methods """

    def __post_init__(self) -> None:
        """Initializes and validates an instance."""
        # Calls parent and/or mixin initialization method(s).
        with contextlib.suppress(AttributeError):
            super().__post_init__()
        # Validates core folder paths and writes them to disk.
        self._validate_root_folder()
        self._validate_io_folders()
        return 
    
    """ Properties """
    
    @property
    def extensions(self) -> dict[str, str]: 
        """Returns dict of file extensions.
        
        Raises:
            TypeError: when a non-string or non-sequence is discovered in a
                stored FileFormat's 'extensions' attribute.
        Returns:
            dict[str, str]: keys are file extensions and values are the related
                key to the file_format in the 'formats' attribute.
        
        """
        extensions = {}
        for key, instance in self.framework.formats.items():
            if isinstance(instance.extensions, str):
                extensions[instance.extensions] = key
            elif isinstance(instance.extensions, Sequence):
                extensions.update(dict.fromkeys(instance.extensions, key))
            else:
                raise TypeError(
                    f'{instance.extensions} are not valid extension types')
        return extensions
                       
    """ Public Methods """

    def load(
        self,
        file_path: Optional[pathlib.Path | str] = None,
        folder: pathlib.Path | str = None,
        file_name: Optional[str] = None,
        file_format: Optional[str | FileFormat] = None,
        **kwargs: Any) -> Any:
        """Imports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        file_path is passed, folder and file_name are ignored.

        Args:
            file_path (Union[str, Path]]): a complete file path. Defaults to 
                None.
            folder (Union[str, Path]]): a complete folder path or the name of a 
                folder. Defaults to None.
            file_name (str): file name without extension. Defaults to None.
            file_format (Union[str, FileFormat]]): object with information about 
                how the file should be loaded or the key to such an object. 
                Defaults to None.
            **kwargs: can be passed if additional options are desired specific
                to the methods attached to a FileFormat instance.

        Returns:
            Any: depending upon method used for appropriate file format, a new
                variable of a supported type is returned.

        """
        file_path, file_format = self._prepare_transfer(
            file_path = file_path,
            folder = folder,
            file_name = file_name,
            transfer_type = 'load',
            file_format = file_format)
        parameters = self._get_transfer_parameters(
            file_format = file_format, 
            **kwargs)
        return file_format.loader(path = file_path, **parameters)

    def save(
        self,
        item: Any,
        file_path: Optional[pathlib.Path | str] = None,
        folder: Optional[pathlib.Path | str] = None,
        file_name: Optional[str] = None,
        file_format: Optional[str | FileFormat] = None,
        **kwargs: Any) -> None:
        """Exports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        file_path is passed, folder and file_name are ignored.

        Args:
            item (Any): object to be save to disk.
            file_path (Union[str, Path]]): a complete file path. Defaults to 
                None.
            folder (Union[str, Path]]): a complete folder path or the name of a 
                folder. Defaults to None.
            file_name (str): file name without extension. Defaults to None.
            file_format (Union[str, FileFormat]]): object with information about 
                how the file should be loaded or the key to such an object. 
                Defaults to None.
            **kwargs: can be passed if additional options are desired specific
                to the methods attached to a FileFormat instance.

        """
        file_path, file_format = self._prepare_transfer(
            file_path = file_path,
            folder = folder,
            file_name = file_name,
            transfer_type = 'save',
            file_format = file_format)
        parameters = self._get_transfer_parameters(
            file_format = file_format, 
            **kwargs)
        file_format.saver(item = item, path = file_path, **parameters)
        return

    def validate(self, path: pathlib.Path | str) -> pathlib.Path:
        """Turns 'file_path' into a pathlib.Path.

        Args:
            path (pathlib.Path | str): str or Path to be validated. If
                a str is passed, the method will see if an attribute matching
                'path' exists and if that attribute contains a Path.

        Raises:
            TypeError: if 'path' is neither a str nor Path.
            FileNotFoundError: if the validated path does not exist and 'create'
                is False.

        Returns:
            pathlib.Path: derived from 'path'.

        """
        if isinstance(path, str):
            attribute = f'{path}_folder'
            try:
                value = getattr(self, attribute)
                if isinstance(value, pathlib.Path):
                    return value
            except AttributeError:
                pass
            else:
                return pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            return path
        else:
            raise TypeError(f'path must be a str or Path type')
        return
      
    """ Private Methods """

    def _combine_path(
        self,
        folder: str,
        file_name: Optional[str] = None,
        extension: Optional[str] = None) -> pathlib.Path:
        """Converts strings to pathlib Path object.

        If 'folder' matches an attribute, the value stored in that attribute
        is substituted for 'folder'.

        If 'name' and 'extension' are passed, a file path is created. Otherwise,
        a folder path is created.

        Args:
            folder (str): folder for file location.
            name (str): the name of the file.
            extension (str): the extension of the file.

        Returns:
            Path: formed from string arguments.

        """
        if hasattr(self, f'{folder}_folder'):
            folder = getattr(self, f'{folder}_folder')
        if file_name and extension and '.' not in file_name:
            return pathlib.Path(folder).joinpath(f'{file_name}.{extension}')
        elif file_name and '.' in file_name:
            return pathlib.Path(folder).joinpath(file_name)
        else:
            return pathlib.Path(folder)

    def _get_transfer_parameters(
        self,
        file_format: FileFormat, 
        **kwargs: Any) -> MutableMapping[Hashable, Any]:
        """Creates complete parameters for a file input/output method.

        Args:
            file_format (FileFormat): an instance with information about the
                needed and optional parameters.
            kwargs: additional parameters to pass to an input/output method.

        Returns:
            MutableMapping[Hashable, Any]: parameters to be passed to an 
                input/output method.

        """
        if file_format.parameters:
            for specific, common in file_format.parameters.items():
                if specific not in kwargs:
                    kwargs[specific] = self.framework.settings[common]
        return kwargs # type: ignore

    def _prepare_transfer( 
        self,
        file_path: pathlib.Path | str,
        folder: pathlib.Path | str,
        file_name: str,
        transfer_type: str,
        file_format: Optional[str | FileFormat] = None) -> (
            tuple[pathlib.Path, FileFormat]):
        """Prepares file path related arguments for loading or saving a file.

        Args:
            file_path (Union[str, Path]]): a complete file path. Defaults to 
                None.
            folder (Union[str, Path]]): a complete folder path or the name of a 
                folder. Defaults to None.
            file_name (str): file name without extension. Defaults to None.
            file_format (Union[str, FileFormat]]): object with information about 
                how the file should be loaded or the key to such an object. 
                Defaults to None.

        Returns:
            tuple: of a completed Path instance and FileFormat instance.

        """
        extension = None
        if file_path:
            file_path = self.validate(path = file_path)
            extension = file_path.suffix[1:] 
        elif file_name and '.' in file_name:
            extension = amos.cleave_str(file_name, divider = '.')[-1]
        if extension and not file_format:
            file_format = self.extensions[extension]    
        file_format = self._validate_file_format(file_format = file_format)
        extension = extension or self._get_extension(file_format = file_format)
        if not folder:
            if transfer_type == 'save':
                folder = self.output_folder
            elif transfer_type == 'load':
                folder = self.input_folder
            else:
                raise ValueError(
                    'either folder or transfer type must be passed')
        if not file_path:
            file_path = self._combine_path(
                folder = folder, 
                file_name = file_name,
                extension = extension)
        return file_path, file_format

    def _get_extension(self, file_format: str | FileFormat) -> str:
        """Returns a str file extension.

        Args:
            file_format (str | FileFormat): name of file format or a FileFormat 
                instance.

        Raises:
            KeyError: if 'file_format' is a str but does not match any known
                file format in 'framework.formats'.

        Returns:
            str: file extension to use.

        """
        if isinstance(file_format, str):
            try:
                file_format = self.framework.formats[file_format]
            except KeyError:
                raise KeyError(f'{file_format} is not a recognized file format')
        if isinstance(file_format.extensions, str):
            return file_format.extensions
        else:
            return file_format.extensions[0]
        
    def _validate_file_format(
        self,
        file_format: str | FileFormat) -> FileFormat:
        """Selects 'file_format' or returns FileFormat instance intact.

        Args:
            file_format (Union[str, FileFormat]): name of file format or a
                FileFormat instance.

        Raises:
            KeyError: if 'file_format' is a str but does not match any known
                file format in 'framework.formats'.
            TypeError: if 'file_format' is neither a str nor FileFormat type.

        Returns:
            FileFormat: appropriate instance.

        """
        if isinstance(file_format, str):
            try:
                return self.framework.formats[file_format]
            except KeyError:
                raise KeyError(f'{file_format} is not a recognized file format')
        elif isinstance(file_format, FileFormat):
            return file_format
        else:
            raise TypeError(f'{file_format} is not a FileFormat type')
        
    def _validate_io_folder(self, path: str | pathlib.Path) -> pathlib.Path:
        """Validates an import and export path.'
        
        Args:
            path (str | pathlib.Path): path to validate.
            
        Returns:
            pathlib.Path: path in a pathlib.Path format.
            
        """
        if isinstance(path, str):
            attribute = f'{path}_folder'
            try:
                path = getattr(self, attribute)
            except AttributeError:
                pass
        if isinstance(path, str): 
            path = self.root_folder.joinpath(path) 
        return path      
    
    def _validate_io_folders(self) -> None:
        """Validates all import and export paths."""
        all_attributes = miller.name_variables(item = self)
        io_attributes = [a for a in all_attributes if a.endswith('_folder')]
        for attribute in io_attributes:
            value = getattr(self, attribute)
            path = self._validate_io_folder(path = value)
            setattr(self, attribute, path)
            self._write_folder(folder = path)
        return
            
    def _validate_root_folder(self) -> None:
        """Validates the root folder path."""
        self.root_folder = self.validate(path = self.root_folder)
        self._write_folder(folder = self.root_folder)
        return

    def _write_folder(self, folder: pathlib.Path | str) -> None:
        """Writes folder to disk.

        Parent folders are created as needed.

        Args:
            folder (Union[str, Path]): intended folder to write to disk.

        """
        pathlib.Path.mkdir(folder, parents = True, exist_ok = True)
        return


def add_loader(loader: types.Functiontype) -> None:
    """Adds a loading function to nagata.

    Args:
        loader (types.Functiontype): method that loads from a file.
        
    """
    setattr(transfer, loader.__name__, loader)
    return

def add_saver(saver: types.Functiontype) -> None:
    """Adds a saving function to nagata.

    Args:
        saver (types.Functiontype): method that saves a file.
        
    """
    setattr(transfer, saver.__name__, saver)
    return
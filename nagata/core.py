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
    FileFormat
    FileFramework
    FileManager (object): interface for nagata file management classes and 
        methods.
    
ToDo:

    
"""
from __future__ import annotations
import abc
from collections.abc import Hashable, MutableMapping, MutableSequence, Sequence
import contextlib
import dataclasses
import inspect
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
        name (Optional[str]): the format name which should match the key when a 
            FileFormat instance is stored.
        module (Optional[str]): name of module where the relevant loader and 
            saver are located, which can either be a nagata or non-nagata 
            module. Defaults to None.
        extensions (Optional[Union[str, MutableSequence[str]]]): str file 
            extension(s) to use. If more than one is listed, the first one is 
            used for saving new files and all will be used for loading. Defaults 
            to None.
        loader (Optional[Union[str, types.FunctionType]]): if a str, it is
            the name of import method in 'module' to use. Otherwise, it should
            be a function for loading. Defaults to None.
        saver (Optional[Union[str, types.FunctionType]]): if a str, it is
            the name of import method in 'module' to use. Otherwise, it should
            be a function for saved. Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from 
            configuration settings where the key is the parameter name that the 
            load or save method should use and the value is the key for the 
            argument in the shared parameters. Defaults to an empty dict. 
        instances (ClassVar[amos.Catalog]): project catalog of instances.
        
    """
    name: Optional[str] = None
    module: Optional[str] = None
    extensions: Optional[str | MutableSequence[str]] = None
    loader: Optional[str | types.FunctionType] = None
    saver: Optional[str | types.FunctionType] = None
    parameters: MutableMapping[str, str] = dataclasses.field(
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
        """[summary]

        Args:
            path (pathlib.Path | str): [description]

        Returns:
            Any: [description]
            
        """             
        method = self._validate_io_method(attribute = 'loader')
        return method(path, **kwargs)
    
    def save(self, item: Any, path: pathlib.Path | str, **kwargs) -> None:
        """[summary]

        Args:
            item (Any): [description]
            path (pathlib.Path | str): [description]

        Returns:
            [type]: [description]
            
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
                        method = locals()[value]
                    except AttributeError:
                        raise AttributeError(
                            f'{value} {attribute} could not be found')
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
    formats: amos.Dictionary[str, FileFormat] = amos.Dictionary(
        contents = {
            'csv': formats.FileFormat(
                name = 'csv',
                module = 'pandas',
                extensions = 'csv',
                loader = 'read_csv',
                saver = 'to_csv',
                parameters = {
                    'encoding': 'file_encoding',
                    'index_col': 'index_column',
                    'header': 'include_header',
                    'low_memory': 'conserve_memory',
                    'nrows': 'test_size'}),
            'excel': formats.FileFormat(
                name = 'excel',
                module = 'pandas',
                extensions = ('xlsx', 'xls'),
                loader = 'read_excel',
                saver = 'to_excel',
                parameters = {
                    'index_col': 'index_column',
                    'header': 'include_header',
                    'nrows': 'test_size'}),
            'feather': formats.FileFormat(
                name = 'feather',
                module = 'pandas',
                extensions = 'feather',
                loader = 'read_feather',
                saver = 'to_feather',
                parameters = {'nthreads': 'threads'}),
            'hdf': formats.FileFormat(
                name = 'hdf',
                module = 'pandas',
                extensions = 'hdf',
                loader = 'read_hdf',
                saver = 'to_hdf',
                parameters = {
                    'columns': 'included_columns',
                    'chunksize': 'test_size'}),
            'json': formats.FileFormat(
                name = 'json',
                module = 'json',
                extensions = 'json',
                loader = 'read_json',
                saver = 'to_json'),
            'pickle': formats.FileFormat(
                name = 'pickle',
                module = 'pickle',
                extensions = ['pickle', 'pkl'],
                loader = formats.load_pickle,
                saver = formats.save_pickle),
            'png': formats.FileFormat(
                name = 'png',
                module = 'seaborn',
                extensions = 'png',
                saver = 'save_fig',
                parameters = {
                    'bbox_inches': 'visual_tightness', 
                    'format': 'visual_format'}),
            'stata': formats.FileFormat(
                name = 'stata',
                module = 'pandas',
                extensions = 'dta',
                loader = 'read_stata',
                saver = 'to_stata',
                parameters = {'chunksize': 'test_size'}),
            'text': formats.FileFormat(
                name = 'text',
                module = None,
                extensions = ['txt', 'text'],
                loader = formats.load_text,
                saver = formats.save_text)})
    
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
        for key, instance in self.formats.items():
            if isinstance(instance.extensions, str):
                extensions[instance.extensions] = key
            elif isinstance(instance.extensions, Sequence):
                extensions.update(dict.fromkeys(instance.extensions, key))
            else:
                raise TypeError(
                    f'{instance.extensions} are not valid extension types')
   
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
                to the pandas or python method used internally.

        Returns:
            Any: depending upon method used for appropriate file format, a new
                variable of a supported type is returned.

        """
        file_path, file_format = self._prepare_transfer(
            file_path = file_path,
            folder = folder,
            file_name = file_name,
            file_format = file_format)
        parameters = self._get_parameters(file_format = file_format, **kwargs)
        loader = file_format.instances[file_format]
        return loader(file_path, **parameters)

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
                to the pandas or python method used internally.

        """
        file_path, file_format = self._prepare_transfer(
            file_path = file_path,
            folder = folder,
            file_name = file_name,
            file_format = file_format)
        parameters = self._get_parameters(file_format = file_format, **kwargs)
        if file_format.module:
            getattr(item, file_format.export_method)(item, **parameters)
        else:
            getattr(self, file_format.export_method)(item, **parameters)
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
        if file_name and extension:
            return pathlib.Path(folder).joinpath(f'{file_name}.{extension}')
        else:
            return pathlib.Path(folder)

    def _get_transfer_parameters(
        self,
        file_format: FileFormat, 
        shared: MutableMapping[str, str],
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
                    kwargs[specific] = shared[common]
        return kwargs # type: ignore

    def _prepare_transfer( 
        self,
        file_path: pathlib.Path | str,
        folder: pathlib.Path | str,
        file_name: str,
        file_format: str | FileFormat) -> (
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
        if file_path:
            file_path = amos.pathlibify(item = file_path)
            if not file_format:
                try:
                    file_format = [f for f in transfer.values()
                                if f.extension == file_path.suffix[1:]][0]
                except IndexError:
                    file_format = [f for f in transfer.values()
                                if f.extension == file_path.suffix][0]           
        file_format = self._validate_file_format(file_format = file_format)
        extension = file_format.extension
        if not file_path:
            file_path =self._combine_path(
                folder = folder, 
                file_name = file_name,
                extension = extension)
        return file_path, file_format

    def _validate_file_format(
        self,
        file_format: str | FileFormat) -> FileFormat:
        """Selects 'file_format' or returns FileFormat instance intact.

        Args:
            file_format (Union[str, FileFormat]): name of file format or a
                FileFormat instance.

        Raises:
            TypeError: if 'file_format' is neither a str nor FileFormat type.

        Returns:
            FileFormat: appropriate instance.

        """
        if file_format in transfer:
            return transfer[file_format]
        elif isinstance(file_format, FileFormat):
            return file_format
        elif (
            inspect.isclass(file_format) 
                and issubclass(file_format, FileFormat)):
            return file_format()
        else:
            raise TypeError(f'{file_format} is not a recognized file format')
        
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
            path = self.self._validate_io_folder(path = value)
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
"""Base classes for file management.

Contents:
    FileFormat: base class for defining rules and methods for different file
        formats.
    FileFramework: stores default settings, all file formats, and any other
        shared information used by FileManager.
    FileManager: interface for nagata file management. It provides a one-stop
        place for loading and saving all files of supported file types in an
        organizational structure specified by the user.

To Do:


"""
from __future__ import annotations

import abc
import contextlib
import dataclasses
import pathlib
import sys
from collections.abc import (
    Hashable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from typing import Any, ClassVar, TypeAlias, Unpack

from . import descriptors, utilities

if sys.version_info < (3, 12):
    GenericDict: TypeAlias = MutableMapping[Hashable, Any]
    GenericList: TypeAlias = MutableSequence[Any]
    Kwargs: TypeAlias = Unpack[GenericDict]
else:
    type GenericDict = MutableMapping[Hashable, Any]
    type GenericList = MutableSequence[Any]
    type Kwargs = Unpack[GenericDict]


@dataclasses.dataclass
class FileFormat:
    """File format information, loader, and saver.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading. Defaults to None.
        load_paraneters:
        save_parameters:

    Attributes:
        registry: stores sublcasses. Defaults to an empty `dict`.

    """

    extensions: ClassVar[str | Sequence[str]] = None
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    registry: ClassVar[GenericDict] = {}

    """ Initialization Methods """

    @classmethod
    def __init_subclass__(cls, *args: Any, **kwargs: Kwargs) -> None:
        """Calls parent class method, if it exists"""
        with contextlib.suppress(AttributeError):
            super().__init_subclass__(*args, **kwargs)
        if abc.ABC not in cls.__bases__:
            key = utilities._namify(cls)
            if key.startswith('file_format_'):
                key = key[12:]
            cls.registry[key] = cls(*args, **kwargs)

    # def __post_init__(self) -> None:
    #     """Automatically registers subclass."""
    #     with contextlib.suppress(AttributeError):
    #         super().__post_init__(*args, **kwargs)
    #     key = camina.namify(self)
    #     FileFramework.formats[key] = self

    # """ Public Methods """

    # def load(self, path: pathlib.Path | str, **kwargs) -> Any:
    #     """Loads a file of the included file format.

    #     Args:
    #         path (pathlib.Path | str): path of file to load from disk.

    #     Returns:
    #         Any: content of loaded file.

    #     """
    #     method = self._validate_io_method(attribute = 'loader')
    #     return method(path, **kwargs)

    # def save(self, item: Any, path: pathlib.Path | str, **kwargs) -> None:
    #     """Saves a file of the included file format.

    #     Args:
    #         item (Any): item to save to disk.
    #         path (pathlib.Path | str): path where the file should be saved.

    #     """
    #     method = self._validate_io_method(attribute = 'saver')
    #     method(item, path, **kwargs)
    #     return self

    # """ Private Methods """

    # def _validate_io_method(self, attribute: str) -> types.FunctionType:
    #     """[summary]

    #     Args:
    #         attribute (str): [description]

    #     Raises:
    #         AttributeError: [description]
    #         ValueError: [description]

    #     Returns:
    #         types.FunctionType: [description]

    #     """
    #     method = getattr(self, attribute)
    #     if isinstance(method, str):
    #         if self.module is None:
    #             try:
    #                 method = getattr(self, method)
    #             except AttributeError:
    #                 try:
    #                     method = getattr(transfer, method)
    #                 except AttributeError:
    #                     raise AttributeError(f'{method} could not be found')
    #     elif isinstance(method, Sequence):
    #         transfer_info = getattr(self, attribute)
    #         print('test transfer info',transfer_info[0], transfer_info[1] )
    #         package = importlib.__import__(transfer_info[0])
    #         importlib.util.spec.loader.exec_module(package)
    #         method = getattr(package, transfer_info[1])
    #             # package = importlib.__import__(self.module)
    #             # name = getattr(self, attribute)
    #             # method = getattr(package, name)
    #             # method = lazy.from_import_path(
    #             #     path = value,
    #             #     package = self.module)
    #     setattr(self, attribute, method)
    #     if not isinstance(method, types.FunctionType):
    #         raise ValueError(
    #             f'{attribute} must be a str, function, or method')
    #     return method


@dataclasses.dataclass
class FileFramework:
    """Default values and classes for file management

    Every attribute in FileFramework should be a class attribute so that it
    is accessible without instancing it (which it cannot be).

    Args:
        settings: default settings for file management.

    """

    settings: ClassVar[dict[Hashable, Any]] = {
        'file_encoding': 'windows-1252',
        'index_column': False,
        'header': 'infer',
        'conserve_memory': False,
        'test_size': 1000,
        'threads': -1,
        'visual_tightness': 'tight',
        'visual_format': 'png'}
    formats: ClassVar[GenericDict] = FileFormat.registry


@dataclasses.dataclass
class FileManager:
    """Basic File and folder management interface.

    Creates and stores dynamic and static file paths, properly formats files
    for import and export, and provides methods for loading and saving items.

    Args:
        framework: class with default settings, dict of supported file formats,
            and any other information needed for file management. Defaults to
            a FileFramework instance.

    """

    root_folder: descriptors.Folder = descriptors.Folder(default = '.')  # noqa: RUF009
    input_folder: pathlib.Path | str = 'root'
    interim_folder: pathlib.Path | str = 'root'
    output_folder: pathlib.Path | str = 'root'
    framework: type[FileFramework] = dataclasses.field(
        default_factory = FileFramework)

    """ Initialization Methods """

    def __post_init__(self) -> None:
        """Initializes and validates an instance."""
        # Calls parent and/or mixin initialization method(s).
        with contextlib.suppress(AttributeError):
            super().__post_init__()
        # Creates and validates the input, interim, and output folders.
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
            Dict-type object where keys are file extensions and values are the
                related key to the file_format in the 'formats' attribute.

        """
        extensions = {}
        for key, instance in self.framework.formats.items():
            if isinstance(instance.extensions, str):
                extensions[instance.extensions] = key
            elif isinstance(instance.extensions, Sequence):
                extensions |= dict.fromkeys(instance.extensions, key)
            else:
                raise TypeError(
                    f'{instance.extensions} are not valid extension types')
        return extensions

    """ Public Methods """

    def load(
        self,
        file_path: pathlib.Path | str | None = None,
        folder: pathlib.Path | str | None = None,
        file_name: str | None = None,
        file_format: str | FileFormat | None = None,
        **kwargs: Kwargs) -> Any:
        """Imports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        file_path is passed, folder and file_name are ignored.

        Args:
            file_path: a complete file path. Defaults to None.
            folder: a complete folder path or the name of a folder. Defaults to
                None.
            file_name: file name without extension. Defaults to None.
            file_format: object with information about
                how the file should be loaded or the key to such an object.
                Defaults to None.
            kwargs: can be passed if additional options are desired specific
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
            transfer_type = 'load',
            **kwargs)
        return file_format.load(path = file_path, **parameters)

    def save(
        self,
        item: Any,
        file_path: pathlib.Path | str | None = None,
        folder: pathlib.Path | str | None = None,
        file_name: str | None = None,
        file_format: str | FileFormat | None = None,
        **kwargs: Kwargs) -> None:
        """Exports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        file_path is passed, folder and file_name are ignored.

        Args:
            item: object to be save to disk.
            file_path: a complete file path. Defaults to
                None.
            folder: a complete folder path or the name of a
                folder. Defaults to None.
            file_name: file name without extension. Defaults to None.
            file_format: object with information about
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
            transfer_type = 'save',
            **kwargs)
        file_format.save(item = item, path = file_path, **parameters)
        return

    def validate(self, path: pathlib.Path | str) -> pathlib.Path:
        """Turns 'file_path' into a pathlib.Path.

        Args:
            path: str or Path to be validated. If
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
            value = getattr(self, f'{path}_folder', None)
            if isinstance(value, pathlib.Path):
                return value
            return pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            return path
        else:
            raise TypeError('path must be a str or Path type')

    """ Private Methods """

    def _combine_path(
        self,
        folder: pathlib.Path | str,
        file_name: str | None = None,
        extension: str | None = None) -> pathlib.Path:
        """Converts strings to pathlib Path object.

        If 'folder' matches an attribute, the value stored in that attribute
        is substituted for 'folder'.

        If 'name' and 'extension' are passed, a file path is created. Otherwise,
        a folder path is created.

        Args:
            folder: folder for file location.
            file_name: name of the file.
            extension: the extension of the file.

        Returns:
            Path: formed from string arguments.

        """
        folder = self._validate_io_folder(path = folder)
        if file_name and extension and '.' not in file_name:
            return pathlib.Path(folder).joinpath(f'{file_name}.{extension}')
        elif file_name and '.' in file_name:
            return pathlib.Path(folder).joinpath(file_name)
        else:
            return pathlib.Path(folder)

    def _get_transfer_parameters(
        self,
        file_format: FileFormat,
        transfer_type: str,
        **kwargs: Kwargs) -> MutableMapping[Hashable, Any]:
        """Creates complete parameters for a file input/output method.

        Args:
            file_format: an instance with information about the
                needed and optional parameters.
            transfer_type: str that indicates whether to get loading or saving
                parameters.
            kwargs: additional parameters to pass to an input/output method.

        Returns:
            MutableMapping[Hashable, Any]: parameters to be passed to an
                input/output method.

        """
        if parameters := getattr(file_format, f'{transfer_type}_parameters'):
            for specific, common in parameters.items():
                if specific not in kwargs:
                    kwargs[specific] = self.framework.settings[common]
        return kwargs

    def _prepare_transfer(
        self,
        file_path: pathlib.Path | str,
        folder: pathlib.Path | str,
        file_name: str,
        transfer_type: str,
        file_format: str | FileFormat | None = None) -> (
            tuple[pathlib.Path, FileFormat]):
        """Prepares file path related arguments for loading or saving a file.

        Args:
            file_path: a complete file path. Defaults to None.
            folder: a complete folder path or the name of a folder. Defaults to
                None.
            file_name: file name without extension. Defaults to None.
            transfer_type: str that indicates whether to get loading or saving
                parameters.
            file_format: object with information about how the file should be
                loaded/saved or the key to such an object. Defaults to None.

        Returns:
            tuple of a completed Path instance and FileFormat instance.

        """
        extension = None
        if file_path:
            file_path = self.validate(path = file_path)
            extension = file_path.suffix[1:]
        elif file_name and '.' in file_name:
            extension = utilities._cleave_str(file_name, divider = '.')[-1]
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
            file_format: name of file format or a FileFormat
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
            except KeyError as error:
                message = f'{file_format} is not a recognized file format'
                raise KeyError(message) from error
        if isinstance(file_format.extensions, str):
            return file_format.extensions
        else:
            return file_format.extensions[0]

    def _validate_file_format(
        self,
        file_format: str | FileFormat) -> FileFormat:
        """Selects 'file_format' or returns FileFormat instance intact.

        Args:
            file_format: name of file format or a
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
            except KeyError as error:
                message = f'{file_format} is not a recognized file format'
                raise KeyError(message) from error
        elif isinstance(file_format, FileFormat):
            return file_format
        else:
            raise TypeError(f'{file_format} is not a FileFormat type')

    def _validate_io_folder(self, path: str | pathlib.Path) -> pathlib.Path:
        """Validates an import and export path.'

        Args:
            path: path to validate.

        Returns:
            pathlib.Path: path in a pathlib.Path format.

        """
        if isinstance(path, str):
            attribute = f'{path}_folder'
            with contextlib.suppress(AttributeError):
                path = getattr(self, attribute)
        if isinstance(path, str):
            path = self.root_folder.joinpath(path)
        return path

    def _validate_io_folders(self) -> None:
        """Validates all import and export paths."""
        for field in dataclasses.fields(self):
            if field.name.endswith('_folder') and field.name != 'root_folder':
                value = getattr(self, field.name)
                path = self._validate_io_folder(path = value)
                setattr(self, field.name, path)
                self._write_folder(folder = path)
        return

    def _write_folder(self, folder: pathlib.Path | str) -> None:
        """Writes folder to disk.

        Parent folders are created as needed.

        Args:
            folder: intended folder to write to disk.

        """
        pathlib.Path(folder).mkdir(parents = True, exist_ok = True)
        return

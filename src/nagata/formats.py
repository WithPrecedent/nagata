"""File formats included out of the box.

Contents:
    Default FileFormat instances. They are not assigned to any values or dict
        because the act of instancing causes them to be stored in
        'FileFramework.formats'.

ToDo:


"""
from __future__ import annotations

import abc
import dataclasses
import sys
from typing import TYPE_CHECKING, Any, ClassVar

from . import base

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Mapping, Sequence


@dataclasses.dataclass
class FileFormatPickle(base.FileFormat):
    """File format information, loader, and saver.

    Args:
        extensions: str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters: shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = ('pickle', 'pkl')
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    def load(self, path: pathlib.Path | str, **kwargs: base.Kwargs) -> object:
        """Loads a pickled object.

        Args:
            path: path to a pickled object.
            kwargs: additional keyword arguments.

        Returns:
            object: item loaded from 'path'.

        """
        with open(path, **kwargs) as a_file:
            if 'pickle' not in sys.modules:
                import pickle
            return pickle.load(a_file)  # noqa: S301

    def save(
        self,
        item: Any,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Pickles 'item' at 'path.

        Args:
            item: item to pickle.
            path: path where 'item' should be pickled
            kwargs: additional keyword arguments.

        """
        with open(path, 'w', **kwargs) as a_file:
            if 'pickle' not in sys.modules:
                import pickle
            pickle.dump(item, a_file)
        return


@dataclasses.dataclass
class FileFormatText(base.FileFormat):
    """File format information, loader, and saver.

    Args:
        extensions: str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters: shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = ('txt', 'text')
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    """ Public Methods """

    def load(self, path: pathlib.Path | str, **kwargs: base.Kwargs) -> Any:
        """Loads a text file.

        Args:
            path: path to text file.
            kwargs: additional keyword arguments.

        Returns:
            str: text contained within the loaded file.

        """
        with open(path, **kwargs) as a_file:
            return a_file.read()

    def save(
        self,
        item: Any,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves str 'item' to a file at 'path'.

        Args:
            item: str item to save to a text file.
            path: path to which 'item' should be saved.
            kwargs: additional keyword arguments.

        """
        with open(path, 'w', **kwargs) as a_file:
            a_file.write(item)
        return


@dataclasses.dataclass
class FileFormatPandas(base.FileFormat, abc.ABC):
    """File format information, loader, and saver.

    Args:
        extensions: str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters: shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = None
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = None

    """ Public Methods """

    def load(self, path: pathlib.Path | str, **kwargs) -> object:
        """Loads a file to a pandas dataframe.

        Args:
            path: path to pandas dataframe.
            kwargs: additional keyword arguments.

        Raises:
            NotImplementedError: if 'loader' is None.

        Returns:
            pandas dataframe.

        """
        if self.loader is None:
            raise NotImplementedError(
                'pandas does not support loading for this data type')
        if 'pd' not in sys.modules:
            import pandas as pd
        return getattr(pd, self.loader)(path, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.GenericDict) -> None:
        """Saves dataframe 'item' to a file at 'path'.

        Args:
            item (object): pandas dataframe.
            path (pathlib.Path | str): path to which 'item' should be saved.

        Raises:
            NotImplementedError: if 'saver' is None.

        """
        if self.saver is None:
            raise NotImplementedError(
                'pandas does not support saving to this data type')
        saver = getattr(item, self.saver)
        saver(path, **kwargs)
        return


@dataclasses.dataclass
class FileFormatCSV(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'csv'
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'encoding': 'file_encoding',
        'index_col': 'index_column',
        'header': 'header',
        'nrows': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'encoding': 'file_encoding',
        'header': 'header',
        'index': 'index_column'}
    loader: ClassVar[str] = 'read_csv'
    saver: ClassVar[str] = 'to_csv'


@dataclasses.dataclass
class FileFormatExcel(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = ('xlsx', 'xls')
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'usecols': 'included_columns',
        'index_col': 'index_column',
        'header': 'header',
        'nrows': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'header': 'header',
        'index': 'index_column'}
    loader: ClassVar[str] = 'read_excel'
    saver: ClassVar[str] = 'to_excel'


@dataclasses.dataclass
class FileFormatFeather(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'feather'
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'columns': 'included_columns'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_feather'
    saver: ClassVar[str] = 'to_feather'


@dataclasses.dataclass
class FileFormatHDF(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = ('hdf', 'hdf5')
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'columns': 'included_columns',
        'chunksize': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_hdf'
    saver: ClassVar[str] = 'to_hdf'


@dataclasses.dataclass
class FileFormatJSON(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'json'
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'encoding': 'file_encoding',
        'nrows': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'encoding': 'file_encoding'}
    loader: ClassVar[str] = 'read_json'
    saver: ClassVar[str] = 'to_json'


@dataclasses.dataclass
class FileFormatLatex(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'latex'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'encoding': 'file_encoding',
        'header': 'header',
        'index': 'index_column'}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = 'to_latex'


@dataclasses.dataclass
class FileFormatParquet(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'parquet'
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'columns': 'included_columns'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'index': 'index_column'}
    loader: ClassVar[str] = 'read_parquet'
    saver: ClassVar[str] = 'to_parquet'


@dataclasses.dataclass
class FileFormatSTATA(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'dta'
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'columns': 'included_columns',
        'index_col': 'index_column',
        'header': 'header',
        'chunksize': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_stata'
    saver: ClassVar[str] = 'to_stata'


@dataclasses.dataclass
class FileFormatSQL(FileFormatPandas):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'sql'
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'columns': 'included_columns',
        'index_col': 'index_column',
        'chunksize': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'index': 'index_column'}
    loader: ClassVar[str] = 'read_sql_table'
    saver: ClassVar[str] = 'to_sql'


@dataclasses.dataclass
class FileFormatSeaborn(base.FileFormat, abc.ABC):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = None
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = None


    """ Public Methods """

    def load(self, path: pathlib.Path | str, **kwargs) -> object:
        """Loads a file to a pandas dataframe.

        Args:
            path (pathlib.Path | str): path to pandas dataframe.

        Raises:
            NotImplementedError: if 'loader' is None.

        Returns:
            object: pandas dataframe.

        """
        if self.loader is None:
            raise NotImplementedError(
                'seaborn does not support loading for this data type')
        if 'seaborn' not in sys.modules:
            import seaborn
        return getattr(seaborn, self.loader)(path, **kwargs)

    def save(self, item: object, path: pathlib.Path | str, **kwargs) -> None:
        """Saves dataframe 'item' to a file at 'path'.

        Args:
            item (object): pandas dataframe.
            path (pathlib.Path | str): path to which 'item' should be saved.

        Raises:
            NotImplementedError: if 'saver' is None.

        """
        if self.saver is None:
            raise NotImplementedError(
                'seaborn does not support saving to this data type')
        saver = getattr(item, self.saver)
        saver(path, **kwargs)
        return


@dataclasses.dataclass
class FileFormatPNG(FileFormatSeaborn):
    """File format information, loader, and saver.

    Args:
        extensions (Optional[Union[str, Sequence[str]]]): str file extension(s)
            associated with the format. If more than one is listed, the first
            one is used for saving new files and all will be used for loading.
            Defaults to None.
        parameters (Mapping[str, str]]): shared parameters to use from the pool
            of settings in FileFramework.settings where the key is the parameter
            name that the load or save method should use and the value is the
            key for the argument in the shared parameters. Defaults to an empty
            dict.

    """

    extensions: ClassVar[str | Sequence[str]] = 'png'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'bbox_inches': 'visual_tightness',
        'format': 'visual_format'}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = 'save_fig'

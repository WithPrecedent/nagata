"""File formats included out of the box.

Contents:
    Default FileFormat instances. They are not assigned to any values or dict
        because the act of instancing causes them to be stored in
        'FileFramework.formats'.

To Do:


"""
from __future__ import annotations

import abc
import dataclasses
import importlib
import pickle
import tomllib
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
        with open(path, 'rb', **kwargs) as a_file:
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
        with open(path, 'wb', **kwargs) as a_file:
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

    def load(
        self,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> object:
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
        pd = importlib.import_module('pandas')
        return getattr(pd, self.loader)(path, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves dataframe 'item' to a file at 'path'.

        Args:
            item (object): pandas dataframe.
            path (pathlib.Path | str): path to which 'item' should be saved.
            kwargs: additional keyword arguments.

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
        'nrows': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
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
        'columns': 'included_columns'}
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
        'encoding': 'file_encoding'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
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
        'columns': 'included_columns'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_stata'
    saver: ClassVar[str] = 'to_stata'


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

    def load(
        self,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> object:
        """Loads a file to a pandas dataframe.

        Args:
            path (pathlib.Path | str): path to pandas dataframe.
            kwargs: additional keyword arguments.

        Raises:
            NotImplementedError: if 'loader' is None.

        Returns:
            object: pandas dataframe.

        """
        if self.loader is None:
            raise NotImplementedError(
                'seaborn does not support loading for this data type')
        sns = importlib.import_module('seaborn')
        return getattr(sns, self.loader)(path, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves dataframe 'item' to a file at 'path'.

        Args:
            item (object): pandas dataframe.
            path (pathlib.Path | str): path to which 'item' should be saved.
            kwargs: additional keyword arguments.

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
    saver: ClassVar[str] = 'savefig'


@dataclasses.dataclass
class FileFormatTSV(FileFormatCSV):
    """File format information, loader, and saver.

    Tab-separated values. Uses the CSV methods with a tab separator.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = ('tsv', 'tab')

    def load(
        self,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> object:
        """Loads a tab-separated file to a pandas dataframe.

        Args:
            path: path to the file.
            kwargs: additional keyword arguments. `sep` defaults to a tab.

        Returns:
            pandas dataframe.

        """
        kwargs.setdefault('sep', '\t')
        return super().load(path, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves dataframe 'item' to a tab-separated file.

        Args:
            item: pandas dataframe.
            path: path to which 'item' should be saved.
            kwargs: additional keyword arguments. `sep` defaults to a tab.

        """
        kwargs.setdefault('sep', '\t')
        super().save(item, path, **kwargs)
        return


@dataclasses.dataclass
class FileFormatJSONLines(FileFormatJSON):
    """File format information, loader, and saver.

    JSON Lines (one JSON record per line).

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = ('jsonl', 'ndjson')
    load_parameters: ClassVar[Mapping[str, str] | None] = {
        'encoding': 'file_encoding',
        'nrows': 'test_size'}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    def load(
        self,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> object:
        """Loads a JSON Lines file to a pandas dataframe.

        Args:
            path: path to the file.
            kwargs: additional keyword arguments. `lines` defaults to True.

        Returns:
            pandas dataframe.

        """
        kwargs.setdefault('lines', True)
        return super().load(path, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves dataframe 'item' to a JSON Lines file.

        Args:
            item: pandas dataframe.
            path: path to which 'item' should be saved.
            kwargs: additional keyword arguments. `orient` defaults to
                'records' and `lines` defaults to True.

        """
        kwargs.setdefault('orient', 'records')
        kwargs.setdefault('lines', True)
        super().save(item, path, **kwargs)
        return


@dataclasses.dataclass
class FileFormatORC(FileFormatPandas):
    """File format information, loader, and saver.

    Apache ORC columnar files. Requires `pyarrow`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'orc'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_orc'
    saver: ClassVar[str] = 'to_orc'


@dataclasses.dataclass
class FileFormatXML(FileFormatPandas):
    """File format information, loader, and saver.

    XML files. Requires `lxml`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'xml'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_xml'
    saver: ClassVar[str] = 'to_xml'


@dataclasses.dataclass
class FileFormatHTML(FileFormatPandas):
    """File format information, loader, and saver.

    HTML tables. Requires `lxml`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = ('html', 'htm')
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_html'
    saver: ClassVar[str] = 'to_html'

    def load(
        self,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> object:
        """Loads a table from an HTML file to a pandas dataframe.

        Args:
            path: path to the HTML file.
            kwargs: additional keyword arguments, such as `match` to select a
                specific table.

        Returns:
            pandas dataframe of the first table found (that matches `match`,
                if passed).

        """
        return super().load(path, **kwargs)[0]


@dataclasses.dataclass
class FileFormatMarkdown(FileFormatPandas):
    """File format information, loader, and saver.

    Markdown tables (saving only). Requires `tabulate`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = ('md', 'markdown')
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = 'to_markdown'


@dataclasses.dataclass
class FileFormatFixedWidth(FileFormatPandas):
    """File format information, loader, and saver.

    Fixed-width formatted text files (loading only).

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'fwf'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_fwf'
    saver: ClassVar[str] = None


@dataclasses.dataclass
class FileFormatSAS(FileFormatPandas):
    """File format information, loader, and saver.

    SAS files (loading only).

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = ('sas7bdat', 'xpt')
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_sas'
    saver: ClassVar[str] = None


@dataclasses.dataclass
class FileFormatSPSS(FileFormatPandas):
    """File format information, loader, and saver.

    SPSS files (loading only). Requires `pyreadstat`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'sav'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}
    loader: ClassVar[str] = 'read_spss'
    saver: ClassVar[str] = None


@dataclasses.dataclass
class FileFormatYAML(base.FileFormat):
    """File format information, loader, and saver.

    YAML files. Requires `pyyaml`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = ('yaml', 'yml')
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    def load(self, path: pathlib.Path | str, **kwargs: base.Kwargs) -> object:
        """Loads a YAML file.

        Args:
            path: path to the YAML file.
            kwargs: additional keyword arguments for `open`.

        Returns:
            object: parsed contents of the file.

        """
        yaml = importlib.import_module('yaml')
        with open(path, encoding = 'utf-8', **kwargs) as a_file:
            return yaml.safe_load(a_file)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves `item` to a YAML file.

        Args:
            item: object to save. It must be YAML-serializable.
            path: path to which 'item' should be saved.
            kwargs: additional keyword arguments for `yaml.safe_dump`.

        """
        yaml = importlib.import_module('yaml')
        with open(path, 'w', encoding = 'utf-8') as a_file:
            yaml.safe_dump(item, a_file, **kwargs)
        return


@dataclasses.dataclass
class FileFormatTOML(base.FileFormat):
    """File format information, loader, and saver.

    TOML files. Loading uses the standard library; saving requires
    `tomli-w`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'toml'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    def load(self, path: pathlib.Path | str, **kwargs: base.Kwargs) -> object:
        """Loads a TOML file.

        Args:
            path: path to the TOML file.
            kwargs: additional keyword arguments for `tomllib.load`.

        Returns:
            dict: parsed contents of the file.

        """
        with open(path, 'rb') as a_file:
            return tomllib.load(a_file, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves mapping `item` to a TOML file.

        Args:
            item: mapping to save.
            path: path to which 'item' should be saved.
            kwargs: additional keyword arguments for `tomli_w.dump`.

        """
        tomli_w = importlib.import_module('tomli_w')
        with open(path, 'wb') as a_file:
            tomli_w.dump(item, a_file, **kwargs)
        return


@dataclasses.dataclass
class FileFormatNPY(base.FileFormat):
    """File format information, loader, and saver.

    NumPy arrays in `.npy` files. Requires `numpy`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'npy'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    def load(self, path: pathlib.Path | str, **kwargs: base.Kwargs) -> object:
        """Loads a NumPy array.

        Args:
            path: path to the `.npy` file.
            kwargs: additional keyword arguments for `numpy.load`.

        Returns:
            numpy.ndarray: loaded array.

        """
        numpy = importlib.import_module('numpy')
        return numpy.load(path, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves array `item` to a `.npy` file.

        Args:
            item: array-like object to save.
            path: path to which 'item' should be saved.
            kwargs: additional keyword arguments for `numpy.save`.

        """
        numpy = importlib.import_module('numpy')
        numpy.save(path, item, **kwargs)
        return


@dataclasses.dataclass
class FileFormatNPZ(base.FileFormat):
    """File format information, loader, and saver.

    Compressed collections of NumPy arrays in `.npz` files. Requires
    `numpy`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'npz'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    def load(self, path: pathlib.Path | str, **kwargs: base.Kwargs) -> object:
        """Loads a `.npz` archive.

        Args:
            path: path to the `.npz` file.
            kwargs: additional keyword arguments for `numpy.load`.

        Returns:
            dict: array names mapped to loaded arrays.

        """
        numpy = importlib.import_module('numpy')
        with numpy.load(path, **kwargs) as archive:
            return {name: archive[name] for name in archive.files}

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves arrays in `item` to a compressed `.npz` archive.

        Args:
            item: mapping of names to arrays, or a single array, which is
                stored under the name 'arr_0'.
            path: path to which 'item' should be saved.
            kwargs: additional arrays to store, keyed by name.

        """
        numpy = importlib.import_module('numpy')
        arrays = dict(item) if hasattr(item, 'items') else {'arr_0': item}
        numpy.savez_compressed(path, **arrays, **kwargs)
        return


@dataclasses.dataclass
class FileFormatJoblib(base.FileFormat):
    """File format information, loader, and saver.

    Joblib files, commonly used for fitted scikit-learn models. Requires
    `joblib`.

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'joblib'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {}

    def load(self, path: pathlib.Path | str, **kwargs: base.Kwargs) -> object:
        """Loads an object stored with joblib.

        Args:
            path: path to the joblib file.
            kwargs: additional keyword arguments for `joblib.load`.

        Returns:
            object: loaded item.

        """
        joblib = importlib.import_module('joblib')
        return joblib.load(path, **kwargs)

    def save(
        self,
        item: object,
        path: pathlib.Path | str,
        **kwargs: base.Kwargs) -> None:
        """Saves `item` with joblib.

        Args:
            item: object to save.
            path: path to which 'item' should be saved.
            kwargs: additional keyword arguments for `joblib.dump`.

        """
        joblib = importlib.import_module('joblib')
        joblib.dump(item, path, **kwargs)
        return


@dataclasses.dataclass
class FileFormatJPEG(FileFormatSeaborn):
    """File format information, loader, and saver.

    JPEG images of figures (saving only).

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = ('jpg', 'jpeg')
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'bbox_inches': 'visual_tightness'}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = 'savefig'


@dataclasses.dataclass
class FileFormatSVG(FileFormatSeaborn):
    """File format information, loader, and saver.

    SVG images of figures (saving only).

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'svg'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'bbox_inches': 'visual_tightness'}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = 'savefig'


@dataclasses.dataclass
class FileFormatPDF(FileFormatSeaborn):
    """File format information, loader, and saver.

    PDF images of figures (saving only).

    Args:
        extensions: str file extension(s) associated with the format. If more
            than one is listed, the first one is used for saving new files and
            all will be used for loading.
        parameters: shared parameters to use from the pool of settings in
            FileFramework.settings where the key is the parameter name that the
            load or save method should use and the value is the key for the
            argument in the shared parameters.

    """

    extensions: ClassVar[str | Sequence[str]] = 'pdf'
    load_parameters: ClassVar[Mapping[str, str] | None] = {}
    save_parameters: ClassVar[Mapping[str, str] | None] = {
        'bbox_inches': 'visual_tightness'}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = 'savefig'

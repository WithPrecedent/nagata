"""
formats: default file formats included out of the box.
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
    Default FileFormat instances. They are not assigned to any values or dict
        because the act of instancing causes them to be stored in 
        'FileFramework.formats'.
    
ToDo:

    
"""
from __future__ import annotations
import abc
from collections.abc import Hashable, Mapping, MutableMapping, Sequence
import contextlib
import dataclasses
import importlib
import importlib.util
import pathlib
import sys
import types
from typing import Any, ClassVar, Optional, Type

import amos
import miller

from . import core
from . import transfer


@dataclasses.dataclass
class FileFormatPickle(core.FileFormat):
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
    extensions: ClassVar[str | Sequence[str]] = ('pickle', 'pkl')
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    
    def load(self, path: pathlib.Path | str, **kwargs) -> object:
        """Loads a pickled object.

        Args:
            path (pathlib.Path | str): path to a pickled object.

        Returns:
            object: item loaded from 'path'.
            
        """   
        a_file = open(path, 'r', **kwargs)
        if 'pickle' not in sys.modules:
            import pickle
        loaded = pickle.load(a_file)
        a_file.close()
        return loaded

    def save(self, item: Any, path: pathlib.Path | str, **kwargs) -> None:
        """Pickles 'item' at 'path.

        Args:
            item (Any): item to pickle.
            path (pathlib.Path | str): path where 'item' should be pickled
            
        """   
        a_file = open(path, 'w', **kwargs)
        if 'pickle' not in sys.modules:
            import pickle
        pickle.dump(item, a_file)
        a_file.close()
        return


@dataclasses.dataclass
class FileFormatText(core.FileFormat):
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
    extensions: ClassVar[str | Sequence[str]] = ('txt', 'text')
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    
    """ Public Methods """
    
    def load(self, path: pathlib.Path | str, **kwargs) -> Any:
        """Loads a text file.

        Args:
            path (pathlib.Path | str): path to text file.

        Returns:
            str: text contained within the loaded file.
            
        """    
        a_file = open(path, 'r', **kwargs)
        loaded = a_file.read()
        a_file.close()
        return loaded
    
    def save(self, item: Any, path: pathlib.Path | str, **kwargs) -> None:
        """Saves str 'item' to a file at 'path'.

        Args:
            item (str): str item to save to a text file.
            path (pathlib.Path | str): path to which 'item' should be saved.
            
        """    
        a_file = open(path, 'w', **kwargs)
        a_file.write(item)
        a_file.close()
        return   


@dataclasses.dataclass
class FileFormatPandas(core.FileFormat, abc.ABC):
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = None

    """ Public Methods """
    
    def load(self, path: pathlib.Path | str, **kwargs) -> Any:
        """Loads a text file.

        Args:
            path (pathlib.Path | str): path to text file.

        Returns:
            str: text contained within the loaded file.
            
        """
        if 'pandas' not in sys.modules:
            import pandas 
        loader = getattr(pandas, self.loader)
        return loader(path, **kwargs)
    
    def save(self, item: Any, path: pathlib.Path | str, **kwargs) -> None:
        """Saves str 'item' to a file at 'path'.

        Args:
            item (str): str item to save to a text file.
            path (pathlib.Path | str): path to which 'item' should be saved.
            
        """    
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'encoding': 'file_encoding',
        'index_col': 'index_column',
        'header': 'header',
        'low_memory': 'conserve_memory',
        'nrows': 'test_size'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'encoding': 'file_encoding',
        'header': 'header',
        'low_memory': 'conserve_memory',
        'nrows': 'test_size'}
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
    parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'index_col': 'index_column',
        'header': 'header',
        'nrows': 'test_size'}
    loader: ClassVar[str] = 'read_excel'
    saver: ClassVar[str] = 'to_excel'
            
# core.FileFormat(
#     name = 'csv',
#     module = 'pandas',
#     extensions = 'csv',
#     loader = ('pandas', 'read_csv'),
#     saver = ('pandas.DataFrame', 'to_csv'),
#     parameters = {
#         'encoding': 'file_encoding',
#         'index_col': 'index_column',
#         'header': 'header',
#         'low_memory': 'conserve_memory',
#         'nrows': 'test_size'})

# core.FileFormat(
#     name = 'excel',
#     module = 'pandas',
#     extensions = ('xlsx', 'xls'),
#     loader = 'read_excel',
#     saver = 'DataFrame.to_excel',
#     parameters = {
#         'index_col': 'index_column',
#         'header': 'header',
#         'nrows': 'test_size'})

# core.FileFormat(
#     name = 'feather',
#     module = 'pandas',
#     extensions = 'feather',
#     loader = 'read_feather',
#     saver = 'DataFrame.to_feather',
#     parameters = {'nthreads': 'threads'})

# core.FileFormat(
#     name = 'hdf',
#     module = 'pandas',
#     extensions = ('hdf', 'hdf5'),
#     loader = 'read_hdf',
#     saver = 'DataFrame.to_hdf',
#     parameters = {
#         'columns': 'included_columns',
#         'chunksize': 'test_size'})

# core.FileFormat(
#     name = 'json',
#     module = 'json',
#     extensions = 'json',
#     loader = 'read_json',
#     saver = 'DataFrame.to_json')

# core.FileFormat(
#     name = 'pickle',
#     module = None,
#     extensions = ['pickle', 'pkl'],
#     loader = transfer.load_pickle,
#     saver = transfer.save_pickle)

# core.FileFormat(
#     name = 'png',
#     module = 'seaborn',
#     extensions = 'png',
#     saver = 'save_fig',
#     parameters = {
#         'bbox_inches': 'visual_tightness', 
#         'format': 'visual_format'})

# core.FileFormat(
#     name = 'stata',
#     module = 'pandas',
#     extensions = 'dta',
#     loader = 'read_stata',
#     saver = 'DataFrame.to_stata',
#     parameters = {'chunksize': 'test_size'})

# core.FileFormat(
#     name = 'text',
#     module = None,
#     extensions = ['txt', 'text'],
#     loader = transfer.load_text,
#     saver = transfer.save_text)
    
# core.FileFormat(
#     name = 'csv',
#     module = 'pandas',
#     extensions = 'csv',
#     loader = ('pandas', 'read_csv'),
#     saver = ('pandas.DataFrame', 'to_csv'),
#     parameters = {
#         'encoding': 'file_encoding',
#         'index_col': 'index_column',
#         'header': 'header',
#         'low_memory': 'conserve_memory',
#         'nrows': 'test_size'})

# core.FileFormat(
#     name = 'excel',
#     module = 'pandas',
#     extensions = ('xlsx', 'xls'),
#     loader = 'read_excel',
#     saver = 'DataFrame.to_excel',
#     parameters = {
#         'index_col': 'index_column',
#         'header': 'header',
#         'nrows': 'test_size'})

# core.FileFormat(
#     name = 'feather',
#     module = 'pandas',
#     extensions = 'feather',
#     loader = 'read_feather',
#     saver = 'DataFrame.to_feather',
#     parameters = {'nthreads': 'threads'})

# core.FileFormat(
#     name = 'hdf',
#     module = 'pandas',
#     extensions = ('hdf', 'hdf5'),
#     loader = 'read_hdf',
#     saver = 'DataFrame.to_hdf',
#     parameters = {
#         'columns': 'included_columns',
#         'chunksize': 'test_size'})

# core.FileFormat(
#     name = 'json',
#     module = 'json',
#     extensions = 'json',
#     loader = 'read_json',
#     saver = 'DataFrame.to_json')

# core.FileFormat(
#     name = 'pickle',
#     module = None,
#     extensions = ['pickle', 'pkl'],
#     loader = transfer.load_pickle,
#     saver = transfer.save_pickle)

# core.FileFormat(
#     name = 'png',
#     module = 'seaborn',
#     extensions = 'png',
#     saver = 'save_fig',
#     parameters = {
#         'bbox_inches': 'visual_tightness', 
#         'format': 'visual_format'})

# core.FileFormat(
#     name = 'stata',
#     module = 'pandas',
#     extensions = 'dta',
#     loader = 'read_stata',
#     saver = 'DataFrame.to_stata',
#     parameters = {'chunksize': 'test_size'})

# core.FileFormat(
#     name = 'text',
#     module = None,
#     extensions = ['txt', 'text'],
#     loader = transfer.load_text,
#     saver = transfer.save_text)
    
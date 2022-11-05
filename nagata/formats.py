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
from typing import Any, ClassVar, Optional, Type

from . import core


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
                'pandas does not support loading for this data type')
        else:
            if 'pandas' not in sys.modules:
                import pandas 
            loader = getattr(pandas, self.loader)
            return loader(path, **kwargs)
    
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
                'pandas does not support saving to this data type')   
        else:
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
        'nrows': 'test_size'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'usecols': 'included_columns',
        'index_col': 'index_column',
        'header': 'header',
        'nrows': 'test_size'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'columns': 'included_columns'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'columns': 'included_columns',
        'chunksize': 'test_size'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'encoding': 'file_encoding',
        'nrows': 'test_size'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'columns': 'included_columns'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'columns': 'included_columns',
        'index_col': 'index_column',
        'header': 'header',
        'chunksize': 'test_size'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'columns': 'included_columns',
        'index_col': 'index_column',
        'chunksize': 'test_size'}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'index': 'index_column'}
    loader: ClassVar[str] = 'read_sql_table'
    saver: ClassVar[str] = 'to_sql'


@dataclasses.dataclass
class FileFormatSeaborn(core.FileFormat, abc.ABC):
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
        else:
            if 'seaborn' not in sys.modules:
                import seaborn
            loader = getattr(seaborn, self.loader)
            return loader(path, **kwargs)
    
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
        else:
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
    load_parameters: ClassVar[Optional[Mapping[str, str]]] = {}
    save_parameters: ClassVar[Optional[Mapping[str, str]]] = {
        'bbox_inches': 'visual_tightness', 
        'format': 'visual_format'}
    loader: ClassVar[str] = None
    saver: ClassVar[str] = 'save_fig'
 
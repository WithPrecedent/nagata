"""
transfer: custom functions for loading and saving
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
    load_pickle:
    save_pickle:
    load_text:
    save_text:
    
ToDo:

    
"""
from __future__ import annotations
from collections.abc import Mapping, MutableSequence
import pathlib
import sys
from typing import Any, ClassVar, Optional, Type

from . import lazy


def load_pickle(path: pathlib.Path | str, **kwargs) -> object:
    """Loads a pickled object.

    Args:
        path (pathlib.Path | str): path to a pickled object.

    Returns:
        object: item loaded from 'path'.
        
    """   
    a_file = open(path, 'r', **kwargs)
    loaded = sys.modules['pickle'].load(a_file)
    a_file.close()
    return loaded

def save_pickle(
    item: Any, 
    path: pathlib.Path | str, 
    **kwargs) -> None:
    """Pickles 'item' at 'path.

    Args:
        item (Any): item to pickle.
        path (pathlib.Path | str): path where 'item' should be pickled
        
    """   
    a_file = open(path, 'w', **kwargs)
    sys.modules['pickle'].dump(item, a_file)
    a_file.close()
    return

def load_text(path: pathlib.Path | str, **kwargs) -> str:
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

def save_text(item: str, path: pathlib.Path | str, **kwargs) -> None:
    """Saves str 'item' to a file at 'path'.

    Args:
        item (str): str item to save to a text file.
        path (pathlib.Path | str): path to which 'item' should be saved.
        
    """    
    a_file = open(path, 'w', **kwargs)
    a_file.write(item)
    a_file.close()
    return
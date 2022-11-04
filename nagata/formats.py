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

from . import core
from . import transfer


core.FileFormat(
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
        'nrows': 'test_size'})

core.FileFormat(
    name = 'excel',
    module = 'pandas',
    extensions = ('xlsx', 'xls'),
    loader = 'read_excel',
    saver = 'to_excel',
    parameters = {
        'index_col': 'index_column',
        'header': 'include_header',
        'nrows': 'test_size'})

core.FileFormat(
    name = 'feather',
    module = 'pandas',
    extensions = 'feather',
    loader = 'read_feather',
    saver = 'to_feather',
    parameters = {'nthreads': 'threads'})

core.FileFormat(
    name = 'hdf',
    module = 'pandas',
    extensions = 'hdf',
    loader = 'read_hdf',
    saver = 'to_hdf',
    parameters = {
        'columns': 'included_columns',
        'chunksize': 'test_size'})

core.FileFormat(
    name = 'json',
    module = 'json',
    extensions = 'json',
    loader = 'read_json',
    saver = 'to_json')

core.FileFormat(
    name = 'pickle',
    module = 'pickle',
    extensions = ['pickle', 'pkl'],
    loader = transfer.load_pickle,
    saver = transfer.save_pickle)

core.FileFormat(
    name = 'png',
    module = 'seaborn',
    extensions = 'png',
    saver = 'save_fig',
    parameters = {
        'bbox_inches': 'visual_tightness', 
        'format': 'visual_format'})

core.FileFormat(
    name = 'stata',
    module = 'pandas',
    extensions = 'dta',
    loader = 'read_stata',
    saver = 'to_stata',
    parameters = {'chunksize': 'test_size'})

core.FileFormat(
    name = 'text',
    module = None,
    extensions = ['txt', 'text'],
    loader = transfer.load_text,
    saver = transfer.save_text)
    
"""
test_miller: tests functions and classes in the miller packae
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

ToDo:
    
    
"""
from __future__ import annotations
import dataclasses
import inspect
import pathlib
import types
from typing import Any, ClassVar

import nagata

   
    
def test_all() -> None:
    manager = nagata.FileManager(
        root_folder = pathlib.Path('.').joinpath('tests'),
        input_folder = 'dummy_folder',
        output_folder = 'dummy__output_folder')
    poem = manager.load(file_name = 'poem.txt')
    return

if __name__ == '__main__':
    test_all()


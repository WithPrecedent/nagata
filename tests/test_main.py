"""Main file for unit tests."""

from __future__ import annotations
import pathlib

import nagata

   
def test_all() -> None:
    manager = nagata.FileManager(
        root_folder = pathlib.Path('.').joinpath('tests'),
        input_folder = 'dummy_folder',
        output_folder = 'dummy_output_folder')
    poem = manager.load(file_name = 'poem.txt')
    manager.save(item = poem, file_name = 'poem_out.txt')
    poem_again = manager.load(file_name = 'poem', file_format = 'text')
    manager.save(
        item = poem_again, 
        file_name = 'poem_out', 
        file_format = 'text')
    poem_three = manager.load(
        file_name = 'poem', 
        folder = 'input', 
        file_format = 'text')
    manager.save(
        item = poem_three,
        file_name = 'poem',
        folder = 'output',
        file_format = 'text')
    test_csv = manager.load(file_name = 'csv_test_file.csv')
    manager.save(test_csv, file_name = 'test_csv_out.csv')
    return

if __name__ == '__main__':
    test_all()



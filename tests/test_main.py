"""Main file for unit tests."""

from __future__ import annotations
import pathlib

import nagata


def test_all() -> None:
    test_folder = pathlib.Path('tests')
    input_folder = test_folder / 'dummy_folder'
    output_folder = test_folder / 'dummy_output_folder'
    manager = nagata.FileManager(
        root_folder = test_folder,
        input_folder = input_folder,
        output_folder = output_folder)
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
    # test_csv = manager.load(file_name = 'csv_test_file.csv')
    # manager.save(test_csv, file_name = 'test_csv_out.csv')
    return

if __name__ == '__main__':
    test_all()



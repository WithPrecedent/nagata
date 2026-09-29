"""FileManager subclasses.

Contents:


To Do:


"""
from __future__ import annotations

import dataclasses
import pathlib

from . import base


@dataclasses.dataclass
class DataScienceManager(base.FileManager):
    """File and folder management interface for data science projects.

    Args:
        framework: class with default settings, dict of supported file formats,
            and any other information needed for file management. Defaults to
            a FileFramework instance.

    """

    root_folder: pathlib.Path | str = pathlib.Path()
    input_folder: pathlib.Path | str = 'input'
    interim_folder: pathlib.Path | str = 'interim'
    output_folder: pathlib.Path | str = 'output'
    reports_folder: pathlib.Path | str = 'reports'
    visuals_folder: pathlib.Path | str = 'visuals'



@dataclasses.dataclass
class WritingManager(base.FileManager):
    """File and folder management interface for writing projects.

    Args:
        framework: class with default settings, dict of supported file formats,
            and any other information needed for file management. Defaults to
            a FileFramework instance.

    """

    root_folder: pathlib.Path | str = pathlib.Path()
    input_folder: pathlib.Path | str = 'input'
    interim_folder: pathlib.Path | str = 'interim'
    output_folder: pathlib.Path | str = 'output'
    reports_folder: pathlib.Path | str = 'reports'
    visuals_folder: pathlib.Path | str = 'visuals'
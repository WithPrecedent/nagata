"""Python file management using a common, intuitive syntax"""

from __future__ import annotations

__version__ = '0.1.7'

__author__: str = 'Corey Rayburn Yung'

__all__: list[str] = []


from .core import FileFormat, FileFramework, FileManager
from .formats import (
    FileFormatCSV,
    FileFormatExcel,
    FileFormatFeather,
    FileFormatHDF,
    FileFormatJSON,
    FileFormatLatex,
    FileFormatPNG,
    FileFormatPandas,
    FileFormatParquet,
    FileFormatPickle,
    FileFormatSQL,
    FileFormatSTATA,
    FileFormatSeaborn,
    FileFormatText,
)
from .lazy import (
    Delayed,
    Importer,
    absolute_import,
    absolute_subpackage_import,
    from_file_path,
    from_import_path,
    from_importables,
    from_path,
    relative_import,
    relative_subpackage_import,
)

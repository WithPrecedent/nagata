"""Python file management using a common, intuitive syntax"""

from __future__ import annotations

__version__ = '0.1.7'

__author__: str = 'Corey Rayburn Yung'

__all__: list[str] = []


from .base import *  # noqa: F403
from .descriptors import *  # noqa: F403
from .formats import *  # noqa: F403
from .lazy import *  # noqa: F403

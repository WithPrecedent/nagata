"""Lazy importing classes and functions.

Contents:
    from_path:
    from_file_path:
    from_import_path:
    absolute_import:
    absolute_supackage_import:
    relative_import:
    relative_subpackage_import:
    from_importables:
    Importer:
    Delayed:

To Do:


"""
from __future__ import annotations

import dataclasses
import importlib
import importlib.util
import pathlib
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import types
    from collections.abc import MutableMapping


""" Importing Tools """

def from_path(
    path: pathlib.Path | str,
    name: str | None = None) -> types.ModuleType:
    """Imports and returns module from import or file path at `name`.

    Args:
        path: import or file path of module to load.
        name: name to store module at in `sys.modules`. If it is None, the stem
            of `path` is used. Defaults to None.

    Returns:
        Imported module.

    """
    if isinstance(path, pathlib.Path) or '\\' in path or r'/' in path:
        return from_file_path(path = path, name = name)
    return from_import_path(path = path)

def from_file_path(
    path: pathlib.Path | str,
    name: str | None = None) -> types.ModuleType:
    """Imports and returns module from file path at `name`.

    Args:
        path: import or file path of module to load.
        name: name to store module at in `sys.modules`. If it is None, the stem
            of `path` is used. Defaults to None.

    Returns:
        Imported module.

    """
    if isinstance(path, str):
        path = pathlib.Path(path)
    if name is None:
        name = path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        raise ImportError(f'Failed to create spec from {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def from_import_path(path: str, package: str | None = None) -> Any:
    """[summary]

    Args:
        path: [description]
        package: [description]. Defaults to None.

    Returns:
        Any: [description]

    """
    # if package and isinstance(path, str):
    #     path = '.'.join([path, package])
    try:
        return sys.modules[path]
    except KeyError as e:
        techniques = [
            absolute_import,
            absolute_subpackage_import,
            relative_import,
            relative_subpackage_import]
        for technique in techniques:
            try:
                return technique(path, package)
            except ModuleNotFoundError:
                item = path.rsplit('.', maxsplit = 1)[-1]
                module_name = path[:-len(item) - 1]
                module = technique(module_name, package)
                return getattr(module, item)
        raise ModuleNotFoundError(f'{path} could not be imported') from e

def absolute_import(path: str, package: str) -> Any:  # noqa: ARG001
    """Imports the item at `path`.

    Args:
        path: import path of the item to import.
        package: name of the package for relative imports. It is currently
            unused when `path` is an absolute path.

    Returns:
        Any: imported item.

    """
    if path.startswith('.'):
        path = path[1:]
        return relative_subpackage_import(path = path)
    return importlib.import_module(path)

def absolute_subpackage_import(path: str, package: str) -> Any:
    """[summary]

    Args:
        path: [description]
        package: [description].

    Returns:
        Any: [description]

    """
    if path.startswith('.'):
        path = path[1:]
        return relative_subpackage_import(path = path, package = package)
    return importlib.import_module(path, package = package)

def relative_import(path: str) -> Any:
    """[summary]

    Args:
        path: [description]

    Returns:
        Any: [description]

    """
    if not path.startswith('.'):
        path = f'.{path}'
    return importlib.import_module(sys.path_importer_cache)

def relative_subpackage_import(path: str, package: str) -> Any:
    """[summary]

    Args:
        path: [description]
        package: [description].

    Returns:
        Any: [description]

    """
    if not path.startswith('.'):
        path = f'.{path}'
    return importlib.import_module(path, package = package)

def from_importables(
    name: str,
    importables: MutableMapping[str, str],
    package: str | None = None) -> Any:
    """Lazily imports modules and items within them.

    Lazy importing means that modules are only imported when they are first
    accessed. This can save memory and keep namespaces decluttered.

    This code is adapted from PEP 562: https://www.python.org/dev/peps/pep-0562/
    which outlines how the decision to incorporate `__getattr__` functions to
    modules allows lazy loading. Rather than place this function solely within
    `__getattr__`, it is included here seprately so that it can easily be called
    by `__init__.py` files throughout nagata and by users (as
    `nagata.load.from_dict`).

    To effectively use `from_dict` in an `__init__.py` file, the user needs to
    pass a `importables` dict which indicates how users should accesss imported
    modules and included items. This modules includes an example `importables`
    dict and how to easily add this function to a `__getattr__` function.

    Instead of limiting its lazy imports to full import paths as the example in
    PEP 562, this function has 2 major advantages:
        1) It allows importing items within modules and not just modules. The
            function first tries to import `name` assuming it is a module. But
            if that fails, it parses the last portion of `name` and attempts to
            import the preceding module and then returns the item within it.
        2) It allows import paths that are less than the full import path by
            using the `importables` dict. `importables` has keys which are the
            name of the attribute being sought and values which are the full
            import path (dropping the leading `.`). `importables` thus acts as
            the normal import block in an __init__.py file but insures that all
            importing is done lazily.

    Args:
        name: name of module or item within a module.
        package: name of package from which the module is sought.
        importables (MutableMapping[str, str]): keys are the access names for
            items sought and values are the import path where the item is
            actually located.

    Raises:
        AttributeError: if there is no module or item matching `name` im
            `importables`.

    Returns:
        Any: a module or item stored within a module.

    """
    try:
        return from_import_path(path = importables[name], package = package)
    except KeyError as e:
        raise KeyError(f'{name} is not in importables') from e


""" Class Implementations """

@dataclasses.dataclass
class Importer:
    """Lazy importer that uses a dict to lazily import items.

    Args:
        package: name of package to which the `importables` are linked.
        importables: dict keys are names
            used to refer to importable item and values are the import paths of
            the importable items. Defaults to an empty dict.

    """

    package: str
    importables: MutableMapping[str, str] | None = dataclasses.field(
        default_factory = dict)

    """ Public Methods """

    def load(self, name: str) -> Any:
        """Returns the imported item stored under `name`.

        Args:
            name: key of the item in `importables`.

        Raises:
            KeyError: if `name` is not in `importables`.

        Returns:
            Any: imported item.

        """
        if name not in self.importables:
            raise KeyError(f'{name} is not in importables')
        if not isinstance(self.importables[name], str):
            return self.importables[name]
        imported = from_importables(
            name = name,
            importables = self.importables,
            package = self.package)
        self.importables[name] = imported
        return imported


@dataclasses.dataclass
class Delayed:
    """Mixin that converts str attributes to imported items when accessed.

    # Only str values of attributes with a `.` in them are assumed to be import
    # paths.

    After an item is imported, it is assigned to the attribute which previously
    held the str import path so that it does not need to be reloaded.

    """

    """ Dunder Methods """

    def __getattribute__(self, name: str) -> Any:
        item = super().__getattribute__(name)
        if not isinstance(item, str):
            return item
        imported = from_import_path(item = name)
        super().__setattr__(name, imported)
        return imported

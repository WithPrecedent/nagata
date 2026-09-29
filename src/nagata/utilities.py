"""Shared tools.

Contents:


To Do:


"""
from __future__ import annotations

import inspect
import pathlib
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

    from . import base

def _cleave_str(
    item: str, /,
    divider: str = '_', *,
    return_last: bool = True,
    raise_error: bool = False) -> tuple[str, str]:
    """Divides 'item' into 2 parts based on 'divider'.

    Args:
        item: item to be divided.
        divider: item to divide 'item' upon.
        return_last: whether to split 'item' upon the first (False) or
            last appearance of 'divider'.
        raise_error: whether to raise an error if 'divider' is not in
            'item' or to return a tuple containing 'item' twice.

    Raises:
        ValueError: if 'divider' is not in 'item' and 'raise_error' is True.

    Returns:
        tuple[str, str]: parts of 'item' on either side of 'divider' unless
            'divider' is not in 'item'.

    """
    if divider in item:
        if return_last:
            suffix = item.split(divider)[-1]
        else:
            suffix = item.split(divider)[0]
        prefix = item[:-len(suffix) - 1]
    elif raise_error:
        raise ValueError(f'{divider} is not in {item}')
    else:
        prefix = suffix = item
    return prefix, suffix

def _drop_privates(item: base.GenericDict, /) -> base.GenericList:
    """Drops items in 'item' with names beginning with an underscore.

    Args:
        item: list-like object with str items or
            names that might have underscores at their beginnings.

    Returns:
        list-like object with items dropped if
            they or their names begin with an underscore.

    Raises:
        TypeError: if 'item' does not contain str types or objects with either
            'name' or '__name__' attributes.

    """
    base = type(item)
    if len(item) > 0 and all(isinstance(i, str) for i in item):
        return base([i for i in item if not i.startswith('_')])
    elif len(item) > 0 and all(hasattr(i, 'name') for i in item):
        return base([i for i in item if not i.name.startswith('_')])
    elif len(item) > 0 and all(hasattr(i, '__name__') for i in item):
        return base([i for i in item if not i.__name__.startswith('_')])
    elif len == 0:
        return item
    else:
        raise TypeError(
            'items in item must be str types or have name or __name__ '
            'attributes')

def _iterify(item: Any) -> Iterable:
    """Returns `item` as an iterable, but does not iterate str types.

    Args:
        item: item to turn into an iterable

    Returns:
        Iterable of `item`. A `str` type will be stored as a single item in an
            Iterable wrapper.

    """
    if item is None:
        return iter(())
    elif isinstance(item, str | bytes):
        return iter([item])
    else:
        try:
            return iter(item)
        except TypeError:
            return iter((item,))

def _name_attributes(
    item: Any,
    include_private: bool = False) -> list[str]:
    """Returns attribute names of 'item'.

    Args:
        item: item to examine.
        include_private: whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        list[str]: names of attributes in 'item'.

    """
    names = dir(item)
    if not include_private:
        names = _drop_privates(names)
    return names

def _namify(item: Any, /, default: str | None = None) -> str | None:
    """Returns `str` name representation of `item`.

    Args:
        item: item to determine a `str` name for.
        default: default name to return if a name cannot be created.

    Returns:
        A name representation of `item.`

    """
    if isinstance(item, str):
        return item
    elif (
        hasattr(item, 'name')
        and not inspect.isclass(item)
        and isinstance(item.name, str)):
        return item.name
    else:
        try:
            return _snakify(item.__name__)
        except AttributeError:
            if item.__class__.__name__ is not None:
                return _snakify(item.__class__.__name__)
            else:
                return default

def _pathlibify(item: str | pathlib.Path) -> pathlib.Path:
    """Converts string `path` to pathlib.Path object.

    Args:
        item: either a string of a path or a pathlib.Path object.

    Raises:
        TypeError if `path` is neither a str or pathlib.Path type.

    Returns:
        pathlib.Path object.

    """
    if isinstance(item, str):
        return pathlib.Path(item)
    elif isinstance(item, pathlib.Path):
        return item
    else:
        raise TypeError('item must be str or pathlib.Path type')

def _snakify(item: str) -> str:
    """Converts a capitalized `str` to snake case.

    Args:
        item: `str` to convert.

    Returns:
        `item` converted to snake case.

    """
    item = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()

def _typify(item: str) -> list[Any] | int | float | bool | str:
    """Converts stings to appropriate, supported datatypes.

    The method converts strings to list (if ', ' is present), int, float,
    or bool datatypes based upon the content of the string. If no
    alternative datatype is found, the item is returned in its original
    form.

    Args:
        item: string to be converted to appropriate datatype.

    Returns:
        Converted item.

    """
    if not isinstance(item, str):
        return item
    try:
        return int(item)
    except ValueError:
        try:
            return float(item)
        except ValueError:
            if item.lower() in {'true', 'yes'}:
                return True
            elif item.lower() in {'false', 'no'}:
                return False
            elif ', ' in item:
                item = item.split(', ')
                return [_typify(i) for i in item]
            else:
                return item

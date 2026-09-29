"""Descriptors for attributes.

Contents:

To Do:


"""
from __future__ import annotations

import abc
import pathlib
from typing import Any

from . import utilities


class Descriptor:
    """Descriptor base class.

    The core code of this class is adapted from the official Python HOWTOs:
    https://docs.python.org/3/howto/descriptor.html

    Unlike the class in the Python docs, this one stores additional attributes
    for use by subclasses that do more than very basic type validation. It
    also can store a default value or default callable if there is no stored
    value.

    Attributes:
        attribute_name: name of the validator attribute in `owner`.
        default: default value to use if no value is set.
        private_name: `attribute_name` with a leading underscore added.

    """

    """ Initialization Methods """

    def __init__(self, *, default: Any):
        """Initializes class instance.

        Args:
            default: default value to use if no value is set.

        """
        self.default = self.validate(default, self)

    """ Required Subclass Methods """

    @abc.abstractmethod
    def validate(
        self,
        item: str | pathlib.Path,
        owner: object | None = None) -> pathlib.Path:
        """Returns a validated `item`.

        Args:
            item: object to validate.
            owner: object to which the descriptor is an attribute.

        Returns:
            Validated object.

        """
        folder = utilities._pathlibify(item)
        pathlib.Path.mkdir(folder, parents = True, exist_ok = True)
        return folder

    """ Dunder Methods """

    def __get__(
        self,
        owner: object,
        objtype: type[Any] | None = None) -> pathlib.Path:
        """Returns item stored in `private_name`.

        Args:
            owner: object of which this validator is an attribute.
            objtype: class of `owner`. Defaults to None.

        Returns:
            Stored item.

        """
        try:
            return getattr(owner, self.private_name)
        except AttributeError:
            return self.default

    def __set__(self, owner: object, value: Any) -> None:
        """Stores `value` in attribute named `private_name` of `owner`.

        Args:
            owner: object of which this validator is an attribute.
            value: item to store, after being validated.

        """
        validated = self.validate(item = value, owner = owner)
        setattr(owner, self.private_name, validated)
        return

    def __set_name__(self, owner: object, name: str) -> None:
        """Sets `attribute_name` and `private_name`.

        Args:
            owner: object of which this validator is an attribute.
            name: name of this attribute in `owner`.

        """
        self.attribute_name = name
        self.private_name = f'_{name}'
        return


class Folder(Descriptor):
    """Descriptor for folder attributes.

    Attributes:
        attribute_name: name of the validator attribute in `owner`.
        default: default value to use if no value is set.
        private_name: `attribute_name` with a leading underscore added.

    """

    """ Instance Methods """

    def validate(
        self,
        item: str | pathlib.Path,
        owner: object | None = None) -> pathlib.Path:  # noqa: ARG002
        """Returns a validated `item`.

        Args:
            item: object to validate.
            owner: object to which the descriptor is an attribute.

        Returns:
            Validated object.

        """
        folder = utilities._pathlibify(item)
        pathlib.Path.mkdir(folder, parents = True, exist_ok = True)
        return folder


class SubFolder(Folder):
    """Descriptor for subfolder attributes.

    Attributes:
        attribute_name: name of the validator attribute in `owner`.
        default: default value to use if no value is set.
        private_name: `attribute_name` with a leading underscore added.

    """

    """ Instance Methods """

    def validate(
        self,
        item: str | pathlib.Path,
        owner: object | None = None) -> pathlib.Path:
        """Returns a validated `item`.

        Args:
            item: object to validate.
            owner: object to which the descriptor is an attribute.

        Returns:
            Validated object.

        """
        if isinstance(item, pathlib.Path):
            path = item
        elif isinstance(item, str) and '/' not in item:
            attribute = getattr(owner, f'{item}_folder')
            try:
                path = getattr(owner, attribute)
            except AttributeError:
                path = owner.root_folder.joinpath(path)
        return super().validate(path, owner)

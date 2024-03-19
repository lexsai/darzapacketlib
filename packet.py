"""This module contains a class to represent a packet."""

from abc import ABC, abstractmethod

import os
from importlib import util
from importlib.machinery import ModuleSpec
from importlib.abc import Loader
from types import ModuleType
from typing import TypeVar, Generic

PacketTypeT = TypeVar('PacketTypeT', bound='Packet')

class Packet(ABC, Generic[PacketTypeT]):
    """Class representing a packet."""

    packet_id = -1

    id_to_class: dict[id, PacketTypeT] = {}
    class_to_id: dict[PacketTypeT, id] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.id_to_class[cls.packet_id] = cls
        cls.class_to_id[cls] = cls.packet_id

    @abstractmethod
    def to_raw_bytes(self):
        """Return the raw bytes that would comprise this packet."""

    @classmethod
    @abstractmethod
    def from_bytes(cls, raw_bytes):
        """Instantiate a packet class from the raw bytes of a packet."""

    @classmethod
    @abstractmethod
    def from_params(cls):
        """Instantiate a packet class from the paramters of a packet."""

dirpath = os.path.dirname(os.path.abspath(__file__))

def load_module(path: str) -> ModuleType:
    """
    Load a python module from the filepath.
    """
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)

    assert isinstance(spec, ModuleSpec)

    module = util.module_from_spec(spec)

    assert isinstance(spec.loader, Loader)

    spec.loader.exec_module(module)
    return module

for fname in os.listdir(os.path.join(dirpath, 'client')):
    if not fname.startswith('__') and fname.endswith('.py'):
        load_module(os.path.join(dirpath, 'client', fname))

for fname in os.listdir(os.path.join(dirpath, 'server')):
    if not fname.startswith('__') and fname.endswith('.py'):
        load_module(os.path.join(dirpath, 'server', fname))

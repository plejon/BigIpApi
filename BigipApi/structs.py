from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Node:
    name: str
    partition: str
    address: str


@dataclass
class Pool:
    name: str
    partition: str
    monitor: str


@dataclass
class CreateDataGroup:
    name: str
    partition: str
    type: str
    records = List[Dict]

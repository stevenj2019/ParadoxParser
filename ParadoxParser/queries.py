from collections.abc import Iterator
from typing import Protocol

from ParadoxParser.ParadoxNodes import GenericBlock, GenericKeyValue


class NodeContainer(Protocol):
    nodes: list

def find_block(block:NodeContainer, match_id:str) -> GenericBlock|None:
    return next((node for node in block.nodes if isinstance(node, GenericBlock) and node.key == match_id), None)

def find_blocks(block:NodeContainer, match_id:str) -> list[GenericBlock]:
    return [node for node in block.nodes if isinstance(node, GenericBlock) and node.key == match_id]

def find_keyvalue(block:NodeContainer, match_id:str) -> GenericBlock|None:
    return next((node for node in block.nodes if isinstance(node, GenericKeyValue) and node.key == match_id), None)

def all_blocks(block:NodeContainer, match_id:str|None = None) -> Iterator[GenericBlock]:
    for node in block.nodes:
        if not isinstance(node, GenericBlock):
            continue
        if match_id is None or node.key == match_id:
            yield node

def all_keyvalues(block:NodeContainer, match_id:str|None = None) -> Iterator[GenericKeyValue]:
    for node in block.nodes:
        if not isinstance(node, GenericKeyValue):
            continue
        if match_id is None or node.key == match_id:
            yield node
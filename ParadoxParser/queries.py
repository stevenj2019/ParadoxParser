from collections.abc import Iterator
from typing import Protocol

from ParadoxParser.ParadoxNodes import (
    GenericBlock,
    GenericKeyValue,
    GenericLegacyLocKey,
    GenericLocKey,
    GenericNode,
)


class NodeContainer(Protocol):
    nodes: list

KEYED_NODE_TYPES = (GenericBlock, GenericKeyValue)
LOCALISATION_NODE_TYPES = (GenericLegacyLocKey, GenericLocKey)

def _matches_node(node: GenericNode, match_str:str) -> bool:
    if isinstance(node, KEYED_NODE_TYPES):
        return node.key == match_str
    return node.value == match_str

def find_node(block:NodeContainer, node_type:type[GenericNode], match_str:str) -> GenericNode | None:
    return next((node for node in block.nodes if isinstance(node, node_type) and _matches_node(node_type, match_str)), None)

def find_nodes(block:NodeContainer, node_type:type[GenericNode], match_str:str) -> list[GenericNode]:
    return [node for node in block.nodes if isinstance(node, node_type) and _matches_node(node_type, match_str)]

def all_nodes(block:NodeContainer, node_type:type[GenericNode], match_str:str) -> Iterator[GenericNode]:
    for node in block.nodes:
        if isinstance(node, node_type) and _matches_node(node, match_str):
            yield node
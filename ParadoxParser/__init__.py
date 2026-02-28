import os, re
from pathlib import Path
import shutil
from .ParadoxNodes import ( GenericNode, GenericKeyValue, 
                            GenericBlock, GenericLogic, GenericFlow, 
                            GenericTrigger, GenericList,
                            GenericFloat, GenericInt, GenericString,
                            GenericBool, GenericToken, GenericComment,
                            GenericComparator)
from .constants import (LOGIC_FLOW_KEYS, LOGIC_KEYS, TRIGGER_KEYS)

class ParadoxScriptParser:
    def __init__(self, path: os.PathLike|str, encoding: str = "UTF-8"):
        self.filepath = Path(path)
        self.filename = self.filepath.name
        self.encoding = encoding
        self.nodes: list[GenericNode] = []
        self._parse_file()

    # ==========================================================
    # FILE LOADING
    # ==========================================================
    def _parse_file(self):
        with open(self.filepath, "r", encoding=self.encoding) as f:
            text = f.read()

        self.tokens = self._tokenize(text)
        self.pos = 0
        self.nodes = self._parse_scope()

    # ==========================================================
    # TOKENIZER
    # ==========================================================
    def _tokenize(self, text: str) -> list[str]:
        """
        Tokenize Paradox script text.
        Handles:
        - key="value with spaces"
        - quoted strings
        - comments (# kept as tokens)
        - braces and operators
        - IDs with dots like arg.1
        """
        token_pattern = r'''
            "[^"\\]*(?:\\.[^"\\]*)*"      |   # quoted strings
            \#.*                           |   # comments (entire rest of line)
            [{}=<>]                         |   # braces and operators
            [a-zA-Z0-9_.]+                  |   # bare words/keys with dots
            \S                               # any other single char
        '''
        return re.findall(token_pattern, text, re.VERBOSE)

    def _peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _next(self):
        token = self._peek()
        self.pos += 1
        return token

    # ==========================================================
    # CORE PARSER
    # ==========================================================
    def _parse_scope(self) -> list[GenericNode]:
        nodes = []
        while self.pos < len(self.tokens):
            token = self._peek()

            if token == "}":
                self._next()
                break
            if token == "{":
                self._next()
                continue

            nodes.append(self._parse_statement())

        return nodes

    def _parse_statement(self) -> GenericNode:
        key = self._next()

        # COMMENT HANDLING
        if key.startswith("#"):
            return GenericComment(key)

        # KEY=VALUE or KEY { BLOCK }
        if self._peek() == "=":
            self._next()  # consume "="
            next_token = self._peek()

            # BLOCK
            if next_token == "{":
                self._next()
                children = self._parse_scope()
                if all(isinstance(c, GenericToken) for c in children):
                    block = GenericList(key)
                else:
                    if key in TRIGGER_KEYS:
                        block = GenericTrigger(key)
                    elif key in LOGIC_KEYS:
                        block = GenericLogic(key)
                    elif key in LOGIC_FLOW_KEYS:
                        block = GenericFlow(key)
                    else:
                        block = GenericBlock(key)
                block.children = children
                return block
            # SIMPLE KEY VALUE
            else:
                value_token = self._next()
                value_node = self._parse_value(value_token)
                return GenericKeyValue(key, value_node)

        # COMPARATOR
        if self._peek() in ["<", ">"]:
            operator = self._next()
            value = self._next()
            return GenericComparator(key, operator, value)

        # BARE TOKEN FALLBACK
        return self._parse_value(key)

    # ==========================================================
    # VALUE PARSER
    # ==========================================================
    def _parse_value(self, token: str) -> GenericNode:
        if token.startswith('"') and token.endswith('"'):
            return GenericString(token)
        if token.lower() == "yes":
            return GenericBool(True)
        if token.lower() == "no":
            return GenericBool(False)
        if re.fullmatch(r"-?\d+", token):
            return GenericInt(int(token))
        if re.fullmatch(r"-?\d+\.\d+", token):
            return GenericFloat(float(token))
        if token.startswith("#"):
            return GenericComment(token)
        return GenericToken(token)

    # ==========================================================
    # DEBUG TREE PRINTER
    # ==========================================================

    def print_tree(self, nodes=None, indent=0):
        if nodes is None:
            nodes = self.nodes

        for node in nodes:
            prefix = "    " * indent

            if isinstance(node, GenericList):
                values = ", ".join(str(c.value) for c in node.children)
                print(f"{prefix}List: {node.key} [{values}]")

            elif isinstance(node, GenericBlock):
                print(f"{prefix}Block: {node.key} ({len(node.children)} children)")
                self.print_tree(node.children, indent + 1)

            elif isinstance(node, GenericKeyValue):
                print(f"{prefix}KV: {node.key} = {node.value.value}")

            else:
                print(f"{prefix}Token: {node.value}")

    def _backup_file(self):
        shutil.copyfile(self.filepath, self.filepath.with_suffix(self.filepath.suffix + ".bak"))

    
    def _to_pdx_script_file(self):
        output = ""
        for node in self.nodes:
            output += node._to_string_literal(indent=0)

        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(output)
    #     with open(self.filepath, "r+") as FILE:
    #         FILE.write(self.root_template.render( pdx_file = self,
    #                                               isinstance=isinstance,
    #                                               GenericNode=GenericNode,
    #                                               GenericBlock=GenericBlock,
    #                                               GenericKeyValue=GenericKeyValue))

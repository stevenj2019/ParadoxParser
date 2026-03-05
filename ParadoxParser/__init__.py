import os, re
from pathlib import Path
import shutil
from .ParadoxNodes import ( GenericNode, GenericKeyValue, 
                            GenericBlock, GenericLogic, GenericFlow, 
                            GenericTrigger, GenericList,
                            GenericFloat, GenericInt, GenericString,
                            GenericBool, GenericToken, GenericComment,
                            GenericComparator, GenericLocKey)
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
        # Step 1: Basic tokenization (works for most cases)
        basic_tokens = re.findall(r'"(?:\\.|[^"\\])*"|#.*|\{|\}|[^\s{}]+', text)

        # Step 2: Post-process tokens that have glued special characters
        final_tokens = []
        for token in basic_tokens:
            # Skip comments and quoted strings
            if token.startswith('"') or token.startswith('#'):
                final_tokens.append(token)
                continue

            # Split token on =, <, > but keep them
            split_tokens = re.split(r'([=<>])', token)
            final_tokens.extend([t for t in split_tokens if t])  # remove empty strings

        return final_tokens

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

    def _backup_file(self):
        shutil.copyfile(self.filepath, self.filepath.with_suffix(self.filepath.suffix + ".bak"))

    def _to_pdx_file(self):
        output = ""
        for node in self.nodes:
            output += node._to_string_literal(indent=0)

        with open(self.filepath, "w", encoding=self.encoding) as f:
            f.write(output)

#Parse a single Paradox loc file (*.yml)
class ParadoxLocParser:
    def __init__(self, path:os.PathLike|str, encoding:str="utf-8-sig"):
        self.filepath = Path(path)
        self.filename = self.filepath.name
        self.encoding = encoding
        self.language_key:str = ""
        self.nodes: list[GenericNode] = []
        self._parse_file()

    def _parse_file(self):
        """Parse Paradox localization file into nodes preserving comments."""
        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                
                if stripped.startswith("l_"):
                    self.language_key = stripped.split(":")[0]

                # Preserve comments as GenericComment
                if stripped.startswith("#"):
                    self.nodes.append(GenericComment(stripped))
                    continue

                # Skip headers
                if stripped.endswith(":") and not '"' in stripped:
                    continue

                # Try to parse loc key
                match = re.compile(r'^\s*([A-Za-z0-9_.-]+):(?:(\d+))?\s*(?:"([^"]*)")?').match(stripped)
                if match:
                    key, num, value = match.groups()
                    num = int(num) if num is not None else 0

                    # preserve quotes if present
                    quote_match = re.search(r'"(.*)"', line)
                    if quote_match:
                        value = quote_match.group(1)
                    else:
                        value = value or ""

                    self.nodes.append(GenericLocKey(key, num, value))

    def _to_pdx_file(self):
        output = f"l_{self.language_key}:"

        for node in self.nodes:
            output += node._to_string_literal(indent=0)

        with open(self.filepath, "w", encoding=self.encoding) as f:
            f.write(output)
import os, re, jinja2
from ParadoxNodes import (GenericNode, GenericKeyValue, GenericBlock,
                          GenericLogic, GenericFlow, GenericTrigger, 
                          GenericList,
                          GenericFloat, GenericInt, GenericString,
                          GenericBool, GenericToken, 
                          GenericComparator)
from constants import (LOGIC_FLOW_KEYS, LOGIC_KEYS, TRIGGER_KEYS)

#Parse a single Paradox script file (*.txt/*.gfx/*.gui(though idk why you would))
class ParadoxScriptParser:
    def __init__(self, path: os.PathLike, encoding: str = "UTF-8"):
        self.filepath = path
        _, self.filename = path.split()
        self.encoding = encoding
        self.nodes: list[GenericNode] = []
        self.jinja_env = jinja2.Environment(loader=jinja2.PackageLoader("templates/"))
        self._parse_file()

    # ==========================================================
    # FILE LOADING
    # ==========================================================

    def _parse_file(self):
        with open(self.filepath, "r", encoding=self.encoding) as f:
            text = f.read()

        # Remove comments
        text = re.sub(r"#.*", "", text)

        # Tokenize
        self.tokens = self._tokenize(text)
        self.pos = 0

        # Parse root scope
        self.nodes = self._parse_scope()

    # ==========================================================
    # TOKENIZER
    # ==========================================================

    def _tokenize(self, text: str) -> list[str]:
        """
        Order matters:
        - Quoted strings first (atomic)
        - Braces
        - Equals
        - Everything else as non-whitespace sequences
        """
        pattern = r'"(?:\\.|[^"\\])*"|\{|\}|=|>|<|\S+'
        return re.findall(pattern, text)

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
                self._next()  # consume
                break

            if token == "{":
                self._next()  # consume stray open brace
                continue

            nodes.append(self._parse_statement())

        return nodes

    def _parse_statement(self) -> GenericNode:
        key = self._next()

        # If next token is "=" we have a key-value or block
        if self._peek() == "=":
            self._next()  # consume "="
            next_token = self._peek()

            # BLOCK
            if next_token == "{":
                self._next()  # consume "{"
                children = self._parse_scope()

                # Determine block type
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
            
        ###comparator
        if self._peek() in ["<", ">"]:
            operator = self._next() 
            value = self._next()
            return GenericComparator(key, operator, value)
        
        # Bare token fallback (used inside lists)
        return self._parse_value(key)

    # ==========================================================
    # VALUE PARSER
    # ==========================================================

    def _parse_value(self, token: str) -> GenericNode:
        # Strings are atomic — never parsed internally
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
        #TODO just copy the self.filename to self.filename.replace(".txt", ".bak")
        return
    
    def _write_file(self):
        self._backup_file()
        return jinja2.render_template(self.jinja_env.get_template("PDXScript.txt.jinja"), 
                                      object = self)

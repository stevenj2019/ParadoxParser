###          ###
# BASE CLASSES #
###          ###
class GenericLocKey:
    def __init__(self, key:str, value:str) -> None:
        self.key = key
        self.value = str(value)

    def _get_value(self)->str|int|float|bool:
        return self.value

    def _to_string_literal(self, indent: int = 0) -> str:
        return f"  {self.key}: \"{self.value}\"\n"
    
class GenericLegacyLocKey:
    def __init__(self, key:str, num:str, value:str) -> None:
        self.key = key
        self.num = int(num)
        self.value = str(value)

    def _get_value(self)->str|int|float|bool:
        return self.value

    def _to_string_literal(self, indent: int = 0) -> str:
        return f"  {self.key}:{self.num} \"{self.value}\"\n"
    
class GenericNode:
    def __init__(self, value:str|float|bool) -> None:
        self.value = value

    def _get_value(self)->str|int|float|bool:
        return self.value
    
    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}{self._get_value()}\n"
    
class GenericKeyValue(GenericNode):
    def __init__(self, key: str, value:GenericNode) -> None:
        self.key = key
        self.value = value
    
    def _get_value(self)->str:
        return f"{self.key} = {self.value.get_value}"

    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}{self.key} = {self.value._to_string_literal()}"
    
    def _get_key_val(self) -> tuple[str, str]:
        return self.key, self.value
    
class GenericBlock(GenericNode):
    def __init__(self, key:str, nodes:list|None=None) -> None:
        if nodes is None:
            nodes = []
        self.key = key
        self.nodes:list[GenericNode] = []
        if nodes:
            self.nodes.extend(nodes)
    # ==========================================================
    # Recursive Traversal
    # ==========================================================
    def traverse(self, callback, include_self=True) -> None:
        """
        Recursively traverse self and all nodes.
        - callback: a function that takes a node and can modify it.
        - include_self: if True, applies callback to this node first.
        """
        if include_self:
            callback(self)
        
        for child in self.nodes:
            callback(child)
            if isinstance(child, GenericBlock):
                child.traverse(callback, include_self=False)

    # CRUD helpers
    def add_child(self, child: GenericNode) -> None:
        self.nodes.append(child)

    def remove_child(self, child: GenericNode) -> None:
        if child in self.nodes:
            self.nodes.remove(child)

    def update_child(self, old_child: GenericNode, new_child: GenericNode) -> None:
        for i, c in enumerate(self.nodes):
            if c is old_child:
                self.nodes[i] = new_child
                break

    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent

        output = f"{tabs}{self.key} = {{\n"

        for child in self.nodes:
            output += child._to_string_literal(indent + 1)

        output += f"{tabs}}}\n"
        return output

###                    ###
# FLAVOUR CLASSES - NODE # - There is every chance these can be deleted, will check when i have the frontend running ig?
###                    ###
class GenericInt(GenericNode):
    def __init__(self, value: int) -> None:
        super().__init__(value)

class GenericFloat(GenericNode):
    def __init__(self, value: float) -> None:
        super().__init__(value)

class GenericString(GenericNode):
    def __init__(self, value: str) -> None:
        self.value = value.replace("\"", "")

    def _to_string_literal(self, indent = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}\"{self._get_value()}\"\n"
    
class GenericToken(GenericNode):
    def __init__(self, value: str) -> None:
        super().__init__(value)

###                       ###
# SPECIALIST CLASSES - NODE #
###                       ###
class GenericComment(GenericNode):
    def __init__(self, value:str) -> None:
        super().__init__(value)
    
    def _to_string_literal(self, indent:int = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}{self._get_value()}\n"
    
class GenericBool(GenericNode):
    def __init__(self, value: bool) -> None:
        self.value = value

    def _get_value(self)->str:
        return "yes" if self.value else "no"
    
    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}{self._get_value()}\n"

class GenericComparator(GenericNode):
    def __init__(self, left:str, operator:str, right:str) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def _get_value(self)->str:
        return f"{self.left} {self.operator} {self.right}" 

###                       ###
# SPCIALIST CLASSES - BLOCK #
###                       ###
class GenericTrigger(GenericBlock):
    def __init__(self, key: str) -> None:
        super().__init__(key)

class GenericLogic(GenericBlock):
    def __init__(self, key: str) -> None:
        super().__init__(key)
    
class GenericFlow(GenericBlock):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        
class GenericList(GenericBlock):
    def __init__(self, key: str) -> None:
        super().__init__(key)
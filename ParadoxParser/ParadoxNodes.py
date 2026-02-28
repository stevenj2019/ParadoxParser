###          ###
# BASE CLASSES #
###          ###
class GenericNode:
    def __init__(self, value:str|int|float|bool):
        self.value = value

    def _get_value(self)->str|int|float|bool:
        return self.value
    
    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}{self._get_value()}\n"
    
class GenericKeyValue(GenericNode):
    def __init__(self, key: str, value:GenericNode):
        self.key = key
        self.value = value
    
    def _get_value(self)->str:
        return f"{self.key} = {self.value.get_value}"

    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}{self.key} = {self.value._get_value()}\n"
    
class GenericBlock(GenericNode):
    def __init__(self, key: str = None):
        self.key = key
        self.children:list[GenericNode] = []

    # ==========================================================
    # Recursive Traversal
    # ==========================================================
    def traverse(self, callback, include_self=True):
        """
        Recursively traverse self and all children.
        - callback: a function that takes a node and can modify it.
        - include_self: if True, applies callback to this node first.
        """
        if include_self:
            callback(self)
        
        for child in self.children:
            callback(child)
            if isinstance(child, GenericBlock):
                child.traverse(callback, include_self=False)

    # CRUD helpers
    def add_child(self, child: GenericNode):
        self.children.append(child)

    def remove_child(self, child: GenericNode):
        if child in self.children:
            self.children.remove(child)

    def update_child(self, old_child: GenericNode, new_child: GenericNode):
        for i, c in enumerate(self.children):
            if c is old_child:
                self.children[i] = new_child
                break

    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent

        output = f"{tabs}{self.key} = {{\n"

        for child in self.children:
            output += child._to_string_literal(indent + 1)

        output += f"{tabs}}}\n"
        return output

###                    ###
# FLAVOUR CLASSES - NODE # - There is every chance these can be deleted, will check when i have the frontend running ig?
###                    ###
class GenericInt(GenericNode):
    def __init__(self, value: int):
        super().__init__(value)

class GenericFloat(GenericNode):
    def __init__(self, value: float):
        super().__init__(value)

class GenericString(GenericNode):
    def __init__(self, value: str):
        super().__init__(value)

class GenericToken(GenericNode):
    def __init__(self, value: str):
        super().__init__(value)

###                      ###
# SPCIALIST CLASSES - NODE #
###                      ###
class GenericComment(GenericNode):
    def __init__(self, value:str):
        super().__init__(value)

class GenericBool(GenericNode):
    def __init__(self, value: bool):
        self.value = value

    def _get_value(self)->str:
        return "yes" if self.value else "no"
    
    def _to_string_literal(self, indent: int = 0) -> str:
        tabs = "\t" * indent
        return f"{tabs}{self._get_value()}\n"

class GenericComparator(GenericNode):
    def __init__(self, left:str, operator:str, right:str):
        self.left = left
        self.operator = operator
        self.right = right

    def _get_value(self)->str:
        return f"{self.left} {self.operator} {self.right}" 

###                       ###
# SPCIALIST CLASSES - BLOCK #
###                       ###
class GenericTrigger(GenericBlock):
    def __init__(self, key: str = None):
        super().__init__(key)

class GenericLogic(GenericBlock):
    def __init__(self, key: str = None):
        super().__init__(key)
    
class GenericFlow(GenericBlock):
    def __init__(self, key: str = None):
        super().__init__(key)
        
class GenericList(GenericBlock):
    def __init__(self, key: str = None):
        super().__init__(key)
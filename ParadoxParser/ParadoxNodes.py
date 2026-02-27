###          ###
# BASE CLASSES #
###          ###
class GenericNode:
    def __init__(self, value:str|int|float|bool):
        self.value = value

    def _get_value(self)->str|int|float|bool:
        return self.value
    
class GenericKeyValue(GenericNode):
    def __init__(self, key: str, value:GenericNode):
        self.key = key
        self.value = value
    
    def _get_value(self)->str:
        return f"{self.key} = {self.value.get_value}"

class GenericBlock(GenericNode):
    def __init__(self, key: str = None):
        self.key = key
        self.children:list[GenericNode] = []

    def _get_value(self)->dict[str, GenericNode]:
        return {self.key: self.children}

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
class GenericBool(GenericNode):
    def __init__(self, value: bool):
        self.value = value

    def _get_value(self)->str:
        return "yes" if self.value else "no"

class GenericComparator(GenericNode):
    def __init__(self, left:str, operator:str, right:str):
        self.left = left
        self.operator = operator
        self.right = right

    def _get_value(self)->str:
        return "{self.left} {self.operator} {self.right}"
    
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
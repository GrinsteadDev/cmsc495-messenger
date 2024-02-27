"""
Purpose:
    Banter Box Web Application Setting Module common_objs.py
    This modules is designed to store object types that get reused through the app. This
    allows us to avoid errors where modules depend on each other when using type hints
Change Log:
    Created by Devin Grinstead :
        
Contributors:
    Devin Grinstead
Methods:
    * No Methods
Objects:
    class UpperMatchList(list)
        Extends the list object to make it uppercase only
"""
from fnmatch import fnmatch

class UpperMatchList(list):
    """
    Creates an UpperCase only str list object
    """
    def __init__(self, iterable = []):
        """"""
        super().__init__([str(item).upper() for item in iterable])

    def __setitem__(self, index, item):
        """"""
        super().__setitem__(index, str(item).upper())

    def insert(self, index, item):
        """"""
        super().insert(index, str(item).upper())

    def append(self, item):
        """"""
        super().append(str(item).upper())
    
    def pattern_match(self, item_pattern: str) -> bool:
        """
        Uses basic pattern matching to determin if an item is in the list
        """
        vOut = False

        if isinstance(item_pattern, str):
            vOut = any([True if fnmatch(x, item_pattern.upper()) else False for x in self])

        return vOut
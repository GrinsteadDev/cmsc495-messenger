from typing import Collection
from fnmatch import fnmatch

file_blacklist = [
    "base.html",
    "head.html"
]

def match_file_blacklist(name) -> bool:
    vOut = False
    
    if isinstance(name, str):
        vOut = any([True if fnmatch(x, name) else False for x in file_blacklist])
    
    return vOut

if __name__ == "__main__":
    isTrue = match_file_blacklist("base.*")
    
    isFalse = match_file_blacklist("base")
    
    isFalse = match_file_blacklist("fff")
    
    f = ""
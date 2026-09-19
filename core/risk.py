from enum import IntEnum
class Risk(IntEnum):
    READ_ONLY=0; LOW=1; NORMAL=2; ELEVATED=3; HIGH=4; CRITICAL=5; DESTRUCTIVE=6; IRREVERSIBLE=7

def classify(resource:str, production:bool, scope:int=1, reduces_access:bool=False, changes_indexability:bool=False):
    if not production: return Risk.NORMAL
    if resource=="robots_txt" and reduces_access: return Risk.CRITICAL
    if changes_indexability: return Risk.CRITICAL if scope >= 10 else Risk.HIGH
    if resource in {"canonical","redirect","hreflang","sitemap_generator"} and scope >= 10: return Risk.HIGH
    if resource=="gbp": return Risk.HIGH
    return Risk.ELEVATED

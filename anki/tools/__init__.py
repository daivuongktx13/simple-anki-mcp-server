from . import anki

__all__ = ["register"]

def register(mcp):
    for mod in (anki, ):
        if hasattr(mod, "register"):
            mod.register(mcp)
    return mcp
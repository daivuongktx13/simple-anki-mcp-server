from . import anki

__all__ = ["register_resources"]

def register_resources(mcp):
    for mod in (anki, ):
        if hasattr(mod, "register_resources"):
            mod.register_resources(mcp)
    return mcp
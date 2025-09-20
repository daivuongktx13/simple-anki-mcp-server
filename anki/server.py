from fastmcp import FastMCP
from .logger import logger
from . import tools as tools_pkg
from . import resources as resources_pkg
# Import each submodule and attach the MCP instance so decorators bind correctly
def build_server(name: str = "fastmcp-modular") -> FastMCP:
    mcp = FastMCP(name)

    # Register all tools/resources/prompts via their module-level register() hooks
    tools_pkg.register(mcp)
    resources_pkg.register_resources(mcp)

    logger.info("Server '%s' initialized", name)
    return mcp

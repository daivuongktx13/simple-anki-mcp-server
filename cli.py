from anki.server import build_server

mcp = build_server()

if __name__ == "__main__":
    # stdio transport so MCP clients can spawn this process
    mcp.run()
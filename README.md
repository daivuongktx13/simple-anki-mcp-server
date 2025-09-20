# 📝 A Simple Anki MCP Server 

🚀 My Custom MCP server that provides minimal tool to connect to Anki through AnkiConnect.

## ⚙️ MCP Server

### 🔧 Tools
- anki_create_deck: Create a new deck
- anki_note_exists: Check if a note exists in a deck
- anki_add_note: Add a note to an existing deck (word, meaning)

### 📚 Resources
- anki://decks - List of available decks

## Run and Visualize

### Enviroment Setup
I use `uv`, a very fast Python package manager.
```
uv sync
```

### 🔍 MCP Inspector
We can inspect the MCP Server at dev environment using:
```
npx @modelcontextprotocol/inspector
```
Run Command:
```
fastmcp run cli.py (stdio) or uv run cli.py
```

## 🙏 Acknowledgements

Special thanks to these awesome projects and authors:
- [nailuoGG/anki-mcp-server](https://github.com/nailuoGG/anki-mcp-server)
- [kitschpatrol/yanki-connect](https://github.com/kitschpatrol/yanki-connect)
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
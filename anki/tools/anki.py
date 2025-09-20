# tools/anki.py
from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP

from ..models import (
    CreateDeckOutput,
    GetDecksOutput,
    AddNoteOutput,
)
from ..anki_client import AnkiError, client


def register(m: FastMCP):
    
    # @m.tool
    # async def anki_get_decks() -> GetDecksOutput:
    #     """List all deck names."""
    #     decks = await client.deck_names()
    #     return GetDecksOutput(decks=decks)

    @m.tool
    async def anki_create_deck(
        name: Annotated[str, Field(description="Deck name to create")]
    ) -> CreateDeckOutput:
        """Create a new deck."""
        deck_id = await client.create_deck(name)
        return CreateDeckOutput(deck_id=deck_id)

    @m.tool
    async def anki_note_exists(
        word: Annotated[str, Field(description="Word to check existence")],
        deck: Annotated[str, Field(description="Deck to check existence")],
    ) -> bool:
        """Return True if any note matches the query (word) for example 禁じる or 信念."""
        query = f"Deck:{deck} Front:{word}"
        ids = await client.find_notes(query)
        return len(ids) > 0

    @m.tool
    async def anki_add_note(
        deckName: str,
        word: str,
        meaning: Annotated[str, Field(description="Word meaning and usage example")],
    ) -> AddNoteOutput:
        """
        Add a note to Anki.
        Handles duplicate gracefully (returns duplicate=True).
        """
        fields = {
            "Front": word,
            "Back": meaning
        }
        try:
            note_id = await client.add_note(
                deckName=deckName,
                fields=fields
            )
            return AddNoteOutput(note_id=note_id, duplicate=False, message="ok")
        except AnkiError as e:
            msg = str(e)
            if "duplicate" in msg.lower():
                return AddNoteOutput(note_id=None, duplicate=True, message=msg)
            elif "deck" in msg.lower():
                return AddNoteOutput(note_id=None, duplicate=False, message=msg)
            raise  # let MCP surface other errors
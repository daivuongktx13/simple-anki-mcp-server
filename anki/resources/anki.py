# resources/anki_decks.py
from fastmcp import FastMCP

from ..models import (
    GetDecksOutput,
)

from ..anki_client import client


def register_resources(m: FastMCP):

    @m.resource(
        uri="anki://decks",
        name="Anki Decks",
        description="List all Anki deck names",
        mime_type="application/json"
    )
    async def resource_decks():
        decks = await client.deck_names()
        return GetDecksOutput(decks=decks)
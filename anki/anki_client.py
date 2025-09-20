# anki_client.py
from __future__ import annotations
import os
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel

from .config import settings

class AnkiError(RuntimeError):
    pass

class AnkiConnectClient:
    """
    Async client cho AnkiConnect. Dễ mở rộng bằng cách thêm methods wrap 'invoke'.
    """
    def __init__(
        self,
        base_url: str | None = None,
        api_key: Optional[str] = None,
        timeout: float = 10.0,
        client: Optional[httpx.AsyncClient] = None,
    ):
        self.base_url = base_url or os.getenv("ANKI_URL", "http://127.0.0.1:8765")
        self.api_key = api_key if api_key is not None else os.getenv("ANKI_KEY") or None
        self.timeout = timeout if timeout is not None else float(os.getenv("ANKI_TIMEOUT", "10"))
        self._client = client

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["anki-connect-key"] = self.api_key
        return h

    async def invoke(self, action: str, params: Optional[Dict[str, Any]] = None, version: int = 6) -> Any:
        payload = {"action": action, "version": version, "params": params or {}}
        client = await self._get_client()
        r = await client.post(self.base_url, json=payload, headers=self._headers())
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            raise AnkiError(str(data["error"]))
        return data.get("result")

    # ---------- Typed helpers ----------
    async def deck_names(self) -> List[str]:
        return await self.invoke("deckNames")

    async def create_deck(self, deck: str) -> int:
        return await self.invoke("createDeck", {"deck": deck})

    async def find_notes(self, query: str) -> List[int]:
        return await self.invoke("findNotes", {"query": query})

    async def add_note(
        self,
        deckName: str,
        fields: Dict[str, str],
        tags: Optional[List[str]] = None,
        options: Optional[Dict[str, Any]] = None,
        modelName: str = "Basic",
    ) -> int:
        note = {
            "deckName": deckName,
            "modelName": modelName,
            "fields": fields,
            "options": options or {"allowDuplicate": False, "duplicateScope": "deck"},
        }
        if tags:
            note["tags"] = tags
        return await self.invoke("addNote", {"note": note})

    async def aclose(self):
        if self._client is not None:
            await self._client.aclose()

    async def __aenter__(self) -> "AnkiConnectClient":
        await self._get_client()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

client = AnkiConnectClient(
    base_url=settings.anki_base_url,
    api_key=settings.anki_api_key,
    timeout=settings.anki_timeout,
)
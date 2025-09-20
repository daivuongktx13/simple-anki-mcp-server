# models.py
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field

# --------- Generic wire models (nếu muốn tái dụng) ----------
class AnkiBaseRequest(BaseModel):
    action: str
    version: int = 6
    params: Dict = Field(default_factory=dict)

class AnkiBaseResponse(BaseModel):
    result: Optional[object] = None
    error: Optional[str] = None

# --------- Typed inputs/outputs cho tools ----------
class CreateDeckOutput(BaseModel):
    deck_id: int

class GetDecksOutput(BaseModel):
    decks: List[str]

class AddNoteOutput(BaseModel):
    note_id: Optional[int] = None
    duplicate: bool = False
    message: str = "ok"
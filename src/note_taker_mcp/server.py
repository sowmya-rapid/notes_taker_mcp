import uuid
from typing import Dict, List
from mcp.server.fastmcp import Context, FastMCP
from smithery.decorators import smithery

# In-memory store (OK for demo)
NOTES: Dict[str, dict] = {}


@smithery.server()
def create_server():
    """
    Smithery factory function.
    DO NOT call .run() here.
    """
    mcp = FastMCP("Note Taker MCP")

    @mcp.tool()
    def create_note(
        title: str,
        content: str,
        ctx: Context,
        tags: List[str] | None = None,
    ) -> dict:
        """Create a new note."""
        note_id = str(uuid.uuid4())
        NOTES[note_id] = {
            "note_id": note_id,
            "title": title,
            "content": content,
            "tags": tags or [],
        }
        return {"status": "created", "note_id": note_id}

    @mcp.tool()
    def append_note(note_id: str, content: str, ctx: Context) -> dict:
        """Append text to an existing note."""
        if note_id not in NOTES:
            return {"error": "Note not found"}
        NOTES[note_id]["content"] += "\n" + content
        return {"status": "updated", "note_id": note_id}

    @mcp.tool()
    def get_note(note_id: str, ctx: Context) -> dict:
        """Retrieve a note."""
        return NOTES.get(note_id, {"error": "Note not found"})

    @mcp.tool()
    def search_notes(query: str, ctx: Context) -> list:
        """Search notes."""
        q = query.lower()
        return [
            note for note in NOTES.values()
            if q in note["title"].lower() or q in note["content"].lower()
        ]

    return mcp

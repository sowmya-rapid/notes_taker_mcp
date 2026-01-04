# note_taker_mcp_server.py

from mcp.server.fastmcp import FastMCP
import uuid
from typing import Dict, List

mcp = FastMCP("Note Taker MCP")

# In-memory store
NOTES: Dict[str, dict] = {}


@mcp.tool()
def create_note(
    title: str,
    content: str,
    tags: List[str] = [],
) -> dict:
    note_id = str(uuid.uuid4())

    NOTES[note_id] = {
        "note_id": note_id,
        "title": title,
        "content": content,
        "tags": tags,
    }

    return {
        "status": "created",
        "note_id": note_id,
    }


@mcp.tool()
def append_note(
    note_id: str,
    content: str,
) -> dict:
    if note_id not in NOTES:
        return {"error": "Note not found"}

    NOTES[note_id]["content"] += "\n" + content

    return {
        "status": "updated",
        "note_id": note_id,
    }


@mcp.tool()
def get_note(note_id: str) -> dict:
    if note_id not in NOTES:
        return {"error": "Note not found"}

    return NOTES[note_id]


@mcp.tool()
def search_notes(query: str) -> list:
    results = []

    for note in NOTES.values():
        if query.lower() in note["title"].lower() or query.lower() in note["content"].lower():
            results.append(note)

    return results


if __name__ == "__main__":
    mcp.run()

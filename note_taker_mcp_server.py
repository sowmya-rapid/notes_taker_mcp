from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery
import uuid
from typing import Dict, List

# In-memory storage
NOTES: Dict[str, dict] = {}

@smithery.server()
def create_server():
    """Factory function that Smithery uses to start your server."""
    mcp = FastMCP("Note Taker MCP")

    @mcp.tool()
    def create_note(title: str, content: str, tags: List[str] = []) -> dict:
        note_id = str(uuid.uuid4())
        NOTES[note_id] = {
            "note_id": note_id,
            "title": title,
            "content": content,
            "tags": tags,
        }
        return {"status": "created", "note_id": note_id}

    @mcp.tool()
    def append_note(note_id: str, content: str) -> dict:
        if note_id not in NOTES:
            return {"error": "Note not found"}
        NOTES[note_id]["content"] += "\n" + content
        return {"status": "updated", "note_id": note_id}

    @mcp.tool()
    def get_note(note_id: str) -> dict:
        return NOTES.get(note_id, {"error": "Note not found"})

    @mcp.tool()
    def search_notes(query: str) -> list:
        return [
            note for note in NOTES.values()
            if query.lower() in note["title"].lower()
            or query.lower() in note["content"].lower()
        ]

    return mcp

# Keep this for local testing, but Smithery will ignore it
def main():
    server = create_server()
    server.run()

if __name__ == "__main__":
    main()
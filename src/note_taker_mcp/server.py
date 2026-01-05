import uuid
from typing import Dict, List
from mcp.server.fastmcp import Context, FastMCP
from smithery.decorators import smithery

# Global storage for the demo
NOTES: Dict[str, dict] = {}

@smithery.server()
def create_server():
    """
    Smithery factory function. 
    The decorator 'enhances' FastMCP for production deployment.
    """
    # Create the FastMCP instance
    mcp = FastMCP("Note Taker MCP")

    @mcp.tool()
    def create_note(title: str, content: str, ctx: Context, tags: List[str] = []) -> dict:
        """Create a new note. The 'ctx' argument is required by Smithery."""
        note_id = str(uuid.uuid4())
        NOTES[note_id] = {
            "note_id": note_id,
            "title": title,
            "content": content,
            "tags": tags,
        }
        return {"status": "created", "note_id": note_id}

    @mcp.tool()
    def append_note(note_id: str, content: str, ctx: Context) -> dict:
        """Add text to an existing note."""
        if note_id not in NOTES:
            return {"error": "Note not found"}
        NOTES[note_id]["content"] += "\n" + content
        return {"status": "updated", "note_id": note_id}

    @mcp.tool()
    def get_note(note_id: str, ctx: Context) -> dict:
        """Retrieve a note by its unique ID."""
        return NOTES.get(note_id, {"error": "Note not found"})

    @mcp.tool()
    def search_notes(query: str, ctx: Context) -> list:
        """Search notes by title or content."""
        return [
            note for note in NOTES.values()
            if query.lower() in note["title"].lower()
            or query.lower() in note["content"].lower()
        ]

    return mcp

if __name__ == "__main__":
    # This allows 'uv run dev' to work locally
    server = create_server()
    server.run()
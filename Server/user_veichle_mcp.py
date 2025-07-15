from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("UserVehicleData")

# Load your JSON data
import json
with open("D://PROJECTS//Simple_file_db_MCP_SERVER//Server//db.json") as f:
    db = json.load(f)



# Example additional utility (optional)
@mcp.tool()
def user_by_email(email: str):
    """Get user info by email"""
    for user in db["users"]:
        if user["email"].lower() == email.lower():
            return user
    return None

# Expose the entire db.json as a resource
@mcp.resource("db://full_db")
def get_full_db() -> dict:
    """Returns the full db.json content (users and vehicles)"""
    return db

@mcp.tool()
def get_db_json() -> dict:
    """Returns the db.json content as a JSON object dictionary for clients like Claude, using the db://full_db resource as the source."""
    return get_full_db()

@mcp.tool()
def update_db_json(new_data: dict) -> str:
    """Update or add data in db.json. Accepts a dict with 'users' and/or 'vehicles' keys. Updates in-memory db and writes to file."""
    updated = False
    if 'users' in new_data:
        db['users'] = new_data['users']
        updated = True
    if 'vehicles' in new_data:
        db['vehicles'] = new_data['vehicles']
        updated = True
    if updated:
        with open("D://PROJECTS//Simple_file_db_MCP_SERVER//Server//db.json", "w") as f:
            json.dump(db, f, indent=4)
        return "db.json updated successfully."
    else:
        return "No valid keys provided. Use 'users' and/or 'vehicles'."


if __name__ == "__main__":
    mcp.run()

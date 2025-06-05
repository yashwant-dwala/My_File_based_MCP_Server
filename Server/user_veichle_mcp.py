from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("UserVehicleData")

# Load your JSON data
import json
with open("D://PROJECTS//Simple_file_db_MCP_SERVER//Server//db.json") as f:
    db = json.load(f)

# Expose the entire dataset as a resource
@mcp.resource("db://user_vehicle_data")
def get_data() -> dict:
    """Returns the full user and vehicle data"""
    return db

@mcp.resource("db://user_vehicle_data/{uid}")
def get_user_by_id(uid: str) -> dict:
    """Returns a perticulatar entry from user data based on the id provided"""
    return next((user for user in db["users"] if user["id"] == uid), None)

@mcp.resource("db://user_vehicle_data/{uid}")
def get_user_by_id(uid: str) -> dict:
    """Returns a perticulatar entry from Vehicle data based on the id provided"""
    return next((Vehicle for Vehicle in db["vehicles"] if Vehicle["id"] == uid), None)


# Example additional utility (optional)
@mcp.tool()
def user_by_email(email: str):
    """Get user info by email"""
    for user in db["users"]:
        if user["email"].lower() == email.lower():
            return user
    return None

if __name__ == "__main__":
    mcp.run()

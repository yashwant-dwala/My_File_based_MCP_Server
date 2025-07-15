from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("UserVehicleData")

# Load your JSON data
import json
with open("D://PROJECTS//Simple_file_db_MCP_SERVER//Server//db.json") as f:
    db = json.load(f)

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
def update_db_json(update_dict: dict) -> str:
    """
    Update, add, or delete top-level keys in db.json.
    - To update/add: provide {key: value}.
    - To delete: provide {key: None}.
    Updates in-memory db and writes to file.
    """
    changed = False
    for key, value in update_dict.items():
        if value is None:
            if key in db:
                del db[key]
                changed = True
        else:
            db[key] = value
            changed = True
    if changed:
        with open("D://PROJECTS//Simple_file_db_MCP_SERVER//Server//db.json", "w") as f:
            json.dump(db, f, indent=4)
        return "db.json updated successfully."
    else:
        return "No changes made. Provide at least one key to add/update or delete."




# # MySQL setup
# import mysql.connector
# MYSQL_CONFIG = {
#     'host': 'localhost',
#     'user': 'your_mysql_user',
#     'password': 'your_mysql_password',
#     'database': 'your_database_name',
# }

# @mcp.tool()
# def get_mysql_database_json() -> dict:
#     """
#     Fetches all tables and their data from the MySQL database, returning a dict of {table_name: [rows]}.
#     """
#     conn = mysql.connector.connect(**MYSQL_CONFIG)
#     cursor = conn.cursor()
#     cursor.execute("SHOW TABLES")
#     tables = [row[0] for row in cursor.fetchall()]
#     db_data = {}
#     for table in tables:
#         cur2 = conn.cursor(dictionary=True)
#         cur2.execute(f"SELECT * FROM `{table}`")
#         db_data[table] = cur2.fetchall()
#         cur2.close()
#     cursor.close()
#     conn.close()
#     return db_data

# @mcp.tool()
# def update_mysql_database_json(update_dict: dict) -> str:
#     """
#     Update/add/delete data in any table of the MySQL database.
#     - To replace all rows in a table: provide {table_name: [row_dicts]}.
#     - To delete all rows: provide {table_name: None} or {table_name: []}.
#     Handles foreign key constraints (e.g., ON DELETE CASCADE) by deleting child tables first.
#     """
#     conn = mysql.connector.connect(**MYSQL_CONFIG)
#     cursor = conn.cursor()
#     # Get all tables and their foreign key dependencies
#     cursor.execute("SELECT TABLE_NAME, REFERENCED_TABLE_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL", (MYSQL_CONFIG['database'],))
#     fk_map = {}
#     for table, ref_table in cursor.fetchall():
#         fk_map.setdefault(ref_table, set()).add(table)
#     # Topological sort to delete child tables first
#     def get_delete_order(tables):
#         visited = set()
#         order = []
#         def visit(t):
#             if t not in visited:
#                 visited.add(t)
#                 for child in fk_map.get(t, []):
#                     visit(child)
#                 order.append(t)
#         for t in tables:
#             visit(t)
#         return order[::-1]  # children first
#     # Deletions
#     to_delete = [k for k, v in update_dict.items() if v is None or v == []]
#     delete_order = get_delete_order(to_delete)
#     for table in delete_order:
#         cursor.execute(f"DELETE FROM `{table}`")
#     # Insert/replace
#     for table, rows in update_dict.items():
#         if rows is not None and rows != []:
#             cursor.execute(f"DELETE FROM `{table}`")
#             for row in rows:
#                 columns = ','.join(f'`{col}`' for col in row.keys())
#                 placeholders = ','.join(['%s'] * len(row))
#                 sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
#                 cursor.execute(sql, tuple(row.values()))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return "MySQL database updated successfully."


if __name__ == "__main__":
    mcp.run()

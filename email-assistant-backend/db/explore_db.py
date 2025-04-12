import sqlite3

# Connect to the database
conn = sqlite3.connect("emails.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables found in the database:")
for table in tables:
    print(f"- {table[0]}")

# For each table, show schema and data
for table_name in tables:
    table_name = table_name[0]
    print(f"\n=== Table: {table_name} ===")

    # Show schema
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    print("Schema:")
    for column in schema:
        print(f"  {column[1]} ({column[2]})")

    # Show data
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    if rows:
        print("Data:")
        for row in rows:
            print(row)
    else:
        print("No data in this table.")

# Close connection
conn.close()
print("\n✅ Done exploring database.")

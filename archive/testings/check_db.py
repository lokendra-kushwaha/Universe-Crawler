import sqlite3

# Connect to the database
conn = sqlite3.connect("universe_search.db")
cursor = conn.cursor()

tables = ['DocumentStore', 'InvertedIndex', 'WebGraph', 'PageRankScores']

print("🔍 DATABASE CHECKING...\n" + "="*30)
for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"✅ Table '{table}': {count} rows saved.")
    except Exception as e:
        print(f"❌ Error in '{table}': {e}")

conn.close()
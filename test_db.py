import os
import sys

HOST = os.environ.get("DB_HOST", "localhost")
USER = os.environ.get("DB_USER", "root")
PASS = os.environ.get("DB_PASSWORD", "")
DB = os.environ.get("DB_NAME", "blog")
PORT = int(os.environ.get("DB_PORT", 3306))

print(f"[TEST] host={HOST}")
print(f"[TEST] user={USER}")
print(f"[TEST] db={DB}")
print(f"[TEST] port={PORT}")
print(f"[TEST] password_len={len(PASS)}")
print()

# Test pymysql
print("--- Test: pymysql ---")
try:
    import pymysql
    c = pymysql.connect(
        host=HOST, user=USER, password=PASS, database=DB, port=PORT,
        charset="utf8mb4",
    )
    print("OK")
    c.close()
except Exception as e:
    print(f"FAIL: {e}")

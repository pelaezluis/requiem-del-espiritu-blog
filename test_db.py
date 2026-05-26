import os
import sys
from mysql import connector

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

# Test 1: with auth_plugin + use_pure
print("--- Test 1: use_pure=True, auth_plugin=mysql_native_password ---")
try:
    c = connector.connect(
        host=HOST, user=USER, password=PASS, database=DB, port=PORT,
        charset="utf8mb4", use_unicode=True,
        use_pure=True, auth_plugin="mysql_native_password",
    )
    print("OK")
    c.close()
except Exception as e:
    print(f"FAIL: {e}")

print()

# Test 2: default settings
print("--- Test 2: default settings ---")
try:
    c = connector.connect(
        host=HOST, user=USER, password=PASS, database=DB, port=PORT,
        charset="utf8mb4", use_unicode=True,
    )
    print("OK")
    c.close()
except Exception as e:
    print(f"FAIL: {e}")

print()

# Test 3: with use_pure only
print("--- Test 3: use_pure=True only ---")
try:
    c = connector.connect(
        host=HOST, user=USER, password=PASS, database=DB, port=PORT,
        charset="utf8mb4", use_unicode=True,
        use_pure=True,
    )
    print("OK")
    c.close()
except Exception as e:
    print(f"FAIL: {e}")

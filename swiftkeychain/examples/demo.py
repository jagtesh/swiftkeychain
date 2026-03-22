#!/usr/bin/env python3
"""SwiftKeychain — Example Usage

Demonstrates macOS Keychain access from Python via ApplePy.
"""
import swiftkeychain as kc

# ── Generic Passwords ──────────────────────────────────────

print("=== Generic Passwords ===\n")

# Store a password
kc.set_password("myapp", "user@example.com", "s3cret-p@ss!")
print("✓ Stored password for user@example.com")

# Store another
kc.set_password("myapp", "admin@example.com", "4dm1n-p@ss!")
print("✓ Stored password for admin@example.com")

# Retrieve it
pw = kc.get_password("myapp", "user@example.com")
print(f"✓ Retrieved password: {pw}")

# List all accounts for a service
accounts = kc.find_passwords("myapp")
print(f"✓ Accounts for 'myapp': {accounts}")

# Delete one
deleted = kc.delete_password("myapp", "admin@example.com")
print(f"✓ Deleted admin account: {deleted}")

# Verify it's gone
pw = kc.get_password("myapp", "admin@example.com")
print(f"✓ admin password after delete: {pw}")  # Should be None

# Clean up
kc.delete_password("myapp", "user@example.com")

# ── Internet Passwords ─────────────────────────────────────

print("\n=== Internet Passwords ===\n")

# Store an internet password
kc.set_internet_password("api.example.com", "bot-user", "t0k3n-xyz", "https", "/v1")
print("✓ Stored internet password for api.example.com")

# Retrieve it
pw = kc.get_internet_password("api.example.com", "bot-user")
print(f"✓ Retrieved internet password: {pw}")

# Clean up
kc.delete_password("api.example.com", "bot-user")

# ── Error Handling ──────────────────────────────────────────

print("\n=== Error Handling ===\n")

# get_password returns None for missing items (no exception)
result = kc.get_password("nonexistent-service", "nobody")
print(f"✓ Missing password returns: {result}")  # None

print("\n🎉 All examples passed!")

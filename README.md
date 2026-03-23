# SwiftKeychain

macOS Keychain access from Python — powered by Swift & [ApplePy](../ApplePy).

> **macOS only** — requires Swift 6.0+ toolchain

## Install

```bash
pip install -e .
```

This compiles the embedded Swift code and installs the Python package.

## Usage

```python
import swiftkeychain as kc

# Store & retrieve passwords
kc.set_password("myapp", "user@email.com", "s3cret")
pw = kc.get_password("myapp", "user@email.com")

# List all accounts for a service
accounts = kc.find_passwords("myapp")

# Internet passwords
kc.set_internet_password("api.example.com", "bot", "token", "https", "/v1")
pw = kc.get_internet_password("api.example.com", "bot")

# Delete
kc.delete_password("myapp", "user@email.com")
```

## API

| Function | Returns | Description |
|----------|---------|-------------|
| `set_password(service, account, password)` | `None` | Store a generic password |
| `get_password(service, account)` | `str \| None` | Retrieve a password |
| `delete_password(service, account)` | `bool` | Delete a password |
| `find_passwords(service)` | `list[str]` | List accounts for a service |
| `set_internet_password(server, account, password, protocol, path)` | `None` | Store an internet password |
| `get_internet_password(server, account)` | `str \| None` | Retrieve an internet password |

## CLI

SwiftKeychain includes a command-line tool `skc` for quick Keychain operations:

```bash
# Store a password (prompts if password omitted)
skc set myapp user@email.com s3cret

# Retrieve a password
skc get myapp user@email.com

# Retrieve password only (for scripting)
skc get myapp user@email.com -q

# Find all accounts for a service
skc find myapp

# Delete a password
skc delete myapp user@email.com

# Internet passwords
skc set-internet api.example.com bot token123
skc get-internet api.example.com bot
```

| Command | Description |
|---------|-------------|
| `skc set <service> <account> [password]` | Store a password (prompts if omitted) |
| `skc get <service> <account> [-q]` | Retrieve a password (`-q` for raw output) |
| `skc delete <service> <account>` | Delete a password |
| `skc find <service>` | List all accounts for a service |
| `skc set-internet <server> <account> [password]` | Store an internet password |
| `skc get-internet <server> <account> [-q]` | Retrieve an internet password |

## Examples

See [`swiftkeychain/examples/demo.py`](swiftkeychain/examples/demo.py) for a full demo.

## License

BSD-3-Clause © Jagtesh Chadha — see [LICENSE](LICENSE).

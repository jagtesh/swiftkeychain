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

## Examples

See [`swiftkeychain/examples/demo.py`](swiftkeychain/examples/demo.py) for a full demo.

## License

BSD-3-Clause © Jagtesh Chadha — see [LICENSE](LICENSE).

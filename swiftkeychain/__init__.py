"""swiftkeychain — macOS Keychain access from Python

Powered by Swift & ApplePy. Wraps the macOS Security framework directly,
no pyobjc or subprocess needed.

Usage:
    import swiftkeychain as kc
    kc.set_password("myapp", "user@email.com", "s3cret")
    pw = kc.get_password("myapp", "user@email.com")
"""
import importlib
import os
import sys

if sys.platform != "darwin":
    raise ImportError("swiftkeychain only supports macOS")


def _load_native():
    """Load the compiled Swift extension module."""
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    so_path = os.path.join(pkg_dir, "swiftkeychain.so")

    if not os.path.exists(so_path):
        raise ImportError(
            "Native extension not found. Build it first:\n"
            "  pip install -e .\n"
            "  # or: python setup.py build_ext --inplace"
        )

    spec = importlib.util.spec_from_file_location("swiftkeychain", so_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_native = _load_native()

# Re-export all public functions
set_password = _native.set_password
get_password = _native.get_password
delete_password = _native.delete_password
find_passwords = _native.find_passwords
set_internet_password = _native.set_internet_password
get_internet_password = _native.get_internet_password

__all__ = [
    "set_password",
    "get_password",
    "delete_password",
    "find_passwords",
    "set_internet_password",
    "get_internet_password",
]

__version__ = "0.1.0"

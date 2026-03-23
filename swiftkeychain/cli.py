"""skc — SwiftKeychain CLI

A command-line interface for macOS Keychain operations.

Usage:
    skc set <service> <account> <password>
    skc get <service> <account>
    skc delete <service> <account>
    skc find <service>
    skc set-internet <server> <account> <password>
    skc get-internet <server> <account>
"""
import argparse
import sys
import getpass

import swiftkeychain as kc


def cmd_set(args):
    """Store a password in the Keychain."""
    password = args.password or getpass.getpass("Password: ")
    kc.set_password(args.service, args.account, password)
    print(f"✅ Stored password for {args.account}@{args.service}")


def cmd_get(args):
    """Retrieve a password from the Keychain."""
    pw = kc.get_password(args.service, args.account)
    if pw is None:
        print(f"❌ No password found for {args.account}@{args.service}", file=sys.stderr)
        sys.exit(1)
    if args.quiet:
        print(pw)
    else:
        print(f"🔑 {args.account}@{args.service}: {pw}")


def cmd_delete(args):
    """Delete a password from the Keychain."""
    result = kc.delete_password(args.service, args.account)
    if result:
        print(f"🗑  Deleted password for {args.account}@{args.service}")
    else:
        print(f"❌ No password found for {args.account}@{args.service}", file=sys.stderr)
        sys.exit(1)


def cmd_find(args):
    """Find all passwords for a service."""
    results = kc.find_passwords(args.service)
    if not results:
        print(f"❌ No passwords found for service '{args.service}'", file=sys.stderr)
        sys.exit(1)
    print(f"🔍 Found {len(results)} password(s) for '{args.service}':\n")
    for entry in results:
        if isinstance(entry, dict):
            account = entry.get("account", "unknown")
            print(f"  • {account}")
        else:
            print(f"  • {entry}")


def cmd_set_internet(args):
    """Store an internet password in the Keychain."""
    password = args.password or getpass.getpass("Password: ")
    kc.set_internet_password(args.server, args.account, password)
    print(f"✅ Stored internet password for {args.account}@{args.server}")


def cmd_get_internet(args):
    """Retrieve an internet password from the Keychain."""
    pw = kc.get_internet_password(args.server, args.account)
    if pw is None:
        print(f"❌ No internet password found for {args.account}@{args.server}", file=sys.stderr)
        sys.exit(1)
    if args.quiet:
        print(pw)
    else:
        print(f"🔑 {args.account}@{args.server}: {pw}")


def main():
    parser = argparse.ArgumentParser(
        prog="skc",
        description="SwiftKeychain CLI — macOS Keychain from the command line",
        epilog="Powered by Swift & ApplePy",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {kc.__version__}")

    sub = parser.add_subparsers(dest="command", required=True, metavar="command")

    # skc set
    p = sub.add_parser("set", help="Store a password")
    p.add_argument("service", help="Service name (e.g., 'myapp')")
    p.add_argument("account", help="Account name (e.g., 'user@email.com')")
    p.add_argument("password", nargs="?", help="Password (prompted if omitted)")
    p.set_defaults(func=cmd_set)

    # skc get
    p = sub.add_parser("get", help="Retrieve a password")
    p.add_argument("service", help="Service name")
    p.add_argument("account", help="Account name")
    p.add_argument("-q", "--quiet", action="store_true", help="Output only the password (for scripting)")
    p.set_defaults(func=cmd_get)

    # skc delete
    p = sub.add_parser("delete", help="Delete a password")
    p.add_argument("service", help="Service name")
    p.add_argument("account", help="Account name")
    p.set_defaults(func=cmd_delete)

    # skc find
    p = sub.add_parser("find", help="Find all passwords for a service")
    p.add_argument("service", help="Service name to search for")
    p.set_defaults(func=cmd_find)

    # skc set-internet
    p = sub.add_parser("set-internet", help="Store an internet password")
    p.add_argument("server", help="Server hostname (e.g., 'github.com')")
    p.add_argument("account", help="Account name")
    p.add_argument("password", nargs="?", help="Password (prompted if omitted)")
    p.set_defaults(func=cmd_set_internet)

    # skc get-internet
    p = sub.add_parser("get-internet", help="Retrieve an internet password")
    p.add_argument("server", help="Server hostname")
    p.add_argument("account", help="Account name")
    p.add_argument("-q", "--quiet", action="store_true", help="Output only the password")
    p.set_defaults(func=cmd_get_internet)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

// SwiftKeychain — macOS Keychain access from Python
// A showcase example for ApplePy.
//
// Usage from Python:
//   import swiftkeychain as kc
//   kc.set_password("myapp", "user@email.com", "s3cret")
//   pw = kc.get_password("myapp", "user@email.com")

import ApplePy
import Foundation
import Security
@preconcurrency import ApplePyFFI

// MARK: - Custom Exception

let KeychainError = PyExceptionType(name: "swiftkeychain.KeychainError", doc: "Keychain operation failed")

// MARK: - Helpers

/// Convert an OSStatus from the Security framework to a human-readable message.
func keychainErrorMessage(_ status: OSStatus) -> String {
    if let msg = SecCopyErrorMessageString(status, nil) {
        return msg as String
    }
    return "Keychain error (OSStatus \(status))"
}

// MARK: - set_password

/// Store a generic password in the macOS Keychain.
@PyFunction
func set_password(service: String, account: String, password: String) throws {
    let data = password.data(using: .utf8)!

    let query: NSDictionary = [
        kSecClass: kSecClassGenericPassword,
        kSecAttrService: service,
        kSecAttrAccount: account,
        kSecValueData: data,
    ]

    // Delete existing item first (upsert pattern)
    SecItemDelete(query)

    let status = SecItemAdd(query, nil)
    if status != errSecSuccess {
        throw KeychainBridgeError.operationFailed(keychainErrorMessage(status))
    }
}

// MARK: - get_password

/// Retrieve a generic password from the macOS Keychain.
/// Returns None if the item doesn't exist.
@PyFunction
func get_password(service: String, account: String) throws -> String? {
    let query: NSDictionary = [
        kSecClass: kSecClassGenericPassword,
        kSecAttrService: service,
        kSecAttrAccount: account,
        kSecReturnData: true,
        kSecMatchLimit: kSecMatchLimitOne,
    ]

    var result: AnyObject?
    let status = SecItemCopyMatching(query, &result)

    if status == errSecItemNotFound {
        return nil
    }
    if status != errSecSuccess {
        throw KeychainBridgeError.operationFailed(keychainErrorMessage(status))
    }

    guard let data = result as? Data else { return nil }
    return String(data: data, encoding: .utf8)
}

// MARK: - delete_password

/// Delete a generic password from the macOS Keychain.
/// Returns True if deleted, False if not found.
@PyFunction
func delete_password(service: String, account: String) -> Bool {
    let query: NSDictionary = [
        kSecClass: kSecClassGenericPassword,
        kSecAttrService: service,
        kSecAttrAccount: account,
    ]

    let status = SecItemDelete(query)
    return status == errSecSuccess
}

// MARK: - find_passwords

/// Find all accounts for a given service.
/// Returns a list of account names.
@PyFunction
func find_passwords(service: String) throws -> [String] {
    let query: NSDictionary = [
        kSecClass: kSecClassGenericPassword,
        kSecAttrService: service,
        kSecReturnAttributes: true,
        kSecMatchLimit: kSecMatchLimitAll,
    ]

    var result: AnyObject?
    let status = SecItemCopyMatching(query, &result)

    if status == errSecItemNotFound {
        return []
    }
    if status != errSecSuccess {
        throw KeychainBridgeError.operationFailed(keychainErrorMessage(status))
    }

    guard let items = result as? [[String: Any]] else { return [] }
    return items.compactMap { $0[kSecAttrAccount as String] as? String }
}

// MARK: - set_internet_password

/// Store an internet password in the macOS Keychain.
@PyFunction
func set_internet_password(server: String, account: String, password: String, protocol_: String = "https", path: String = "/") throws {
    let data = password.data(using: .utf8)!

    let dict = NSMutableDictionary()
    dict[kSecClass] = kSecClassInternetPassword
    dict[kSecAttrServer] = server
    dict[kSecAttrAccount] = account
    dict[kSecAttrPath] = path
    dict[kSecValueData] = data

    if let proto = protocolFromString(protocol_) {
        dict[kSecAttrProtocol] = proto
    }

    // Delete existing item first
    let deleteDict = dict.mutableCopy() as! NSMutableDictionary
    deleteDict.removeObject(forKey: kSecValueData)
    SecItemDelete(deleteDict)

    let status = SecItemAdd(dict, nil)
    if status != errSecSuccess {
        throw KeychainBridgeError.operationFailed(keychainErrorMessage(status))
    }
}

// MARK: - get_internet_password

/// Retrieve an internet password from the macOS Keychain.
@PyFunction
func get_internet_password(server: String, account: String) throws -> String? {
    let query: NSDictionary = [
        kSecClass: kSecClassInternetPassword,
        kSecAttrServer: server,
        kSecAttrAccount: account,
        kSecReturnData: true,
        kSecMatchLimit: kSecMatchLimitOne,
    ]

    var result: AnyObject?
    let status = SecItemCopyMatching(query, &result)

    if status == errSecItemNotFound {
        return nil
    }
    if status != errSecSuccess {
        throw KeychainBridgeError.operationFailed(keychainErrorMessage(status))
    }

    guard let data = result as? Data else { return nil }
    return String(data: data, encoding: .utf8)
}

// MARK: - Internal Error Type

enum KeychainBridgeError: Error, PyExceptionMapping {
    case operationFailed(String)

    var pythonExceptionType: PyExceptionType { KeychainError }
    var pythonMessage: String {
        switch self {
        case .operationFailed(let msg): return msg
        }
    }
}

// MARK: - Protocol mapping helper

func protocolFromString(_ str: String) -> CFString? {
    switch str.lowercased() {
    case "https": return kSecAttrProtocolHTTPS
    case "http": return kSecAttrProtocolHTTP
    case "ftp": return kSecAttrProtocolFTP
    case "ssh": return kSecAttrProtocolSSH
    default: return nil
    }
}

// MARK: - Module Entry Point

@PyModule("swiftkeychain", functions: [
    set_password,
    get_password,
    delete_password,
    find_passwords,
    set_internet_password,
    get_internet_password,
])
func swiftkeychain() {}

// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "SwiftKeychain",
    platforms: [.macOS(.v13)],
    products: [
        .library(name: "SwiftKeychain", type: .dynamic, targets: ["SwiftKeychain"]),
    ],
    dependencies: [
        .package(url: "https://github.com/jagtesh/ApplePy.git", from: "1.0.0"),
    ],
    targets: [
        .target(
            name: "SwiftKeychain",
            dependencies: [
                .product(name: "ApplePy", package: "ApplePy"),
                .product(name: "ApplePyClient", package: "ApplePy"),
            ],
            linkerSettings: [
                .linkedFramework("Security"),
            ]
        ),
    ]
)

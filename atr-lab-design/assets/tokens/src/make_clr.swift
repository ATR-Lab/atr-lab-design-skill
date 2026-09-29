// Build palette.clr (macOS NSColorList) from palette.gpl. Usage: swift make_clr.swift <palette.gpl> <out.clr>
import AppKit
let args = CommandLine.arguments
guard args.count == 3 else { print("usage: swift make_clr.swift palette.gpl out.clr"); exit(2) }
let text = try String(contentsOfFile: args[1], encoding: .utf8)
let list = NSColorList(name: "ATR Lab")
var n = 0
for line in text.split(separator: "\n") {
    let s = line.trimmingCharacters(in: .whitespaces)
    if s.isEmpty || s.hasPrefix("#") || s.hasPrefix("GIMP") || s.hasPrefix("Name:") || s.hasPrefix("Columns:") { continue }
    let parts = s.split(separator: "\t", maxSplits: 1)
    guard parts.count == 2 else { continue }
    let rgb = parts[0].split(separator: " ").compactMap { Double($0) }
    guard rgb.count == 3 else { continue }
    let c = NSColor(srgbRed: rgb[0] / 255, green: rgb[1] / 255, blue: rgb[2] / 255, alpha: 1)
    list.setColor(c, forKey: String(parts[1]))
    n += 1
}
try list.write(to: URL(fileURLWithPath: args[2]))
// verify by reading back
guard let back = NSColorList(name: "check", fromFile: args[2]) else { print("readback failed"); exit(1) }
print("palette.clr: wrote \(n) colors, read back \(back.allKeys.count)")

#!/usr/bin/env lua

-- Add current directory to path for local requires
package.path = package.path .. ";scripts/lua/?.lua;./?.lua"
local C = require("ansi-colors")

print(C.bold .. C.accent .. "ANSI Colors Library Demo" .. C.reset)
print(string.rep("-", 30))

-- 1. Showcase basic colors
print(C.colorize(C.green,  "This is Green (Success)"))
print(C.colorize(C.yellow, "This is Yellow (Warning)"))
print(C.colorize(C.blue,   "This is Blue (Info)"))
print(C.colorize(C.cyan,   "This is Cyan (Process)"))
print(C.colorize(C.accent, "This is the Theme Accent (Muted Green)"))

print("")

-- 2. Showcase text styles
print(C.bold .. "This text is BOLD" .. C.reset)
print(C.dim .. "This text is DIM" .. C.reset)
print(C.italic .. "This text is ITALIC" .. C.reset)

print("")

-- 3. Showcase combination of styles
print(C.bold .. C.yellow .. "BOLD YELLOW WARNING!" .. C.reset)
print(C.dim .. C.italic .. "Dim and Italicized note..." .. C.reset)
print(C.bold .. C.accent .. "Bold Theme Accent" .. C.reset)

print("")

-- 4. Using the helper function for inline styling
local message = "System status: " .. C.colorize(C.bold .. C.green, "OPERATIONAL")
print(message)

print(string.rep("-", 30))
print(C.dim .. "Demo complete." .. C.reset)

#!/usr/bin/env lua

-- Armagdon Prep - Lua Version of Status Dashboard
-- Highlights Lua's powerful pattern matching for parsing files.

local date = os.date("%Y-%m-%d")
local filename = "content/daily/" .. date .. ".md"

local file = io.open(filename, "r")
if not file then
    print("⚠️  Log not found: " .. filename)
    os.exit(1)
end

print("==========================================")
print("   ARMAGDON STATUS (LUA) - " .. os.date("%A, %B %d"))
print("==========================================")

print("METRICS:")
for line in file:lines() do
    -- Match metrics in frontmatter
    local key, val = line:match("^(%w+_hours):%s*(%d+%.?%d*)")
    if key then
        print(string.format("  • %-15s: %s", key, val))
    end
    
    local status = line:match("^status:%s*\"([^"]+)\"")
    if status then
        print(string.format("  • %-15s: %s", "Status", status))
    end

    -- Match tasks
    local done, task = line:match("^-%s+%\\[([ xX])\\]%s+(.*)")
    if task then
        local mark = (done == " " and "[PENDING]" or "[DONE]   ")
        print("  " .. mark .. " " .. task)
    end
end

file:close()
print("==========================================")

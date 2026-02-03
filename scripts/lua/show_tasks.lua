#!/usr/bin/env lua

-- Add current directory to path for local requires
package.path = package.path .. ";scripts/lua/?.lua;./?.lua"
local C = require("ansi-colors")

local date = os.date("%Y-%m-%d")
local filename = "content/daily/" .. date .. ".md"

local file = io.open(filename, "r")
if not file then
    print(C.bold .. "⚠️  Log not found: " .. C.reset .. filename)
    os.exit(1)
end

print(C.bold .. C.accent .. "==========================================" .. C.reset)
print(C.bold .. "   ARMAGDON STATUS (LUA) - " .. os.date("%A, %B %d"))
print(C.bold .. C.accent .. "==========================================" .. C.reset)

print(C.bold .. "METRICS:" .. C.reset)
for line in file:lines() do
    -- Match metrics in frontmatter
    local key, val = line:match("^(%w+_hours):%s*(%d+%.?%d*)")
    if key then
        print(string.format("  • " .. C.yellow .. "%-15s" .. C.reset .. ": " .. C.bold .. "%s" .. C.reset, key, val))
    end
    
    local status = line:match("^status:%s*\"([^"]+)\"")
    if status then
        print(string.format("  • " .. C.yellow .. "%-15s" .. C.reset .. ": " .. C.bold .. "%s" .. C.reset, "Status", status))
    end

    -- Match tasks
    local done, task = line:match("^-%s+%[" .. "([ xX])" .. "]%s+(.*)")
    if task then
        if done == " " then
            print("  [" .. C.yellow .. "PENDING" .. C.reset .. "] " .. task)
        else
            print("  [" .. C.green .. "DONE" .. C.reset .. "   ] " .. C.dim .. task .. C.reset)
        end
    end
end

file:close()
print(C.bold .. C.accent .. "==========================================" .. C.reset)

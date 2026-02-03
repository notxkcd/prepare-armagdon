#!/usr/bin/env lua

-- Colors
local green  = "\27[32m"
local yellow = "\27[33m"
local bold   = "\27[1m"
local dim    = "\27[2m"
local reset  = "\27[0m"
local accent = "\27[38;5;64m" -- Muted Green (closest to #556b2f)

local date = os.date("%Y-%m-%d")
local filename = "content/daily/" .. date .. ".md"

local file = io.open(filename, "r")
if not file then
    print(bold .. "⚠️  Log not found: " .. reset .. filename)
    os.exit(1)
end

print(bold .. accent .. "==========================================" .. reset)
print(bold .. "   ARMAGDON STATUS (LUA) - " .. os.date("%A, %B %d"))
print(bold .. accent .. "==========================================" .. reset)

print(bold .. "METRICS:" .. reset)
for line in file:lines() do
    -- Match metrics in frontmatter
    local key, val = line:match("^(%w+_hours):%s*(%d+%.?%d*)")
    if key then
        print(string.format("  • " .. yellow .. "%-15s" .. reset .. ": " .. bold .. "%s" .. reset, key, val))
    end
    
    local status = line:match("^status:%s*\"([^"]+)\"")
    if status then
        print(string.format("  • " .. yellow .. "%-15s" .. reset .. ": " .. bold .. "%s" .. reset, "Status", status))
    end

    -- Match tasks
    local done, task = line:match("^-%s+%\\[([ xX])\\]%s+(.*)")
    if task then
        if done == " " then
            print("  [" .. yellow .. "PENDING" .. reset .. "] " .. task)
        else
            print("  [" .. green .. "DONE" .. reset .. "   ] " .. dim .. task .. reset)
        end
    end
end

file:close()
print(bold .. accent .. "==========================================" .. reset)
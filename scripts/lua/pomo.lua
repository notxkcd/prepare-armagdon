#!/usr/bin/env lua

-- Add current directory to path for local requires
package.path = package.path .. ";scripts/lua/?.lua;./?.lua"
local C = require("ansi-colors")

local POMO_INC = 0.42
local DURATION = 25

local function get_filename()
    return "content/daily/" .. os.date("%Y-%m-%d") .. ".md"
end

local function render_bar(percent, color)
    local width = 20
    local filled = math.floor(percent * width / 100)
    local empty = width - filled
    return color .. string.rep("█", filled) .. C.reset .. C.dim .. string.rep("░", empty) .. C.reset
end

local function run_timer(mins, label, color)
    local total = mins * 60
    local seconds = total
    while seconds > 0 do
        local m = math.floor(seconds / 60)
        local s = seconds % 60
        local percent = 100 - (seconds / total * 100)
        local bar = render_bar(percent, color)
        
        io.write(string.format("\r%s %s [%02d:%02d] %s", bar, C.bold .. label .. C.reset, m, s, C.reset))
        io.flush()
        os.execute("sleep 1")
        seconds = seconds - 1
    end
    print("\n" .. C.green .. C.bold .. "✅ " .. label .. " Complete!" .. C.reset)
end

local function update_log(filename, task_name, metric)
    local lines = {}
    local now = os.date("%H:%M")
    local f = io.open(filename, "r")
    for line in f:lines() do
        if line:find("^" .. metric .. ":") then
            local val = tonumber(line:match(":%s*(%d+%.?%d*)"))
            line = metric .. ": " .. string.format("%.2f", val + POMO_INC)
        end
        if line:find(task_name, 1, true) and not line:find("🍅") then
            line = line:gsub("%[ %]", "[ ] [" .. now .. "]")
            line = line .. " 🍅"
        end
        table.insert(lines, line)
    end
    f:close()
    f = io.open(filename, "w")
    for _, line in ipairs(lines) do f:write(line .. "\n") end
    f:close()
end

-- Main Loop
while true do
    os.execute("clear")
    print(C.bold .. C.accent .. "--- Lua Focus Loop ---" .. C.reset)
    local filename = get_filename()
    local tasks = {}
    local f = io.open(filename, "r")
    if not f then print(C.yellow .. "No log found." .. C.reset); break end
    for line in f:lines() do
        local done, name = line:match("^-%s+%[([ ])%]%s+(.*)")
        if name then table.insert(tasks, name) end
    end
    f:close()

    if #tasks == 0 then print(C.green .. "All tasks done!" .. C.reset); break end
    for i, t in ipairs(tasks) do print(C.bold .. i .. ")" .. C.reset .. " " .. t) end
    print(C.dim .. "q) Quit" .. C.reset)

    io.write("\n" .. C.bold .. "Select task #: " .. C.reset)
    local choice = io.read()
    if choice == "q" then break end
    local idx = tonumber(choice)
    if idx and tasks[idx] then
        local selected = tasks[idx]
        run_timer(DURATION, selected, C.accent)
        update_log(filename, selected, "focus_hours") -- Simple default
        print(C.dim .. "Log updated. Press Enter to continue..." .. C.reset)
        io.read()
    end
end

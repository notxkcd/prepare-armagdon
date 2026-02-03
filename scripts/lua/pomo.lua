#!/usr/bin/env lua

-- Colors
local green  = "\27[32m"
local yellow = "\27[33m"
local blue   = "\27[34m"
local bold   = "\27[1m"
local dim    = "\27[2m"
local reset  = "\27[0m"
local accent = "\27[38;5;64m"

local POMO_INC = 0.42
local DURATION = 25

local function get_filename()
    return "content/daily/" .. os.date("%Y-%m-%d") .. ".md"
end

local function render_bar(percent, color)
    local width = 20
    local filled = math.floor(percent * width / 100)
    local empty = width - filled
    return color .. string.rep("█", filled) .. reset .. dim .. string.rep("░", empty) .. reset
end

local function run_timer(mins, label, color)
    local total = mins * 60
    local seconds = total
    while seconds > 0 do
        local m = math.floor(seconds / 60)
        local s = seconds % 60
        local percent = 100 - (seconds / total * 100)
        local bar = render_bar(percent, color)
        
        io.write(string.format("\r%s %s [%02d:%02d] %s", bar, bold .. label .. reset, m, s, reset))
        io.flush()
        os.execute("sleep 1")
        seconds = seconds - 1
    end
    print("\n" .. green .. bold .. "✅ " .. label .. " Complete!" .. reset)
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
    print(bold .. accent .. "--- Lua Focus Loop ---" .. reset)
    local filename = get_filename()
    local tasks = {}
    local f = io.open(filename, "r")
    if not f then print(yellow .. "No log found." .. reset); break end
    for line in f:lines() do
        local done, name = line:match("^-%s+%[([ ])%]%s+(.*)")
        if name then table.insert(tasks, name) end
    end
    f:close()

    if #tasks == 0 then print(green .. "All tasks done!" .. reset); break end
    for i, t in ipairs(tasks) do print(bold .. i .. ")" .. reset .. " " .. t) end
    print(dim .. "q) Quit" .. reset)

    io.write("\n" .. bold .. "Select task #: " .. reset)
    local choice = io.read()
    if choice == "q" then break end
    local idx = tonumber(choice)
    if idx and tasks[idx] then
        local selected = tasks[idx]
        run_timer(DURATION, selected, accent)
        update_log(filename, selected, "focus_hours") -- Simple default
        print(dim .. "Log updated. Press Enter to continue..." .. reset)
        io.read()
    end
end
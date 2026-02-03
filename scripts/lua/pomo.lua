#!/usr/bin/env lua

-- Armagdon Prep - Lua Version of Focus Loop
-- Demonstrates file I/O and logical control flow in Lua.

local POMO_INC = 0.42
local DURATION = 25

local function get_filename()
    return "content/daily/" .. os.date("%Y-%m-%d") .. ".md"
end

local function run_timer(mins, label)
    local seconds = mins * 60
    while seconds > 0 do
        local m = math.floor(seconds / 60)
        local s = seconds % 60
        io.write(string.format("\r⏳ %s: %02d:%02d remaining...", label, m, s))
        io.flush()
        os.execute("sleep 1")
        seconds = seconds - 1
    end
    print("\n✅ " .. label .. " Complete!")
end

local function update_log(filename, task_name, metric)
    local lines = {}
    local now = os.date("%H:%M")
    
    -- Read file
    local f = io.open(filename, "r")
    for line in f:lines() do
        -- Update metric
        if line:find("^" .. metric .. ":") then
            local val = tonumber(line:match(":%s*(%d+%.?%d*)"))
            line = metric .. ": " .. string.format("%.2f", val + POMO_INC)
        end
        -- Update task line
        if line:find(task_name, 1, true) and not line:find("🍅") then
            line = line:gsub("%[" .. " " .. "]%s*[" .. " " .. "]", "[ ] [" .. now .. "]")
            line = line .. " 🍅"
        end
        table.insert(lines, line)
    end
    f:close()

    -- Write file
    f = io.open(filename, "w")
    for _, line in ipairs(lines) do
        f:write(line .. "\n")
    end
    f:close()
end

-- Main Loop
while true do
    os.execute("clear")
    print("--- Lua Focus Loop ---")
    local filename = get_filename()
    local tasks = {}
    
    local f = io.open(filename, "r")
    if not f then print("No log found."); break end
    
    for line in f:lines() do
        local done, name = line:match("^-%s+%[([ ])%]%s+(.*)")
        if name then table.insert(tasks, name) end
    end
    f:close()

    if #tasks == 0 then print("All tasks done!"); break end

    for i, t in ipairs(tasks) do print(i .. ") " .. t) end
    print("q) Quit")

    io.write("\nSelect task #: ")
    local choice = io.read()
    if choice == "q" then break end
    
    local idx = tonumber(choice)
    if idx and tasks[idx] then
        local selected = tasks[idx]
        run_timer(DURATION, selected)
        
        -- Categorize
        local metric = "focus_hours"
        if selected:find("Ruck") then metric = "physical_hours" end
        
        update_log(filename, selected, metric)
        print("Log updated. Press Enter to continue...")
        io.read()
    end
end

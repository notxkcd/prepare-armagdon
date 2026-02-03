local C = {}

C.reset  = "\27[0m"
C.bold   = "\27[1m"
C.dim    = "\27[2m"
C.italic = "\27[3m"

-- Colors
C.green  = "\27[32m"
C.yellow = "\27[33m"
C.blue   = "\27[34m"
C.cyan   = "\27[36m"
C.white  = "\27[37m"

-- Theme Accent (Muted Green)
C.accent = "\27[38;5;64m"

-- Helper function to wrap text in color
function C.colorize(color, text)
    return color .. text .. C.reset
end

return C

--
--
--

local tools = {}

function tools.this_is()
    print("this is only a test")
end

function tools.all_trim()
    return s:match("^%s*(.-)%s*$")
end

function tools.md5sum(value)
    local command = "echo -n '" .. value .."' | md5sum | cut -f1 -d' ' "
    local handle = io.popen(command)
    local result = handle:read("*a")
    handle:close()
    return tools.all_trim(result)
end

return tools

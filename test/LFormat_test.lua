--for
for i = 1, 10 do
    print(i)
end
for i, v in ipairs(table_name) do
    print(i, v)
end
for i, v in pairs(table_name) do
    print(i, v)
end

--single commit
--[[
    multi commit
]]

--function
local function function_name(a, b, ...) --commit test
    -- body
    print('local function test') ----[[commit test]]
end

function function_name(a, b, ...)
    -- body
    print('function test')
end

print(function()
    --todo
    return 'anonymity fuction'
end)

--string
str = 'hello world'
str = [[hello world]]
str = [[
    hello world
]]

--condition keys
if a >= b then end
if a <= b then end
if a == b then end
if a > b then end
if a < b then end
if true then
    print('hello')
elseif false then
    print('hello')
else 
    print('hello')
end

if (a > b) and (a == b) then
    
end

--indent
for i = 1, 10 do
    if true then
        print(i)
        for i = 1, 10 do
            print(i)
        end
    end
end
--operation keys
--[[operation]]c = 1 + 2 -3 * 4 / 5 % 6

--table
tbl = {}
tbl = { x = 1, y = 2 }
tbl = {
    x = 1,
    y = 2
}

--other
repeat
    print('hello')
until a == b

print(function() return 'hello' end, 'world')
require('hello')
require "hello"

foo():foo()
:foo()
:foo()





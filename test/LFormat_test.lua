--for test
for i=1,10 do
              print(i)
end
for i,v in ipairs( table_name ) do
print( i, v )
                    end
for i,v in pairs( table_name ) do
print( i, v )
end

--single commit test
--[[
    multi commit test
]]

--function test
local function function_name(a,b,...)--commit test
-- body
    print('local function test')         ----[[commit test]]
end

function function_name(a,b,...)
    -- body
    print('function test')
end

print(function( )
    --todo
    return 'anonymity fuction'
end)

--string
str='hello world'
str=[[hello world]]
str=[[
    hello world
]]

--condition keys test
if a>=b then    end
if a<=b then    end
if a==b then       end
if a>b then end
if a<b then end
if true then
    print('hello')
        elseif false then
            print('hello')
    else
print('hello')
    end

if (a>b) and(a==b) then
    
end

--indent test
for i=1,10 do
if true then
print(i)
for i = 1, 10        do
    print(i)
end
end
end

foo():foo():foo()
:foo()
:foo()

print('hello', 'world',
'hello',
'world',
'hello')

print('hello',function( abc )
    --todo
return 'anonymity fuction'
end, 'world',foo())

function foo( ... )
if true then 
    end   
    end

--operation keys test
--[[operation]]c=1+2-3*4/5%6

--table test
tbl= {}
tbl =    {x= 1  , y=2}
tbl = {
x =-1,
y=2
}

--other test
    repeat
    print('hello')
until   a==b

print(function () return 'hello'end,'world')
            require      ('hello')
require  "hello"

if true then
-- display.newSprite(display.getImage('hero_attack_00_01.png'))
        self:runAction(cc.Sequence:create(cc.DelayTime:create(0.5), cc.CallFunc:create(function()
            self._isAttack = false
        end)))
end



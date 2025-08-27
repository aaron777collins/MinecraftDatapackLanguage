say Testing conditionals with function calls
if "entity @s[type=minecraft:player]":
say Calling player function
function test:player_effects
else if "entity @s[type=minecraft:zombie]":
say Calling zombie function
function test:zombie_effects
else:
say Calling default function
function test:default_effects

tellraw @ a {"text":"Hover over me!","color":"blue","hoverEvent": {"action":"show_text","contents": {"text":"This is hover text!"}}}
tellraw @ a {"text":"Click me!","color":"green","clickEvent": {"action":"run_command","value":"/say clicked"}}
tellraw @ a {"text":"Interactive text!","color":"purple","hoverEvent": {"action":"show_text","contents": {"text":"Hover information"}},"clickEvent": {"action":"run_command","value":"/say interactive"}}
say say
say "Tellraw events complete"
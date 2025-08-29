# Garbage collection for MDL variables
# Clear temporary storage
data remove storage mdl:temp element
data remove storage mdl:temp index
data remove storage mdl:temp last_index
# Reset scoreboard objectives (optional - uncomment if needed)
# scoreboard objectives remove temp dummy
# scoreboard objectives remove temp2 dummy

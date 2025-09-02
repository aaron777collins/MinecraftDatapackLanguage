scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] gamePhase 2
tellraw @a [{"text":"Phase 2 starting!"}]
execute as @a run function comprehensive:phase_2

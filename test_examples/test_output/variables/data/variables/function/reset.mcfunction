scoreboard players set @e[type=armor_stand,tag=mdl_server,limit=1] globalCounter 0
scoreboard players set @s playerCounter 0
scoreboard players set @a[team=red] teamCounter 0
tellraw @a [{"text":"All counters reset !"}]
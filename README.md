
# Life Steal
Life Steal FR is a simple datapack aiming to add life steal behaviours from the original Lifesteal SMP:<br>
[https://lifesteal.fandom.com/wiki/Season_1](https://lifesteal.fandom.com/wiki/Season_1)

This datapack adds texture for the revive beacon and use 1.21 food components for interactions with the system (eating a heart, consuming a renamed revive beacon)

## Download links:
- Modrinth: [https://modrinth.com/datapack/lifestealfr/](https://modrinth.com/datapack/lifestealfr/)
- PlanetMinecraft: [https://www.planetminecraft.com/data-pack/life-steal-fr/](https://www.planetminecraft.com/data-pack/life-steal-fr/)

## Configuration
By default, revived players restart with 4 hearts and the maximum heart amount is 20.<br>
You can change that with these two commands when being /op:
- `scoreboard players set MAX_HEARTS life_steal.data 20`
- `scoreboard players set REVIVED_HEARTS life_steal.data 4`

As datapack don't have `/ban` permissions by default, you should edit your `server.properties` file and set the line `function-permission-level` to `3`



# Life Steal
[![GitHub](https://img.shields.io/github/v/release/Stoupy51/LifeSteal?logo=github&label=GitHub)](https://github.com/Stoupy51/LifeSteal/releases/latest)
[![Smithed](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.smithed.dev%2Fv2%2Fpacks%2Flifestealfr%2Fmeta&query=%24.stats.downloads.total&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDQgNCIgeG1sbnM6dj0iaHR0cHM6Ly92ZWN0YS5pby9uYW5vIj48cGF0aCBkPSJNLjczNy44NTlsLjg4Ny0uMjg1Yy4wOTktLjAzMi4yMDUtLjAzMi4zMDQgMGwxLjMzNS40MjktMS4wNC4zMzR6bS0uMTk1LjE4OXYuNDg3YzAgLjEwNS4wNjguMTk5LjE2OC4yMzFsMS41MTQuNDg3TDMuMjkgMS45MWMuMS0uMDMyLjE2OC0uMTI2LjE2OC0uMjMxdi0uNDg3bC0xLjIzNC4zOTF6bS44NTkgMS4xOWwuODIzLjI2LjQxMi0uMTI3di4zNzlsLS40MTIuMTMyLS44MjMtLjI2NHptLS40NDguNTA1di4yOTlsMS4yNzIuNDA4LjgyMy0uMjY0di0uM2wtLjgyMy4yNTl6IiBwYWludC1vcmRlcj0ic3Ryb2tlIGZpbGwgbWFya2VycyIgZmlsbD0iIzFiNDhjNCIvPjwvc3ZnPg%3D%3D&logoColor=224bbb&label=Smithed&labelColor=black&color=224bbb)](https://smithed.net/packs/lifestealfr)
[![Modrinth](https://img.shields.io/modrinth/dt/lifestealfr?logo=modrinth&label=Modrinth)](https://modrinth.com/datapack/lifestealfr)
[![Discord](https://img.shields.io/discord/1216400498488377467?label=Discord&logo=discord)](https://discord.gg/anxzu6rA9F)

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

![Life Steal Image](https://cdn.modrinth.com/data/3Gjekf6h/images/e4342487d618915d2a9d913e5774b41ca47b08b4.png)


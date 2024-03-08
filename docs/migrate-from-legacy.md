# Migrate from Legacy Version (0.x)
In 1.0, the specifications have been significantly changed and simplified.
```diff
import discord
from discord import app_commands
from discord.ext import commands
- from discord_ext_help import helpExtension, command_list, options
+ from discord_ext_help.help import extension
- from reactionmenu import ViewMenu

- command_list.cmdlist = [
-     {
-         "name": "/test",
-         "id": None,
-         "description": "this is a test command!",
-         "args": [],
-         "example": "https://media1.tenor.com/m/m1Tu9iU-zqQAAAAC/wumpus-discord.gif",
-     },
-     {
-         "name": "/say",
-         "id": None,
-         "description": "The character entered in the argument is uttered!",
-         "args": [
-             {
-                 "name": "text",
-                 "description": None,
-                 "required": True,
-             }
-         ],
-         "example": "https://media1.tenor.com/m/m1Tu9iU-zqQAAAAC/wumpus-discord.gif",
-     },
- ]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
+ deh = helpext(bot)

@bot.event
async def setup_hook():
-     await bot.tree.sync()
+     command = await bot.tree.sync()
+     await deh.regist_ids(command)

@bot.tree.command(
    name="help", description="show help"
)
- @app_commands.choices(command=options.cmds)
- async def help(interaction: discord.Interaction, command: str = None):
+ async def help(interaction: discord.Interaction):
    await interaction.response.defer()
    await generate(interaction)
-     res = await helpExtension.response(interaction, command)
-     menu = res["resp"]
- 
-     if res["type"] == "menu":
-         await menu.start()
-         return
-     await interaction.followup.send(embed=menu)

- helpExtension.setup()
bot.run(token)
```
## Difference from 0.x
* Generation of help using the conventional dictionary has been discontinued and replaced with automatic generation using `walk_commands()`.

If you want to use conventional code, use `discord_ext_help.legacy`. (Support is not provided, however.)
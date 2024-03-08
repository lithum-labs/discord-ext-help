# discord.ext.help
> [!NOTE]
> The specification has changed from the legacy version (0.x), and this library now only supports help generation for application commands.
A discord.py extension that automatically generates interaction help commands.

## Dependency
- [Defxult/reactionmenu](https://github.com/Defxult/reactionmenu)
- discord.py 2.0 and later 

This library is not guaranteed to be compatible with the discord.py fork (Because the reactionmenu used in this library is probably dedicated to discord.py).

Also, for pycord, you can reproduce the behavior of this library by using [`discord.ext.pages`](https://docs.pycord.dev/en/stable/ext/pages/index.html).

## How To Use
### Install
```
pip install discord-ext-help
```
### example
```python
import discord
from discord.ext import commands
from discord_ext_help.help import extension as helpext

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
deh = helpext(bot)

@bot.event
async def setup_hook():
    command = await bot.tree.sync()
    await deh.regist_ids(command)

@bot.tree.command(
    name="help", description="show help"
)
async def help(interaction: discord.Interaction):
    await interaction.response.defer()
    await generate(interaction)

bot.run(token)
```
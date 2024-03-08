import discord
from discord import app_commands
from discord.ext import commands
from reactionmenu import ViewButton, ViewMenu


class extension:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = {
            "embed_title": "{}'s command list".format(bot.user.name),
            "description_not_found": "There is no description for this command.",
            "description_not_found_group": "There is no description for this command group."
        }
        self.registed_id = False

    async def regist_ids(self, syncedTree):
        for cmd in syncedTree:
            if cmd.guild_id is None:
                self.bot.tree._global_commands[cmd.name].id = cmd.id
            else:
                self.bot.tree._guild_commands[cmd.guild.id][cmd.name].id = cmd.id
        self.registed_id = True
        # -----------------------------------
        embed = discord.Embed(title=self.config["embed_title"])
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        cmds = [
            com
            for com in self.bot.tree.walk_commands()
            if isinstance(com, app_commands.Command)
        ]
        groups = [
            com
            for com in self.bot.tree.walk_commands()
            if isinstance(com, app_commands.Group)
        ]

        loops = 1
        emb = []
        length = len(cmds)
        for command in cmds:
            command_name = command.name
            if self.registed_id:
                command_name = "</{}:{}>".format(command.name, command.id)
            embed.add_field(
                name=command_name,
                value=command.description
                if command.description
                else self.config["description_not_found"],
            )
            if loops >= 6:
                emb.append(embed)
                embed = discord.Embed(title=self.config["embed_title"])
                embed.set_author(
                    name=self.bot.user.name, icon_url=self.bot.user.avatar.url
                )
                loops = 0
            else:
                loops = loops + 1

        for group_command in groups:
            embed = discord.Embed(
                title=group_command.name,
                description=group_command.description
                if group_command.description
                else None,
                color=discord.Color.blurple(),
            )
            for comm in group_command.commands:
                embed.add_field(
                    name=comm.name,
                    value=comm.description if comm.description else comm.name,
                    inline=False,
                )
            emb.append(emb)

        if not loops > length:
            emb.append(embed)
        self.menu_cache = emb

    async def generate(self, interaction: discord.Interaction):
        menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)
        if self.menu_cache:
            emb = self.menu_cache
        else:
            embed = discord.Embed(title=self.config["embed_title"])
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            cmds = [
                com
                for com in self.bot.tree.walk_commands()
                if isinstance(com, app_commands.Command)
            ]
            groups = [
                com
                for com in self.bot.tree.walk_commands()
                if isinstance(com, app_commands.Group)
            ]

            loops = 1
            emb = []
            length = len(cmds)
            for command in cmds:
                command_name = command.name
                if self.registed_id:
                    command_name = "</{}:{}>".format(command.name, command.id)
                embed.add_field(
                    name=command_name,
                    value=command.description
                    if command.description
                    else self.config["description_not_found"],
                )
                if loops >= 6:
                    emb.append(embed)
                    embed = discord.Embed(title=self.config["embed_title"])
                    embed.set_author(
                        name=self.bot.user.name, icon_url=self.bot.user.avatar.url
                    )
                    loops = 0
                else:
                    loops = loops + 1

            for group_command in groups:
                embed = discord.Embed(
                    title=self.config["embed_title"] + " (" + group_command.name + ")",
                    description=group_command.description
                    if group_command.description
                    else self.config["description_not_found_group"],
                    color=discord.Color.blurple(),
                )
                for comm in group_command.commands:
                    embed.add_field(
                        name=comm.name,
                        value=comm.description if comm.description else comm.name,
                        inline=False,
                    )
                emb.append(emb)

            if not loops > length:
                emb.append(embed)
        for embed in emb:
            menu.add_page(embed)
        menu.add_button(ViewButton.go_to_first_page())
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        menu.add_button(ViewButton.go_to_last_page())
        await menu.start()

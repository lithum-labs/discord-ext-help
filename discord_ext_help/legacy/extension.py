import discord
from discord import app_commands
from discord.ext import commands as dcommands
from reactionmenu import ViewMenu, ViewButton

from .config import options, command_list

class helpExtension:

    async def response(interaction: discord.Interaction, command: str = None):
        if command is None:
            title = options.embed_title
            menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)

            length = len(command_list.cmdlist)
            # pages = max(length // 10 + (1 if length % 10 > 0 else 0), 1) # 念のため残しておく
            ct = 0
            lct = 0
            emb = []
            embed = discord.Embed(title=title)
            for cmds in command_list.cmdlist:
                cmdname = "{}".format(cmds["name"])
                desc = options.nodesc
                if not cmds["id"] is None:
                    cmdname = "<{}:{}>".format(cmds["name"], cmds["id"])
                if not cmds["description"] is None:
                    desc = cmds["description"]
                embed.add_field(name=cmdname, value=desc)
                if ct >= 8:
                    emb.append(embed)
                    embed = discord.Embed(title=title)
                    ct = 0
                else:
                    ct = ct + 1
                lct = lct + 1
            if not lct > length:
                emb.append(embed)

            for embed in emb:
                menu.add_page(embed)

            menu.add_button(ViewButton.go_to_first_page())
            menu.add_button(ViewButton.back())
            menu.add_button(ViewButton.next())
            menu.add_button(ViewButton.go_to_last_page())

            return {"type": "menu", "resp": menu}
        else:
            cmd = None
            for cmds in command_list.cmdlist:
                if cmds["name"] == command:
                    cmd = cmds
                    break
            embed = discord.Embed(
                title=options.error.cmd_error_title,
                description=options.error.cmd_notfound,
            )
            if not cmd is None:
                if not cmd["id"] is None:
                    command = "<{}:{}>".format(cmds["name"], cmds["id"])
                desc_cmd = options.nodesc
                if not cmds["description"] is None:
                    desc_cmd = cmds["description"]
                embed = discord.Embed(
                    title=options.cmd_desc.replace("{cmdname}", command),
                    description=desc_cmd
                )
                for args in cmd["args"]:
                    desc = options.nodesc_args
                    req = options.optional
                    if args["required"]:
                        req = options.required
                    if not args["description"] is None:
                        desc = args["description"]
                    embed.add_field(
                        name="`{}` ({})".format(args["name"], req), value=desc
                    )
                if not cmd["example"] is None:
                    embed.set_image(url=cmd["example"])

            
            return {"type": "embed", "resp": embed}

    def setup():
        command_list.cmdlist.append(
            {
                "name": "/help",
                "id": options.help_id,
                "description": options.description,
                "args": [
                    {
                        "name": options.args_name,
                        "description": options.args_desc,
                        "required": False
                    }
                ],
                "example": options.example_help
            }
        )
        for cmds in command_list.cmdlist:
            options.cmds.append(
                discord.app_commands.Choice(name=cmds["name"], value=cmds["name"])
            )
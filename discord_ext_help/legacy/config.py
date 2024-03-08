class options:
    botname = "testBot"  # bot name.
    embed_title = "{} help".format(botname)
    embed_desc = "List of {} commands.".format(botname)
    name = "help"
    description = "Displays a list of commands."
    args_name = "command"
    args_desc = "Displays detailed usage of the specified command."
    nodesc = "No description is provided for this commands."
    nodesc_args = "No description is provided for this arguments."
    cmds = []
    guild = None
    cmd_desc = "Explanation of {cmdname}"
    optional = "optional"
    required = "required"
    help_id = None
    example_help = None

    class error:
        cmd_error_title = "Error"
        cmd_notfound = "This command does not exist."

class command_list:
    cmdlist = []
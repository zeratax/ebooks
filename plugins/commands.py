###
# This module is supposed to give other plugins the ability to create and remove
# new bot commands
###

# check if commands is already initialized
try:
  commands
except NameError:
  commands = {}


def create_command(group, name, keywords, description, mention=True):
    """
    function to create bot commands for other modules,
    will be stored in commands variable
    """
    if not group in commands:
        commands[group] = {}
    commands[group][name] = {}
    commands[group][name]['keywords'] = keywords
    commands[group][name]['description'] = description
    commands[group][name]['mention'] = mention

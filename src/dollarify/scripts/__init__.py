from dollarify.scripts import main, manage, run
commands = [manage.cli, run.cli]
for cmd in commands:
    main.cli.add_command(cmd)
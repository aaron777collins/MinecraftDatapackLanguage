complete -c mdl -n "__fish_use_subcommand" -a "build" -d "Build MDL files into a datapack"
complete -c mdl -n "__fish_use_subcommand" -a "check" -d "Check MDL files for syntax errors"
complete -c mdl -n "__fish_use_subcommand" -a "new" -d "Create a new MDL project"
complete -c mdl -n "__fish_use_subcommand" -a "completion" -d "Shell completion utilities"
complete -c mdl -n "__fish_use_subcommand" -a "docs" -d "Docs utilities"

# global options
complete -c mdl -s h -l help -d "Show help"
complete -c mdl -l version -d "Show version"

# build options
complete -c mdl -n "__fish_seen_subcommand_from build" -l mdl -d "MDL file or directory" -r -F
complete -c mdl -n "__fish_seen_subcommand_from build" -s o -l output -d "Output directory" -r -F
complete -c mdl -n "__fish_seen_subcommand_from build" -l verbose -d "Verbose output"
complete -c mdl -n "__fish_seen_subcommand_from build" -l wrapper -d "Wrapper directory" -r
complete -c mdl -n "__fish_seen_subcommand_from build" -l no-zip -d "Do not zip"
complete -c mdl -n "__fish_seen_subcommand_from build" -s h -l help -d "Help"

# check options
complete -c mdl -n "__fish_seen_subcommand_from check" -l verbose -d "Verbose output"
complete -c mdl -n "__fish_seen_subcommand_from check" -s h -l help -d "Help"

# new options
complete -c mdl -n "__fish_seen_subcommand_from new" -l pack-name -d "Custom datapack name" -r
complete -c mdl -n "__fish_seen_subcommand_from new" -l pack-format -d "Pack format number" -r
complete -c mdl -n "__fish_seen_subcommand_from new" -l output -d "Project directory" -r -F
complete -c mdl -n "__fish_seen_subcommand_from new" -l exclude-local-docs -d "Skip copying docs"
complete -c mdl -n "__fish_seen_subcommand_from new" -s h -l help -d "Help"

# completion subcommands
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "print" -d "Print completion script"
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "install" -d "Install completion"
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "uninstall" -d "Uninstall completion"
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "doctor" -d "Diagnose setup"
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "bash zsh fish powershell" -d "Shell"

# docs subcommands
complete -c mdl -n "__fish_seen_subcommand_from docs" -a "open" -d "Open docs website"
complete -c mdl -n "__fish_seen_subcommand_from docs" -a "serve" -d "Serve docs locally"
complete -c mdl -n "__fish_seen_subcommand_from docs" -l port -d "Port" -r
complete -c mdl -n "__fish_seen_subcommand_from docs" -l dir -d "Docs directory" -r -F
complete -c mdl -n "__fish_seen_subcommand_from docs" -s h -l help -d "Help"


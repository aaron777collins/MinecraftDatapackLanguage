complete -c mdl -n "__fish_use_subcommand" -a "build" -d "Build MDL files into a datapack"
complete -c mdl -n "__fish_use_subcommand" -a "check" -d "Check MDL files for syntax errors"
complete -c mdl -n "__fish_use_subcommand" -a "new" -d "Create a new MDL project"
complete -c mdl -n "__fish_use_subcommand" -a "completion" -d "Shell completion utilities"
complete -c mdl -n "__fish_use_subcommand" -a "docs" -d "Docs utilities"

# build options
complete -c mdl -n "__fish_seen_subcommand_from build" -l mdl -d "MDL file or directory" -r -F
complete -c mdl -n "__fish_seen_subcommand_from build" -s o -l output -d "Output directory" -r -F
complete -c mdl -n "__fish_seen_subcommand_from build" -l verbose -d "Verbose output"
complete -c mdl -n "__fish_seen_subcommand_from build" -l wrapper -d "Wrapper directory" -r
complete -c mdl -n "__fish_seen_subcommand_from build" -l no-zip -d "Do not zip"

# check options
complete -c mdl -n "__fish_seen_subcommand_from check" -l verbose -d "Verbose output"

# new options
complete -c mdl -n "__fish_seen_subcommand_from new" -l pack-name -d "Custom datapack name" -r
complete -c mdl -n "__fish_seen_subcommand_from new" -l pack-format -d "Pack format number" -r
complete -c mdl -n "__fish_seen_subcommand_from new" -l output -d "Project directory" -r -F
complete -c mdl -n "__fish_seen_subcommand_from new" -l exclude-local-docs -d "Skip copying docs"

# completion subcommands
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "print" -d "Print completion script"
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "install" -d "Install completion"
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "uninstall" -d "Uninstall completion"
complete -c mdl -n "__fish_seen_subcommand_from completion" -a "doctor" -d "Diagnose setup"

# docs subcommands
complete -c mdl -n "__fish_seen_subcommand_from docs" -a "serve" -d "Serve docs locally"


_mdl_complete() {
  local cur prev words cword
  _init_completion -n : || {
    COMPREPLY=()
    return
  }

  local subcommands="build check new completion docs"
  if [[ ${cword} -eq 1 ]]; then
    COMPREPLY=( $(compgen -W "${subcommands}" -- "$cur") )
    return
  fi

  case "${words[1]}" in
    build)
      COMPREPLY=( $(compgen -W "--mdl -o --output --verbose --wrapper --no-zip" -- "$cur") )
      [[ ${cur} == -* ]] || COMPREPLY+=( $(compgen -f -d -- "$cur") )
      ;;
    check)
      COMPREPLY=( $(compgen -W "--verbose" -- "$cur") )
      [[ ${cur} == -* ]] || COMPREPLY+=( $(compgen -f -d -- "$cur") )
      ;;
    new)
      COMPREPLY=( $(compgen -W "--pack-name --pack-format --output --exclude-local-docs" -- "$cur") )
      ;;
    completion)
      COMPREPLY=( $(compgen -W "print install uninstall doctor" -- "$cur") )
      ;;
    docs)
      COMPREPLY=( $(compgen -W "serve" -- "$cur") )
      ;;
  esac
}
complete -F _mdl_complete mdl


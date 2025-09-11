_mdl_complete() {
  local cur prev words cword
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  words=("${COMP_WORDS[@]}")
  cword=${COMP_CWORD}

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
      COMPREPLY=( $(compgen -W "open serve" -- "$cur") )
      ;;
  esac
}
complete -F _mdl_complete mdl


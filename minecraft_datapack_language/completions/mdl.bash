_mdl_complete() {
  local cur prev words cword
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  words=("${COMP_WORDS[@]}")
  cword=${COMP_CWORD}

  local subcommands="build check new completion docs"
  if [[ ${cword} -eq 1 ]]; then
    if [[ "$cur" == -* ]]; then
      COMPREPLY=( $(compgen -W "-h --help --version" -- "$cur") )
    else
      COMPREPLY=( $(compgen -W "${subcommands}" -- "$cur") )
    fi
    return
  fi

  # Global options available anywhere
  if [[ "$cur" == -* ]]; then
    COMPREPLY=( $(compgen -W "-h --help --version" -- "$cur") )
    return
  fi

  case "${words[1]}" in
    build)
      COMPREPLY=( $(compgen -W "--mdl -o --output --verbose --wrapper --no-zip -h --help" -- "$cur") )
      [[ "$prev" == "--mdl" ]] && { COMPREPLY=( $(compgen -f -d -- "$cur") ); return; }
      [[ "$prev" == "-o" || "$prev" == "--output" ]] && { COMPREPLY=( $(compgen -d -- "$cur") ); return; }
      [[ ${cur} == -* ]] || COMPREPLY+=( $(compgen -f -d -- "$cur") )
      ;;
    check)
      COMPREPLY=( $(compgen -W "--verbose -h --help" -- "$cur") )
      [[ ${cur} == -* ]] || COMPREPLY+=( $(compgen -f -d -- "$cur") )
      ;;
    new)
      COMPREPLY=( $(compgen -W "--pack-name --pack-format --output --exclude-local-docs -h --help" -- "$cur") )
      [[ "$prev" == "--output" ]] && { COMPREPLY=( $(compgen -d -- "$cur") ); return; }
      ;;
    completion)
      # Suggest subcommands or shells for 3rd arg
      if [[ ${cword} -eq 2 ]]; then
        COMPREPLY=( $(compgen -W "print install uninstall doctor -h --help" -- "$cur") )
      else
        case "${words[2]}" in
          print|install|uninstall)
            COMPREPLY=( $(compgen -W "bash zsh fish powershell" -- "$cur") )
            ;;
          *) ;;
        esac
      fi
      ;;
    docs)
      if [[ ${cword} -eq 2 ]]; then
        COMPREPLY=( $(compgen -W "open serve -h --help" -- "$cur") )
      else
        if [[ "${words[2]}" == "serve" ]]; then
          COMPREPLY=( $(compgen -W "--port --dir -h --help" -- "$cur") )
          [[ ${cur} == -* ]] || COMPREPLY+=( $(compgen -d -- "$cur") )
        fi
      fi
      ;;
  esac
}
complete -F _mdl_complete mdl


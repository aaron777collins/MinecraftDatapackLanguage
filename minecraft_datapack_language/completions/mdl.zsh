#compdef mdl
_mdl() {
  local -a subcmds
  subcmds=(build check new completion docs)
  if (( CURRENT == 2 )); then
    _arguments '-h[Show help]' '--help[Show help]' '--version[Show version]'
    _describe 'command' subcmds
    return
  fi
  case $words[2] in
    build)
      _arguments '-h[Help]' '--help[Help]' '*:file:_files' '--mdl[MDL file or dir]:file:_files' '-o[Output dir]:dir:_files -/' '--output[Output dir]:dir:_files -/' '--verbose[Verbose]' '--wrapper[Wrapper name]' '--no-zip[No zip]'
      ;;
    check)
      _arguments '-h[Help]' '--help[Help]' '*:file:_files' '--verbose[Verbose]'
      ;;
    new)
      _arguments '-h[Help]' '--help[Help]' '--pack-name[Datapack name]:name:' '--pack-format[Pack format]:number:' '--output[Project dir]:dir:_files -/' '--exclude-local-docs[Skip docs]'
      ;;
    completion)
      _values 'subcommands' 'print' 'install' 'uninstall' 'doctor'
      if (( CURRENT == 3 )); then
        _values 'shells' 'bash' 'zsh' 'fish' 'powershell'
      fi
      ;;
    docs)
      _values 'subcommands' 'open' 'serve'
      if [[ $words[3] == 'serve' ]]; then
        _arguments '-h[Help]' '--help[Help]' '--port[Port]:port:' '--dir[Docs directory]:dir:_files -/'
      fi
      ;;
  esac
}
compdef _mdl mdl


#compdef mdl
_mdl() {
  local -a subcmds
  subcmds=(build check new completion docs)
  if (( CURRENT == 2 )); then
    _describe 'command' subcmds
    return
  fi
  case $words[2] in
    build)
      _arguments '*:file:_files' '--mdl' '-o' '--output' '--verbose' '--wrapper' '--no-zip'
      ;;
    check)
      _arguments '*:file:_files' '--verbose'
      ;;
    new)
      _arguments '--pack-name' '--pack-format' '--output' '--exclude-local-docs'
      ;;
    completion)
      _values 'subcommands' 'print' 'install' 'uninstall' 'doctor'
      ;;
    docs)
      _values 'subcommands' 'serve'
      ;;
  esac
}
compdef _mdl mdl


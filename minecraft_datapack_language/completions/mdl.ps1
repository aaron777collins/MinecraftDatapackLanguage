Register-ArgumentCompleter -Native -CommandName mdl -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
    $line = $commandAst.ToString()
    $parts = [System.Management.Automation.PSParser]::Tokenize($line, [ref]$null) | Where-Object { $_.Type -eq 'CommandArgument' } | ForEach-Object { $_.Content }
    if ($parts.Count -lt 1) {
        'build','check','new','completion','docs','--help','-h','--version' | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_) }
        return
    }
    switch ($parts[0]) {
        'build' {
            '--mdl','-o','--output','--verbose','--wrapper','--no-zip','--help','-h' | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterName', $_) }
        }
        'check' {
            '--verbose','--help','-h' | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterName', $_) }
        }
        'new' {
            '--pack-name','--pack-format','--output','--exclude-local-docs','--help','-h' | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterName', $_) }
        }
        'completion' {
            'print','install','uninstall','doctor','--help','-h' | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_) }
        }
        'docs' {
            'open','serve','--help','-h','--port','--dir' | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_) }
        }
    }
}


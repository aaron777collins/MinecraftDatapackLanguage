
import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  const diag = vscode.languages.createDiagnosticCollection('mdl');
  context.subscriptions.push(diag);

  // Register completion provider for IntelliSense
  const completionProvider = vscode.languages.registerCompletionItemProvider('mdl', {
    provideCompletionItems(document, position) {
      const completionItems: vscode.CompletionItem[] = [];
      
      // Get the line text up to the cursor position
      const linePrefix = document.lineAt(position).text.substr(0, position.character);
      
      // Check if we're in a pack declaration
      if (linePrefix.includes('pack "') && !linePrefix.includes('pack_format')) {
        const formatItem = new vscode.CompletionItem('pack_format 15', vscode.CompletionItemKind.Field);
        formatItem.detail = 'Pack format version';
        formatItem.documentation = 'Specifies the pack format version. Use 15 for modern format';
        formatItem.insertText = 'pack_format 15';
        completionItems.push(formatItem);
      }
      
      if (linePrefix.includes('pack "') && !linePrefix.includes('description')) {
        const descItem = new vscode.CompletionItem('description "Description"', vscode.CompletionItemKind.Field);
        descItem.detail = 'Pack description';
        descItem.insertText = 'description "Description"';
        completionItems.push(descItem);
      }
      
      // Variable declarations
      if (linePrefix.trim().startsWith('var ')) {
        const numItem = new vscode.CompletionItem('num', vscode.CompletionItemKind.Keyword);
        numItem.detail = 'Number variable type';
        numItem.documentation = 'Declares a number variable stored in scoreboard';
        numItem.insertText = 'num';
        completionItems.push(numItem);
        
        // Scope completions for variable declarations
        const scopeItem = new vscode.CompletionItem('<@s>', vscode.CompletionItemKind.Keyword);
        scopeItem.detail = 'Player scope';
        scopeItem.documentation = 'Declare variable with player scope (default for most variables)';
        scopeItem.insertText = '<@s>';
        completionItems.push(scopeItem);
        
        const allPlayersScopeItem = new vscode.CompletionItem('<@a>', vscode.CompletionItemKind.Keyword);
        allPlayersScopeItem.detail = 'All players scope';
        allPlayersScopeItem.documentation = 'Declare variable with all players scope';
        allPlayersScopeItem.insertText = '<@a>';
        completionItems.push(allPlayersScopeItem);
        
        const teamScopeItem = new vscode.CompletionItem('<@a[team=red]>', vscode.CompletionItemKind.Keyword);
        teamScopeItem.detail = 'Team scope';
        teamScopeItem.documentation = 'Declare variable with team scope';
        teamScopeItem.insertText = '<@a[team=red]>';
        completionItems.push(teamScopeItem);
      }
      
      // Variable assignment with scope completions
      if (linePrefix.includes('=') || linePrefix.includes('+') || linePrefix.includes('-') || linePrefix.includes('*') || linePrefix.includes('/')) {
        // Suggest scope syntax for variable access
        const playerScopeItem = new vscode.CompletionItem('<@s>', vscode.CompletionItemKind.Keyword);
        playerScopeItem.detail = 'Player scope access';
        playerScopeItem.documentation = 'Access variable with player scope';
        playerScopeItem.insertText = '<@s>';
        completionItems.push(playerScopeItem);
        
        const allPlayersScopeItem = new vscode.CompletionItem('<@a>', vscode.CompletionItemKind.Keyword);
        allPlayersScopeItem.detail = 'All players scope access';
        allPlayersScopeItem.documentation = 'Access variable with all players scope';
        allPlayersScopeItem.insertText = '<@a>';
        completionItems.push(allPlayersScopeItem);
        
        const teamScopeItem = new vscode.CompletionItem('<@a[team=red]>', vscode.CompletionItemKind.Keyword);
        teamScopeItem.detail = 'Team scope access';
        teamScopeItem.documentation = 'Access variable with team scope';
        teamScopeItem.insertText = '<@a[team=red]>';
        completionItems.push(teamScopeItem);
      }
      
      // Control flow keywords
      const controlFlowKeywords = [
        { name: 'if', detail: 'If statement', doc: 'Conditional statement with curly braces' },
        { name: 'else', detail: 'Else statement', doc: 'Default branch for conditional' },
        { name: 'while', detail: 'While loop', doc: 'Loop that continues while condition is true' }
      ];
      
      controlFlowKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Variable declaration keywords
      const varKeywords = [
        { name: 'var', detail: 'Variable declaration', doc: 'Declare a variable' }
      ];
      
      varKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Function execution keywords
      const execKeywords = [
        { name: 'exec', detail: 'Execute function', doc: 'Execute a function with optional scope' }
      ];
      
      execKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Hook keywords
      const hookKeywords = [
        { name: 'on_load', detail: 'Load hook', doc: 'Function that runs when datapack loads' },
        { name: 'on_tick', detail: 'Tick hook', doc: 'Function that runs every tick' }
      ];
      
      hookKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Tag type keywords
      const tagTypeKeywords = [
        { name: 'recipe', detail: 'Recipe tag', doc: 'Tag for custom crafting recipes' },
        { name: 'loot_table', detail: 'Loot table tag', doc: 'Tag for custom loot drops' },
        { name: 'advancement', detail: 'Advancement tag', doc: 'Tag for custom advancements' },
        { name: 'item_modifier', detail: 'Item modifier tag', doc: 'Tag for custom item modifiers' },
        { name: 'predicate', detail: 'Predicate tag', doc: 'Tag for custom predicates' },
        { name: 'structure', detail: 'Structure tag', doc: 'Tag for custom structures' }
      ];
      
      tagTypeKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Minecraft commands
      const minecraftCommands = [
        { name: 'say', detail: 'Say command', doc: 'Send message to all players (auto-converts to tellraw)' },
        { name: 'tellraw', detail: 'Tellraw command', doc: 'Send formatted message with JSON' },
        { name: 'effect', detail: 'Effect command', doc: 'Apply status effect' },
        { name: 'particle', detail: 'Particle command', doc: 'Create particle effect' },
        { name: 'execute', detail: 'Execute command', doc: 'Execute command conditionally' },
        { name: 'scoreboard', detail: 'Scoreboard command', doc: 'Manage scoreboard objectives' },
        { name: 'function', detail: 'Function command', doc: 'Call another function' },
        { name: 'tag', detail: 'Tag command', doc: 'Manage entity tags' },
        { name: 'tp', detail: 'Teleport command', doc: 'Teleport entities' },
        { name: 'kill', detail: 'Kill command', doc: 'Kill entities' },
        { name: 'summon', detail: 'Summon command', doc: 'Summon entity' },
        { name: 'give', detail: 'Give command', doc: 'Give item to player' }
      ];
      
      minecraftCommands.forEach(cmd => {
        const item = new vscode.CompletionItem(cmd.name, vscode.CompletionItemKind.Function);
        item.detail = cmd.detail;
        item.documentation = cmd.doc;
        item.insertText = cmd.name;
        completionItems.push(item);
      });
      
      // Function call scope completions
      if (linePrefix.includes('exec') && linePrefix.includes(':')) {
        const functionPlayerScopeItem = new vscode.CompletionItem('<@s>', vscode.CompletionItemKind.Keyword);
        functionPlayerScopeItem.detail = 'Player scope function call';
        functionPlayerScopeItem.documentation = 'Execute function as current player';
        functionPlayerScopeItem.insertText = '<@s>';
        completionItems.push(functionPlayerScopeItem);
        
        const functionAllPlayersScopeItem = new vscode.CompletionItem('<@a>', vscode.CompletionItemKind.Keyword);
        functionAllPlayersScopeItem.detail = 'All players scope function call';
        functionAllPlayersScopeItem.documentation = 'Execute function as all players';
        functionAllPlayersScopeItem.insertText = '<@a>';
        completionItems.push(functionAllPlayersScopeItem);
        
        const functionTeamScopeItem = new vscode.CompletionItem('<@a[team=red]>', vscode.CompletionItemKind.Keyword);
        functionTeamScopeItem.detail = 'Team scope function call';
        functionTeamScopeItem.documentation = 'Execute function as team members';
        functionTeamScopeItem.insertText = '<@a[team=red]>';
        completionItems.push(functionTeamScopeItem);
      }
      
      // Entity selectors
      const selectors = [
        { name: '@p', detail: 'Nearest player', doc: 'Select nearest player' },
        { name: '@r', detail: 'Random player', doc: 'Select random player' },
        { name: '@a', detail: 'All players', doc: 'Select all players' },
        { name: '@e', detail: 'All entities', doc: 'Select all entities' },
        { name: '@s', detail: 'Self', doc: 'Select executing entity' }
      ];
      
      selectors.forEach(selector => {
        const item = new vscode.CompletionItem(selector.name, vscode.CompletionItemKind.Variable);
        item.detail = selector.detail;
        item.documentation = selector.doc;
        item.insertText = selector.name;
        completionItems.push(item);
      });
      
      // Raw text syntax
      const rawTextItems = [
        { 
          name: '$!raw', 
          detail: 'Raw text block start', 
          doc: 'Start a raw text block. Content inside will be inserted directly without MDL parsing.',
          insertText: '$!raw\n    ${1:Insert raw text here}\nraw!$'
        },
        { 
          name: 'raw!$', 
          detail: 'Raw text block end', 
          doc: 'End a raw text block.',
          insertText: 'raw!$'
        }
      ];
      
      rawTextItems.forEach(item => {
        const completionItem = new vscode.CompletionItem(item.name, vscode.CompletionItemKind.Keyword);
        completionItem.detail = item.detail;
        completionItem.documentation = item.doc;
        completionItem.insertText = new vscode.SnippetString(item.insertText);
        completionItems.push(completionItem);
      });
      
      // Variable substitution syntax
      const varSubItems = [
        { 
          name: '$variable<@s>$', 
          detail: 'Variable substitution', 
          doc: 'Read variable value with scope',
          insertText: '$${1:variable}<${2:@s}>$'
        }
      ];
      
      varSubItems.forEach(item => {
        const completionItem = new vscode.CompletionItem(item.name, vscode.CompletionItemKind.Variable);
        completionItem.detail = item.detail;
        completionItem.documentation = item.doc;
        completionItem.insertText = new vscode.SnippetString(item.insertText);
        completionItems.push(completionItem);
      });
      
      return completionItems;
    }
  });

  context.subscriptions.push(completionProvider);

  vscode.workspace.onDidSaveTextDocument(doc => {
    if (doc.languageId === 'mdl') {
      runCheckFile(doc, diag);
    }
  });

  const buildCmd = vscode.commands.registerCommand('mdl.build', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) { return; }
    const doc = editor.document;
    if (doc.languageId !== 'mdl') { return; }
    const out = await vscode.window.showInputBox({ prompt: 'Output datapack folder', value: 'dist/datapack' });
    if (!out) { return; }
    const wrapper = await vscode.window.showInputBox({ prompt: 'Wrapper name (optional)', value: '' });
    const wrapperArg = wrapper ? ` --wrapper "${wrapper}"` : '';
    const cmd = `mdl build --mdl "${doc.fileName}" -o "${out}"${wrapperArg}`;
    runShell(cmd);
  });

  const checkWsCmd = vscode.commands.registerCommand('mdl.checkWorkspace', async () => {
    const folder = vscode.workspace.workspaceFolders?.[0];
    if (!folder) {
      vscode.window.showErrorMessage('Open a folder or workspace to check.');
      return;
    }
    await runCheckWorkspace(folder.uri.fsPath, diag);
  });

  const newProjectCmd = vscode.commands.registerCommand('mdl.newProject', async () => {
    const name = await vscode.window.showInputBox({ prompt: 'Project name', value: 'my_mdl_project' });
    if (!name) { return; }
    const description = await vscode.window.showInputBox({ prompt: 'Project description', value: 'My MDL Project' });
    if (!description) { return; }
    const cmd = `mdl new "${name}" --name "${description}" --pack-format 15`;
    runShell(cmd);
  });

  context.subscriptions.push(buildCmd, checkWsCmd, newProjectCmd);

  // initial diagnostics
  const active = vscode.window.activeTextEditor?.document;
  if (active && active.languageId === 'mdl') {
    runCheckFile(active, diag);
  }
}

function runCheckFile(doc: vscode.TextDocument, diag: vscode.DiagnosticCollection) {
  const cmd = `mdl check --json "${doc.fileName}"`;
  exec(cmd, (err, stdout, stderr) => {
    updateDiagnosticsFromJson(diag, [doc.fileName], stdout || stderr);
  });
}

async function runCheckWorkspace(root: string, diag: vscode.DiagnosticCollection) {
  const cmd = `mdl check --json "${root}"`;
  exec(cmd, (err, stdout, stderr) => {
    // We'll parse JSON diagnostics and map to files
    updateDiagnosticsFromJson(diag, undefined, stdout || stderr);
  });
}

function updateDiagnosticsFromJson(diag: vscode.DiagnosticCollection, limitTo?: string[], output?: string) {
  const fileMap = new Map<string, vscode.Diagnostic[]>();
  try {
    const parsed = JSON.parse(output || '{"ok":true,"errors":[]}');
    const errors = parsed.errors as Array<{file:string, line?:number, message:string}>;
    for (const err of errors || []) {
      if (limitTo && !limitTo.includes(err.file)) continue;
      const uri = vscode.Uri.file(err.file);
      const existing = fileMap.get(uri.fsPath) || [];
      const line = typeof err.line === 'number' ? Math.max(0, err.line - 1) : 0;
      const range = new vscode.Range(line, 0, line, Number.MAX_SAFE_INTEGER);
      existing.push(new vscode.Diagnostic(range, err.message, vscode.DiagnosticSeverity.Error));
      fileMap.set(uri.fsPath, existing);
    }
  } catch (e) {
    // fallback: clear on parse errors
  }

  // Clear diagnostics first
  diag.clear();

  if (fileMap.size === 0) {
    // nothing to show
    return;
  }

  // Set diags per file
  for (const [fsPath, diags] of fileMap) {
    diag.set(vscode.Uri.file(fsPath), diags);
  }
}

function runShell(cmd: string) {
  const terminal = vscode.window.createTerminal({ name: 'MDL' });
  terminal.show();
  terminal.sendText(cmd);
}

export function deactivate() {}

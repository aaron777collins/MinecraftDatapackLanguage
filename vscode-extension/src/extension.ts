
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
        const formatItem = new vscode.CompletionItem('pack_format 82', vscode.CompletionItemKind.Field);
        formatItem.detail = 'Pack format version';
        formatItem.documentation = 'Specifies the pack format version. Use 82 for new JavaScript-style format';
        formatItem.insertText = 'pack_format 82';
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
        
        const strItem = new vscode.CompletionItem('str', vscode.CompletionItemKind.Keyword);
        strItem.detail = 'String variable type';
        strItem.documentation = 'Declares a string variable stored in NBT data';
        strItem.insertText = 'str';
        completionItems.push(strItem);
        
        const listItem = new vscode.CompletionItem('list', vscode.CompletionItemKind.Keyword);
        listItem.detail = 'List variable type';
        listItem.documentation = 'Declares a list variable stored in multiple scoreboard objectives';
        listItem.insertText = 'list';
        completionItems.push(listItem);
      }
      
      // Control flow keywords
      const controlFlowKeywords = [
        { name: 'if', detail: 'If statement', doc: 'Conditional statement with curly braces' },
        { name: 'else if', detail: 'Else if statement', doc: 'Additional conditional branch' },
        { name: 'else', detail: 'Else statement', doc: 'Default branch for conditional' },
        { name: 'while', detail: 'While loop', doc: 'Loop that continues while condition is true' },
        { name: 'for', detail: 'For loop', doc: 'Loop that iterates over entities or values' },
        { name: 'switch', detail: 'Switch statement', doc: 'Multi-branch conditional statement' },
        { name: 'case', detail: 'Case label', doc: 'Individual case in switch statement' },
        { name: 'default', detail: 'Default case', doc: 'Default branch in switch statement' },
        { name: 'break', detail: 'Break statement', doc: 'Exit current loop or switch' },
        { name: 'continue', detail: 'Continue statement', doc: 'Skip to next iteration of loop' },
        { name: 'return', detail: 'Return statement', doc: 'Return value from function' }
      ];
      
      controlFlowKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Error handling keywords
      const errorKeywords = [
        { name: 'try', detail: 'Try block', doc: 'Start of error handling block' },
        { name: 'catch', detail: 'Catch block', doc: 'Error handling block' },
        { name: 'throw', detail: 'Throw statement', doc: 'Throw an error' }
      ];
      
      errorKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Variable declaration keywords
      const varKeywords = [
        { name: 'var', detail: 'Variable declaration', doc: 'Declare a variable' },
        { name: 'let', detail: 'Let declaration', doc: 'Declare a block-scoped variable' },
        { name: 'const', detail: 'Constant declaration', doc: 'Declare a constant variable' }
      ];
      
      varKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Import keywords
      const importKeywords = [
        { name: 'import', detail: 'Import statement', doc: 'Import module or function' },
        { name: 'from', detail: 'From clause', doc: 'Specify import source' },
        { name: 'as', detail: 'As alias', doc: 'Import with alias' }
      ];
      
      importKeywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.detail = keyword.detail;
        item.documentation = keyword.doc;
        item.insertText = keyword.name;
        completionItems.push(item);
      });
      
      // Minecraft commands
      const minecraftCommands = [
        { name: 'say', detail: 'Say command', doc: 'Send message to all players' },
        { name: 'tellraw', detail: 'Tellraw command', doc: 'Send formatted message' },
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
    const cmd = `mdl new "${name}" --name "${description}" --pack-format 82`;
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

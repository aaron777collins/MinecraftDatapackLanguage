
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
      if (linePrefix.includes('pack "') && !linePrefix.includes('min_format') && !linePrefix.includes('max_format')) {
        // Suggest min_format and max_format for pack format 82+
        const minFormatItem = new vscode.CompletionItem('min_format [82, 0]', vscode.CompletionItemKind.Field);
        minFormatItem.detail = 'Minimum pack format version (required for pack format 82+)';
        minFormatItem.documentation = 'Specifies the minimum version supported. Format: [major, minor] or just major';
        minFormatItem.insertText = 'min_format [82, 0]';
        completionItems.push(minFormatItem);
        
        const maxFormatItem = new vscode.CompletionItem('max_format [82, 1]', vscode.CompletionItemKind.Field);
        maxFormatItem.detail = 'Maximum pack format version (required for pack format 82+)';
        maxFormatItem.documentation = 'Specifies the maximum version supported. Format: [major, minor] or just major';
        maxFormatItem.insertText = 'max_format [82, 1]';
        completionItems.push(maxFormatItem);
      }
      
      // General pack declaration suggestions
      if (linePrefix.includes('pack "') && !linePrefix.includes('description')) {
        const descItem = new vscode.CompletionItem('description "Description"', vscode.CompletionItemKind.Field);
        descItem.detail = 'Pack description';
        descItem.insertText = 'description "Description"';
        completionItems.push(descItem);
      }
      
      if (linePrefix.includes('pack "') && !linePrefix.includes('pack_format')) {
        const formatItem = new vscode.CompletionItem('pack_format 82', vscode.CompletionItemKind.Field);
        formatItem.detail = 'Pack format version';
        formatItem.documentation = 'Specifies the pack format version. Use 82+ for new metadata format';
        formatItem.insertText = 'pack_format 82';
        completionItems.push(formatItem);
      }
      
      if (linePrefix.includes('pack "') && !linePrefix.includes('min_engine_version')) {
        const engineItem = new vscode.CompletionItem('min_engine_version "1.21.4"', vscode.CompletionItemKind.Field);
        engineItem.detail = 'Minimum engine version';
        engineItem.documentation = 'Specifies the minimum Minecraft engine version required';
        engineItem.insertText = 'min_engine_version "1.21.4"';
        completionItems.push(engineItem);
      }
      
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

  context.subscriptions.push(buildCmd, checkWsCmd);

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

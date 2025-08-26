
import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  const diag = vscode.languages.createDiagnosticCollection('mdl');
  context.subscriptions.push(diag);

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

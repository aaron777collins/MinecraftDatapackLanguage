
import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  const diag = vscode.languages.createDiagnosticCollection('mdl');
  context.subscriptions.push(diabuild, diag);

  vscode.workspace.onDidSaveTextDocument(doc => {
    if (doc.languageId === 'mdl') {
      runCheck(doc, diag);
    }
  });

  const buildCmd = vscode.commands.registerCommand('mdl.build', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) { return; }
    const doc = editor.document;
    if (doc.languageId !== 'mdl') { return; }
    const out = await vscode.window.showInputBox({ prompt: 'Output datapack folder', value: 'dist/datapack' });
    if (!out) { return; }
    const cmd = `mdl build --mdl "${doc.fileName}" -o "${out}"`;
    runShell(cmd);
  });

  context.subscriptions.push(buildCmd);

  // initial diagnostics
  const active = vscode.window.activeTextEditor?.document;
  if (active && active.languageId === 'mdl') {
    runCheck(active, diag);
  }
}

function runCheck(doc: vscode.TextDocument, diag: vscode.DiagnosticCollection) {
  const cmd = `mdl check "${doc.fileName}"`;
  exec(cmd, (err, stdout, stderr) => {
    const diags: vscode.Diagnostic[] = [];
    if (err) {
      // try to parse "Line X:" pattern
      const msg = stdout || stderr || String(err);
      const m = msg.match(/Line (\\d+):\\s*(.*)/);
      if (m) {
        const line = parseInt(m[1], 10) - 1;
        const range = new vscode.Range(line, 0, line, doc.lineAt(line).text.length);
        diags.push(new vscode.Diagnostic(range, m[2], vscode.DiagnosticSeverity.Error));
      } else {
        diags.push(new vscode.Diagnostic(new vscode.Range(0,0,0,1), msg, vscode.DiagnosticSeverity.Error));
      }
    }
    diag.set(doc.uri, diags);
  });
}

function runShell(cmd: string) {
  const terminal = vscode.window.createTerminal({ name: 'MDL' });
  terminal.show();
  terminal.sendText(cmd);
}

export function deactivate() {}

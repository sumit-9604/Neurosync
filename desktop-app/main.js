const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let agentProcess;
let statsProcess;

const pythonExe = process.platform === 'win32'
  ? 'python'
  : '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3';

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 700,
    minWidth: 800,
    minHeight: 600,
    frame: false,
    backgroundColor: '#0a0e14',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile('renderer/index.html');
  mainWindow.on('closed', () => { mainWindow = null; });
}

function startAgent() {
  const agentScript = path.join(__dirname, '..', 'desktop-agent', 'agent', 'main.py');
  const wsUrl = 'wss://neurosync-production-0f2b.up.railway.app/ws';

  agentProcess = spawn(pythonExe, [agentScript, '--url', wsUrl]);

  agentProcess.stdout.on('data', (data) => {
    const line = data.toString().trim();
    if (mainWindow) mainWindow.webContents.send('agent-log', line);
  });

  agentProcess.stderr.on('data', (data) => {
    const line = data.toString().trim();
    if (mainWindow) mainWindow.webContents.send('agent-log', line);
  });

  agentProcess.on('close', () => {
  if (mainWindow) mainWindow.webContents.send('agent-status', 'disconnected');
  // Auto-restart after 5 seconds
  setTimeout(startAgent, 5000);
});
}

function startStats() {
  const statsScript = path.join(__dirname, 'renderer', 'stats.py');

  statsProcess = spawn(pythonExe, [statsScript]);

  let buffer = '';
  statsProcess.stdout.on('data', (data) => {
    buffer += data.toString();
    const lines = buffer.split('\n');
    buffer = lines.pop(); // keep incomplete line
    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const stats = JSON.parse(line.trim());
        if (mainWindow) mainWindow.webContents.send('stats-update', stats);
      } catch {}
    }
  });

  statsProcess.on('close', () => {
    // Restart stats after 3s if it crashes
    setTimeout(startStats, 3000);
  });
}

app.whenReady().then(() => {
  createWindow();
  startAgent();
  startStats();
});

app.on('window-all-closed', () => {
  if (agentProcess) agentProcess.kill();
  if (statsProcess) statsProcess.kill();
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.on('window-close', () => app.quit());
ipcMain.on('window-minimize', () => mainWindow?.minimize());
ipcMain.on('window-maximize', () => {
  if (mainWindow?.isMaximized()) mainWindow.unmaximize();
  else mainWindow?.maximize();
});
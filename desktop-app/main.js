const { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let tray;
let agentProcess;

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
    icon: path.join(__dirname, 'assets', 'icon.png'),
  });

  mainWindow.loadFile('renderer/index.html');

  mainWindow.on('closed', () => { mainWindow = null; });
}

function startAgent() {
  const pythonExe = process.platform === 'win32' ? 'python' : '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3';
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

  agentProcess.on('close', (code) => {
    if (mainWindow) mainWindow.webContents.send('agent-status', 'disconnected');
  });
}

app.whenReady().then(() => {
  createWindow();
  startAgent();
});

app.on('window-all-closed', () => {
  if (agentProcess) agentProcess.kill();
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.on('window-close', () => app.quit());
ipcMain.on('window-minimize', () => mainWindow?.minimize());
ipcMain.on('window-maximize', () => {
  if (mainWindow?.isMaximized()) mainWindow.unmaximize();
  else mainWindow?.maximize();
});
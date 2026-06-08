const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onAgentLog: (cb) => ipcRenderer.on('agent-log', (_, data) => cb(data)),
  onAgentStatus: (cb) => ipcRenderer.on('agent-status', (_, data) => cb(data)),
  closeWindow: () => ipcRenderer.send('window-close'),
  minimizeWindow: () => ipcRenderer.send('window-minimize'),
  maximizeWindow: () => ipcRenderer.send('window-maximize'),
});

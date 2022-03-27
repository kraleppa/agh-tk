const { contextBridge, ipcRenderer } = require("electron");

const selectFolder = () => ipcRenderer.invoke("dialog:openDirectory");

contextBridge.exposeInMainWorld("api", {
  selectFolder,
});

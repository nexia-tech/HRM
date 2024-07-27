const { app, BrowserWindow,ipcMain } = require("electron");
const path = require('path');

const ip = ipcMain

function ElectronMainMethod() {
  const launchWindow = new BrowserWindow({
    title: "Nexia HRM",
    width: 1300,
    height: 600,
    minWidth: 1000,
    minHeight:560,
    autoHideMenuBar: true,
    fullscreenable:false,

    frame: false, // Remove the default window frame
    webPreferences: {
      nodeIntegration: true, // Enable Node integration if needed
      contextIsolation: true, // Disable context isolation if Node integration is enabled
      devTools: true,
      preload: path.join(__dirname,'preload.js')
    },
    
  });

  const appUrl = "http://127.0.0.1:8000/";
  // const appUrl = "http://ec2-34-226-12-37.compute-1.amazonaws.com/"

  launchWindow.loadURL(appUrl);

  ip.on('minimizeApp',()=>{
    console.log("workign 1");
    launchWindow.minimize()
  })
  
  ip.on('maximizeApp',()=>{
    console.log("workign 2");
    launchWindow.maximize()
  })

}

app.whenReady().then(ElectronMainMethod)
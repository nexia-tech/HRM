const { app, BrowserWindow } = require("electron");


function ElectronMainMethod() {
  const launchWindow = new BrowserWindow({
    title: "Nexia HRM",
    width: 1300,
    height: 600,
    minWidth: 1000,
    minHeight:560,
    autoHideMenuBar: true,
    frame: false,// Enable the default window frame
    webPreferences: {
      nodeIntegration: true,// Enable Node integration if needed
      contextIsolation: true, // Disable context isolation if Node integration is enabled
    },
    
  });

  const appUrl = "http://127.0.0.1:8000/";
  
  launchWindow.loadURL(appUrl);

  
}

app.whenReady().then(ElectronMainMethod)
// const appUrl = "http://ec2-34-226-12-37.compute-1.amazonaws.com/"

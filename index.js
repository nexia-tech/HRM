const { app, BrowserWindow } = require("electron");


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
      contextIsolation: false, // Disable context isolation if Node integration is enabled
    },
    
  });

  const appUrl = "http://127.0.0.1:8000/";
  // const appUrl = "http://ec2-34-226-12-37.compute-1.amazonaws.com/"

  launchWindow.loadURL(appUrl);


}

app.whenReady().then(ElectronMainMethod)
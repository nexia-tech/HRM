const { app, BrowserWindow } = require("electron");

function ElectronMainMethod() {
  const launchWindow = new BrowserWindow({
    title: "Nexia HRM",
    width: 1024,
    height: 800,
  });

  const appUrl = "http://127.0.0.1:8000/";
  // const appUrl = "http://ec2-34-226-12-37.compute-1.amazonaws.com/"

  launchWindow.loadURL(appUrl);
}

app.whenReady().then(ElectronMainMethod)
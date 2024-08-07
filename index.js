const { app, BrowserWindow, Tray, Menu } = require("electron");
const path = require("path");

let tray = null;
let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    title: "Nexia HRM",
    width: 1300,
    height: 600,
    minWidth: 1000,
    minHeight: 560,
    autoHideMenuBar: true,
    frame: true, // Enable the default window frame
    webPreferences: {
      nodeIntegration: true, // Enable Node integration if needed
      contextIsolation: false, // Disable context isolation if Node integration is enabled
    },
  });

  const appUrl = "http://127.0.0.1:8000/";
  mainWindow.loadURL(appUrl);


}

// app.on('ready', () => {
//   createWindow();

//   tray = new Tray(path.join(__dirname, 'tray-icon.png')); // Provide a path to your tray icon

//   const contextMenu = Menu.buildFromTemplate([
//     { label: 'Show App', click: () => { mainWindow.show(); } },
//     { label: 'Quit', click: () => { app.isQuiting = true; app.quit(); } }
//   ]);

//   tray.setToolTip('Nexia HRM');
//   tray.setContextMenu(contextMenu);

//   tray.on('click', () => {
//     mainWindow.show();
//   });
// });

app.whenReady().then(createWindow)
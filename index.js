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
    frame: true, // Remove the default window frame
    webPreferences: {
      nodeIntegration: true, // Enable Node integration if needed
      contextIsolation: false, // Disable context isolation if Node integration is enabled
    },
  });

  const appUrl = "http://127.0.0.1:8000/";
  mainWindow.loadURL(appUrl);

  mainWindow.on('minimize', (event) => {
    event.preventDefault();
    mainWindow.hide();
  });

  mainWindow.on('close', (event) => {
    if (!app.isQuiting) {
      event.preventDefault();
      mainWindow.hide();
    }

    return false;
  });
}

app.on('ready', () => {
  createWindow();

  tray = new Tray(path.join(__dirname, 'tray-icon.png')); // Provide a path to your tray icon

  const contextMenu = Menu.buildFromTemplate([
    { label: 'Show App', click: () => { mainWindow.show(); } },
    { label: 'Quit', click: () => { app.isQuiting = true; app.quit(); } }
  ]);

  tray.setToolTip('Nexia HRM');
  tray.setContextMenu(contextMenu);

  tray.on('click', () => {
    mainWindow.show();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// const appUrl = "http://ec2-34-226-12-37.compute-1.amazonaws.com/"
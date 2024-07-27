const {ipcRenderer} = require('electron');

const ipc = ipcRenderer


minWindowBtn.addEventListener('click',()=>{
    ipc.send('minimizeApp')
  })

  maxWindowBtn.addEventListener('click',()=>{
    console.log('max');
    ipc.send('maximizeApp')
  })
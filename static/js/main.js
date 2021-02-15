// create socketio connection
const socket = io.connect('http://' + document.domain + ':' + location.port);

// update dial values when message comes on socket
socket.on('dial_update',  function (msg)  {
    const dial = document.getElementById(msg.name);
    dial.setAttribute("data-value", parseFloat(msg.value));
});

// send stop/start command to server on clicking button
const control_button = document.querySelector('.control_button');
control_button.addEventListener('click', ()=> {
  socket.emit('control', {data: 'toggle'});
});


// lights to show connection
let connectingLightsTimer;
socket.on('status',  function (msg)  {

  // lights blink consecutively
  if (msg == 'connecting'){
    connectingLightsTimer = setInterval(connectingLights, 1000);
  }

  // lights stay on
  else if (msg == 'connected'){
    clearInterval(connectingLightsTimer);
    setTimeout(connectedLights, 1000);
  }

  // lights turn off
  else if (msg == 'disconnected'){
    disconnectedLights();
  }
});


function connectedLights(){
  const lights = document.querySelectorAll('.light');
  lights.forEach((light) => {
    light.style.background = 'red';
  });
}

function disconnectedLights(){
  const lights = document.querySelectorAll('.light');
  lights.forEach((light) => {
    light.style.background = 'black';
  });
}

function connectingLights(){
  const lights = document.querySelectorAll('.light');
  lights.forEach((light, index)=>{
    setTimeout(toggleLight, 250*index, light);
    setTimeout(toggleLight, 250*index+250, light);
  });
}

function toggleLight(light){
  light.style.background == 'red' ? light.style.background = 'black' :light.style.background = 'red';
}

var callid = '', is_muted = false, is_started = false;

function pageload() { // Initializes the sdk and logs in the user.
  CS.call.onMessage(handleCallFromIML);

  // configuration parameters.
  let config = {
    appId: "pid_413c1c38_8bad_4539_86f3_afa7cdbdbb30"         // <----------- Update the projectid here-----------
  };

  // callback called at the end of initialization to notify success or failure.
  function callback(ret, resp) {
    if (ret == 200) {
      console.log("SDK " + CS.version + " initialized ");

      // Initiate login request
      CS.login("Amar", "amarsaiteja", function (err, resp) {                   // <----------- Update the user credentials here-----------
        if (err == 200) {
          console.log("Login succesful");
          //document.getElementById("startbtn").disabled = false;
        }
        else {
          console.log("login failed with response code " + err + " reason " + resp);
        }
      });
    }
  }
  CS.initialize(config, callback);
}

function handleCallFromIML(msgType, resp) {
  switch (msgType) {
    case "OFFER":     /* incoming offer from remote party */
      break;
    case "RINGING":   /* ringing */
      console.log("calling");
      //document.getElementById("startbtn").innerHTML =  'Call';
      break;
    case "ANSWERED":  /* call answer */
      console.log("answered");
      //setTimeout(() => { console.log('Done'); endCall();}, 180000);
      // document.getElementById("startbtn").innerHTML =  'End Call';
      break;
    case "END":       /* call end */
      console.log("ending call");
      //document.getElementById("startbtn").innerHTML = 'Call';
      break;
  }
}

function callbackFunc(code, resp) {
  if (code != 200) {
    alert("call failed with response code " + code + " reason " + resp);
  }
  else {
    alert("call success with response code " + code + " reason " + resp);
  }
}

function endCall() {
  CS.call.end(callid, "Bye", function (ret, resp) {
    if (ret == 200)
      //CS.call.saveRecording(callid, 'recording.wav');
      console.log("call end successfully");
  });
  //CS.call.saveRecording(callid, 'recording.wav');
}


/* Initiate outbound call (call remote party) */
function start(destnum) {
  destnum = '+' + destnum
  console.log("destination no is:" + destnum);
  if (is_started == false) {
    console.log('done');
    is_started = true;
    callid = CS.call.startPSTNCall(destnum, "localVideo", "remoteVideo", function callbackFunc() { }, true);
    //document.getElementById("startbtn").innerHTML =  'End call';
  } else {
    /* End ongoing call */
    //document.getElementById("startbtn").innerHTML = 'Call';
    is_started = false;
    CS.call.end(callid, "Bye", function (ret, resp) {
      if (ret == 200)
        CS.call.saveRecording(callid, 'recording.wav');
      console.log("call end successfully");
    });

  }
}

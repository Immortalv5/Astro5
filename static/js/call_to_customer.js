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
          document.getElementById("startbtn").disabled = false;
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
      //document.getElementById("startbtn").innerHTML =  'Call';
      break;
    case "ANSWERED":  /* call answer */
      setTimeout(() => { console.log('Done'); endCall();}, 180000);
      // document.getElementById("startbtn").innerHTML =  'End Call';
      break;
    case "END":       /* call end */
      console.log("call end");
      document.getElementById("startbtn").innerHTML = 'Call';
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
    document.getElementById("startbtn").innerHTML = 'Call';
    is_started = false;
    CS.call.end(callid, "Bye", function (ret, resp) {
      if (ret == 200)
        CS.call.saveRecording(callid, 'recording.wav');
      console.log("call end successfully");
    });

  }
}

function call_to(phone_number, user_number){



  //CS.initialize({appId:"mmOwzQUOqkEpmDZdDTDm"}, function callback(ret, resp) {if (ret == 200) { console.log("SDK "+CS.version+" initialize "); }});
//
//   var data = {
//     projectid :  'pid_7a183e41_bcff_4aa0_80a2_6f0e9dd7c174',
//     authtoken : '5d2c949f_3006_4109_a407_bbc76946dca2',
//     user :  'Amar',
//     pass :  'amar',
//    // recipient : 'Suvi' ,
//    // message :  'Hi',
//    // msgType :  1,
//    // ct :  'text/plain',
//   }
//
//
//
//   var proxyURL = 'https://c3d67f65a38b.ngrok.io'//'https://astro5.herokuapp.com';
//   var requestURL = "https://proxy.vox-cpaas.com/api/user";
//
//   var request = new XMLHttpRequest();
//   request.open('POST', requestURL, true);
//   request.setRequestHeader("Content-type", "application/json");
//   //request.setRequestHeader('charser', 'UTF-8')
//   request.setRequestHeader('Access-Control-Allow-Origin', proxyURL);
//   request.responseType = 'json';
//
//   request.onload = function() {
//     var data = request.response;
//     console.log(data);
//     //document.querySelector('pre').textContent = JSON.stringify(data, null, 2);
//   }
//
//   request.send('authtoken=5d2c949f_3006_4109_a407_bbc76946dca2&projectid=pid_7a183e41_bcff_4aa0_80a2_6f0e9dd7c174&username=sai&password=amar');
// // And the ajax request I am making with it:
// // $.ajax({
// //   type: "POST",
// //   url: 'https://api.vox-cpaas.com/user',
// //   data: data,
// //   headers: {
// //     "Access-Control-Allow-Origin": 'https://7e69bc60b726.ngrok.io',
// //   },
// // });
//
//   console.log('astrologers:',phone_number);
//   console.log('user:',user_number)
//
//   send_data(data)
}

function send_data(data){
  console.log(data)
}

function call_to(phone_number, user_number){

  CS.initialize({appId:"mmOwzQUOqkEpmDZdDTDm"}, function callback(ret, resp) {if (ret == 200) { console.log("SDK "+CS.version+" initialize "); }});

  var data = {
    projectid :  'pid_7a183e41_bcff_4aa0_80a2_6f0e9dd7c174',
    authtoken : '5d2c949f_3006_4109_a407_bbc76946dca2',
    user :  'Amar',
    pass :  'amar',
   // recipient : 'Suvi' ,
   // message :  'Hi',
   // msgType :  1,
   // ct :  'text/plain',
  }

// And the ajax request I am making with it:
$.ajax({
  type: "POST",
  url: 'https://api.vox-cpaas.com/user',
  data: data,
  headers: {
    "Access-Control-Allow-Origin": 'https://7e69bc60b726.ngrok.io',
  },
});

  console.log('astrologers:',phone_number);
  console.log('user:',user_number)

}

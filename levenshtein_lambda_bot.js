'use strict';
var https = require('https');
var PAGE_TOKEN = "PAGE_TOKEN";
var VERIFY_TOKEN = "VERIFY_TOKEN";
exports.handler = (event, context, callback) => {
  // process GET request
  if(event.params && event.params.querystring){
    var queryParams = event.params.querystring;
 
    var rVerifyToken = queryParams['hub.verify_token']
 
    if (rVerifyToken === VERIFY_TOKEN) {
      var challenge = queryParams['hub.challenge']
      callback(null, parseInt(challenge))
    }else{
      callback(null, 'Error, wrong validation token');
    }
 
  // process POST request
  }else{
    var messagingEvents = event.entry[0].messaging;
    for (var i = 0; i < messagingEvents.length; i++) {
      var messagingEvent = messagingEvents[i];
    
      var sender = messagingEvent.sender.id;
      if (messagingEvent.message && messagingEvent.message.text) {
        var text = messagingEvent.message.text; 
        console.log("Received message: " + text);
        
        sendTextMessage(sender, "'" + text.substring(0, 50) + "' has " + levenshtein(text.toLowerCase(),"yeet") + " yeet levels");
        
        callback(null, "Done")
      }
    }
 
    callback(null, event);
  }
};
function sendTextMessage(senderFbId, text) {
  var json = {
    recipient: {id: senderFbId},
    message: {text: text},
  };
  var body = JSON.stringify(json);
  var path = '/v2.6/me/messages?access_token=' + PAGE_TOKEN;
  var options = {
    host: "graph.facebook.com",
    path: path,
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  };
  var callback = function(response) {
    var str = ''
    response.on('data', function (chunk) {
      str += chunk;
    });
    response.on('end', function () {
 
    });
  }
  var req = https.request(options, callback);
  req.on('error', function(e) {
    console.log('problem with request: '+ e);
  });
 
  req.write(body);
  req.end();
}

var levenshtein = function(a, b) {
  if (a.length === 0) return b.length
  if (b.length === 0) return a.length

  var matrix = []

  // increment along the first column of each row
  var i
  for (i = 0; i <= b.length; i++) {
    matrix[i] = [i]
  }

  // increment each column in the first row
  var j
  for (j = 0; j <= a.length; j++) {
    matrix[0][j] = j
  }

  // Fill in the rest of the matrix
  for (i = 1; i <= b.length; i++) {
    for (j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1]
      } else {
        matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, // substitution
                                Math.min(matrix[i][j - 1] + 1, // insertion
                                         matrix[i - 1][j] + 1)) // deletion
      }
    }
  }

  return matrix[b.length][a.length]
}

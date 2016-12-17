import $ from 'jquery';
import BASE_URL from './config';

let loggedin = false;
let userinfo = {};

// TODO: time check
function checkIfLoggedin(callback) {
  $.get(BASE_URL + 'userinfo').then(d => {
    if (d.success) {
      loggedin = true;
      userinfo = d;
    } else {
      loggedin = false;
    }

    callback(loggedin, userinfo);
  });
}

chrome.runtime.onMessage.addListener(
  (request, _, callback) => {
    if (request.message == "AJAX") {
      $.ajax(request.request).then(d => {
        loggedin = true;
        callback(d);
      },
      () => {
        loggedin = false;
      });
    } else if (request.message == "isLoggedin") {
      checkIfLoggedin(callback);
    }

    return true;
  }
);
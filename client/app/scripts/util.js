import $ from 'jquery';
import { URL_BASE } from './config';

export function _start(main) {
  chrome.runtime.sendMessage({message: 'isLoggedin'}, (r, info) => {
    if (!r) {
      let w = window.open(`${URL_BASE}login-google`, 'Login to conspire', 'width=600, height=600, menubar=no, toolbar=no, scrollbars=yes');
    } else {
      main();
    }
  });
}
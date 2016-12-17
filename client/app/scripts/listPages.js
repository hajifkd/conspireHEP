import $ from 'jquery';
import { URL_BASE } from './config';
import React from 'react';
import ReactDOM from 'react-dom';
import { ReactionButtonGroup, CHOISES } from './ReactionButtonGroup';

const ABS_REGEXP = new RegExp('^http.*/abs/(.+)$');

function main() {
  let headers = $('dt > span.list-identifier');
  let urls = headers.find('a:first-child').map((_, a) => a.href);
  let arxiv_ids = $.makeArray(urls.map((_, u) => u.match(ABS_REGEXP)[1]));

  chrome.runtime.sendMessage({
    message: 'AJAX',
    request: {
      type: 'POST',
      url: `${URL_BASE}list/reactions`,
      contentType: 'application/json',
      dataType : 'JSON',
      data: JSON.stringify({'arxiv_ids': arxiv_ids})
    }
  }, p => {
    for (let arxiv_id in p.reactions) {
      let index = arxiv_ids.indexOf(arxiv_id);
      let jqDom = $(headers[index]);
      let div = $("<div style='display: inline'>");
      jqDom.after(div).after('&nbsp;');

      let numbers = {};

      for (let k of CHOISES) {
        numbers[k] = 0;
      }

      for (let k of p.reactions[arxiv_id].reactions) {
        if (!numbers[k]) numbers[k] = 1;
        else numbers[k]++;
      }

      ReactDOM.render(<ReactionButtonGroup
                          numbers={numbers}
                          myself={p.reactions[arxiv_id].myself}
                          arxivId={arxiv_id} />, div[0]);
    }
  });
}

$(main);
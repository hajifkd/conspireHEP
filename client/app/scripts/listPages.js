import $ from 'jquery';
import { URL_BASE } from './config';
import React from 'react';
import ReactDOM from 'react-dom';
import { ReactionButtonGroup } from './ReactionButtonGroup';
import { _start } from './utils';


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

      ReactDOM.render(<ReactionButtonGroup
                          reactions={p.reactions[arxiv_id].reactions}
                          myself={p.reactions[arxiv_id].myself}
                          arxivId={arxiv_id} />, div[0]);
      
      div.after(`<span class="comment_size">💬${p.reactions[arxiv_id].comment_size}</span>`)
    }
  });
}

$(_start.bind(undefined, main));
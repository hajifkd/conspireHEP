import $ from 'jquery';
import { URL_BASE } from './config';
import React from 'react';
import ReactDOM from 'react-dom';
import { ReactionButtonGroup } from './ReactionButtonGroup';
import { CommentsField } from './CommentsField';
import { _start } from './utils';

const ABS_REGEXP = new RegExp('^http.*/abs/(.+)$');


function main() {
  let arxiv_id = location.href.match(ABS_REGEXP)[1];

  chrome.runtime.sendMessage({
    message: 'AJAX',
    request: {
      type: 'POST',
      url: `${URL_BASE}get/reactions`,
      contentType: 'application/json',
      dataType : 'JSON',
      data: JSON.stringify({'arxiv_id': arxiv_id})
    }
  }, p => {
    let jqDom = $("div.authors");
    let div = $("<div>");
    jqDom.append(div);

    ReactDOM.render(<ReactionButtonGroup
                        reactions={p.reactions}
                        myself={p.myself}
                        arxivId={arxiv_id} />, div[0]);
  });

  let commentArea = $("<div>");
  $("div.endorsers").after(commentArea);

  ReactDOM.render(<CommentsField
                        arxivId={arxiv_id} />, commentArea[0]);
}

$(_start.bind(undefined, main));
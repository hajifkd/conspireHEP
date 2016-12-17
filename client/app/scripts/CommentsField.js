import React from 'react';
import { URL_BASE } from './config';

export class CommentsField extends React.Component {
  constructor(props) {
    super(props);

    this.state = {newComment: '', comments: []};
  
    chrome.runtime.sendMessage({
      message: 'AJAX',
      request: {
        type: 'POST',
        url: `${URL_BASE}get/comments`,
        contentType: 'application/json',
        dataType : 'JSON',
        data: JSON.stringify({arxiv_id: props.arxivId})
      }
    }, p => {
      this.setState({comments: p.comments})
    });
  }

  onClick() {
    let comment = this.state.newComment;
    chrome.runtime.sendMessage({
      message: 'AJAX',
      request: {
        type: 'POST',
        url: `${URL_BASE}add/comment`,
        contentType: 'application/json',
        dataType : 'JSON',
        data: JSON.stringify({
          arxiv_id: this.props.arxivId,
          comment: comment
        })
      }
    }, r => {
      if (!r.success) return;

      let comments = this.state.comments.slice();
      comments.push({username: 'Me', comment: comment});
      this.setState({newComment: '', comments: comments});
    });

  }

  handleChange(event) {
    this.setState({newComment: event.target.value});
  }

  render() {
    return (
      <div className="commentbox">
        <h2>Comments on <span className='ctitle'>{this.props.arxivId}</span></h2>
        <div className='comments'>
          {this.state.comments.map((c, i) => {
            return (<div className="comment" key={i}>
                      <span className='comment_id'>{i + 1}</span>:
                      <span className="created_at">{c.created_at}</span>
                      <span className='name'>
                        {c.username}
                        <a href={`https://inspirehep.net/search?cc=HepNames&p=${c.username}`}>(inspire search)</a>
                      </span> wrote:
                      <div className="comment_text"><pre>{c.comment}</pre></div>
                    </div>);
          })}
        </div>
        <textarea cols='50' rows='5'
          value={this.state.value}
          onChange={this.handleChange.bind(this)}>
        </textarea><br />
        <input type='submit' value='Submit' onClick={this.onClick.bind(this)}/>
      </div>
    );
  }
}
import React from 'react';
import { ReactionButton } from './ReactionButton';
import { URL_BASE } from './config';

const emoji = ["👍", "👎"];
export const CHOISES = ["like", "dislike"];

export class ReactionButtonGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      numbers: CHOISES.map(k => props.numbers[k]),
      myself: CHOISES.indexOf(props.myself)
    };
  }

  onClick(i) {
    let reaction = this.state.myself == i ? '' : CHOISES[i];
    
    chrome.runtime.sendMessage({
      message: 'AJAX',
      request: {
        type: 'POST',
        url: `${URL_BASE}add/reaction`,
        contentType: 'application/json',
        dataType : 'JSON',
        data: JSON.stringify({
          arxiv_id: this.props.arxivId,
          reaction: reaction
        })
      }
    }, r => {
      if (!r.success) return false;
      
      if (this.state.myself == i) {
        this.setState({
          numbers: this.state.numbers.map((n, j) => j == i ? n - 1 : n),
          myself: -1,
        });
      } else {
        this.setState({
          numbers: this.state.numbers.map((n, j) => {
            if (i == j) return n + 1;
            else if (this.state.myself == j) return n - 1;
            else return n;
          }),
          myself: i
        });
      }
    });

  }

  render() {
    return (
      <span>
        {this.state.numbers.map((n, i) => {
          console.log(this.state);
          console.log(i);
          console.log(this.state.myself);
          return (<ReactionButton emoji={emoji[i]}
            clicked={this.state.myself == i}
            number={n}
            onClick={this.onClick.bind(this, i)}
            key={i} />);
        })}
      </span>
    );
  }
}
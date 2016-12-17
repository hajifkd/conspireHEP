import React from 'react';
import { ReactionButton } from './ReactionButton';
import { URL_BASE } from './config';

const emoji = ["👍", "👎", "🔖"];
export const choises = ["like", "dislike", "read_later"];

export class ReactionButtonGroup extends React.Component {
  constructor(props) {
    super(props);
    let numbers = choises.map(_ => 0);

    for (let v of props.reactions) {
      let index = choises.indexOf(v);
      if (index < 0) continue;
      numbers[index]++;
    }

    this.state = {
      numbers: numbers,
      myself: choises.indexOf(props.myself)
    };
  }

  onClick(i) {
    let reaction = this.state.myself == i ? '' : choises[i];
    
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
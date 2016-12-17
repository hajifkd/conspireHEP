import React from 'react';

export class ReactionButton extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <span>
        <span className={this.props.clicked ? "emoji" : "emoji emoji-disabled"}
          onClick={this.props.onClick}>
          {this.props.emoji}
        </span>
        <span className="num_count">
          {this.props.number}
        </span>
      </span>
    );
  }
}
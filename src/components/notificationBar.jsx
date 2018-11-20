import React, { Component } from 'react';

export default class NotificationBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hide: false,
    };
    this.close = this.close.bind(this);
  }
  
  close() {
    this.setState({hide: true});
  };
  
  render() {
    return (
      <React.Fragment>
        { this.state.hide ? '' :
          <div className="alert" role="alert" id="message-bar" style={{
            display: 'none',
            position: 'relative'
          }}
          onClick={this.close}
          
          >
            
            <span id="message-bar-close-button" style={{
              position: 'absolute',
              top: '1px',
              right: '10px',
              cursor: 'pointer'
            }} onClick={this.close}
            >x</span>
            
            <p id="message-bar-text" style={{
              display: 'none',
              marginBottom: 0
            }}/>
          
          </div>
        }
      </React.Fragment>
    )
  }
}

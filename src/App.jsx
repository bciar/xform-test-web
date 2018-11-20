/* XFormTest Web
*
* Resources
* - React Dropzone
*   - https://react-dropzone.js.org/
*   - https://github.com/react-dropzone/react-dropzone/
*/
import React, { Component } from 'react';
import Dropzone from 'react-dropzone';
import request from 'superagent';

import Header from './components/header';
import NotificationBar from './components/notificationBar';

import './App.css';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      success: "",
      error: "",
      warnings: ""
      
    };
    this.closeSuccess = this.closeSuccess.bind(this);
    this.closeWarnings = this.closeWarnings.bind(this);
    this.closeError = this.closeError.bind(this);
  }
  closeSuccess() {
    this.setState({success: ""});
  };
  closeWarnings() {
    this.setState({warnings: ""});
  };
  closeError() {
    this.setState({error: ""});
  };
  
  render() {
    return (
      <div className="App">
        <Header/>
        <div className="container" style={{textAlign: 'center'}}>
          <NotificationBar/>
          
          <br/>
          
          <Dropzone
            className="dropzone"
            accept='.xml,.xls,.xlsx'
            onDrop={ (acceptedFiles) => {
              let messageBar = document.querySelector('#message-bar');
              let messageTxt = document.querySelector('#message-bar-text');
              
              if (acceptedFiles.length > 1) {
                messageBar.classList.remove('alert-info');
                messageBar.classList.remove('alert-success');
                messageBar.classList.add('alert-danger');
                messageBar.style.display = 'inherit';
                if (messageTxt) {
                  messageTxt.style.display = 'inherit';
                  messageTxt.innerHTML = 'Please only select one file at a time.';
                }
              } else if (acceptedFiles.length === 1) {
                messageBar.classList.remove('alert-danger');
                messageBar.classList.remove('alert-success');
                messageBar.classList.add('alert-info');
                messageBar.innerHTML = 'Processing...';
                messageBar.style.display = 'inherit';
                
                const file = acceptedFiles[0];
                // TODO: get from env
                // request.post('http://localhost:5000/upload')
                // request.post('http://xform-test-api.pma2020.org/upload')
                // request.post('http://xform-test-api-staging.pma2020.org/upload')
                // request.post('http://xform-test-api-staging.herokuapp.com/upload')
                request.post('http://xform-test-api.herokuapp.com/upload')
                .attach(file.name, file)
                .then(response => {
                  const data = JSON.parse(response.text);
                  
                  if (data.error) {
                    messageBar.classList.remove('alert-info');
                    messageBar.classList.remove('alert-success');
                    messageBar.classList.add('alert-danger');
                    messageBar.style.display = 'inherit';
                    if (messageTxt) {
                      messageTxt.innerHTML = data.error;
                      messageTxt.style.display = 'inherit';
                    }
                  }
                  
                  messageBar.style.display = 'none';
                  if (messageTxt)
                    messageTxt.style.display = 'none';
                  this.setState({
                    success: data.success,
                    error: data.error,
                    warnings: data.warnings,
                  })
                });
              }
            }
          }>
            <form action="/upload">
              <div className="dz-message needsclick" style={{
                textAlign: 'center'
              }}>
                <label htmlFor="file-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="17"
                       viewBox="0 0 20 17">
                    <path d="M10 0l-5.2 4.9h3.3v5.1h3.8v-5.1h3.3l-5.2-4.9zm9.3 11.5l-3.2-2.1h-2l3.4 2.6h-3.5c-.1 0-.2.1-.2.1l-.8 2.3h-6l-.8-2.2c-.1-.1-.1-.2-.2-.2h-3.6l3.4-2.6h-2l-3.2 2.1c-.4.3-.7 1-.6 1.5l.6 3.1c.1.5.7.9 1.2.9h16.3c.6 0 1.1-.4 1.3-.9l.6-3.1c.1-.5-.2-1.2-.7-1.5z"/>
                  </svg>
                  <span> Click here or drop an XLSForm (xls, xlsx) or XForm (xml)
                    file to run tests.</span>
                </label>
              </div>
            </form>
          </Dropzone>
  
          { this.state.success ?
          <div className="alert alert-success message-bar"
               style={{position: 'relative'}}>
            <span style={{position: 'absolute',
                top: '1px',
              right: '10px',
              cursor:'pointer'
            }} onClick={this.closeSuccess}
            >x</span>
            <div style={{textAlign: 'left'}}>
              <pre style={{marginBottom: 0}}>{ this.state.success }</pre>
            </div>
          </div> : '' }
            
  
          { this.state.warnings ?
          <div className="alert alert-warning message-bar" style={{
            position: 'relative'
          }}>
            <span style={{position: 'absolute',
              top: '1px',
              right: '10px',
              cursor: 'pointer'
            }} onClick={this.closeWarnings}
            >x</span>
            <div style={{textAlign: 'left'}}>
              <pre style={{marginBottom: 0}}>{ this.state.warnings }</pre>
            </div>
          </div> : '' }
  
          { this.state.error ?
          <div className="alert alert-danger message-bar"
               style={{position: 'relative'}}>
            <span style={{position: 'absolute',
              top: '1px',
              right: '10px',
              cursor: 'pointer'
            }} onClick={this.closeError}
            >x</span>
            
            <div style={{textAlign: 'left'}}>
              <pre style={{marginBottom: 0}}>{ this.state.error }</pre>
            </div>
          </div> : '' }
          
          <p style={{fontSize: '0.8em'}}>
            Are you new here?
            <a href="http://xform-test-docs.pma2020.org">&nbsp;
            Check out the docs!
            </a>
          </p>
        </div>
        
      </div>
    )
  }
}

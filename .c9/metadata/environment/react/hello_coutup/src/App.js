{"filter":false,"title":"App.js","tooltip":"/react/hello_coutup/src/App.js","undoManager":{"mark":0,"position":0,"stack":[[{"start":{"row":0,"column":0},"end":{"row":25,"column":0},"action":"remove","lines":["import React, { Component } from 'react';","","class App extends Component {","  state = {","    hello: 'Hello App.js!!'","}","","","handleChange = () => {","  this.setState({","    hello: 'Bye App.js!!'","  })","}","","render() {","  return (","    <div className=\"App\">","      <div>{this.state.hello}</div>","      <button onClick={this.handleChange}>Click me!</button>","      </div>","    )","  }","}","","export default App;",""],"id":2},{"start":{"row":0,"column":0},"end":{"row":24,"column":19},"action":"insert","lines":["import React, { Component } from 'react';","","class App extends Component {","  state = {","    count : 0","}","","","countup = () => {","  this.setState({","    count : this.state.count + 1","  })","}","","render() {","  return (","    <div className=\"App\">","      <div>{this.state.count}</div>","      <button onClick={this.countup}>count up!</button>","      </div>","    )","  }","}","","export default App;"]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":24,"column":19},"end":{"row":24,"column":19},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1688091596009,"hash":"fb3a96465c8dc3715a3536a0e2b26b5c0dd531fa"}
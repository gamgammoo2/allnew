// import React from 'react';
// import Hello from './Hello';
// import './App.css';

// function App() {
//   const name = "react";
//   const style = {
//     backgroundColor : "black",
//     color : 'aqua',
//     fontSize : 24,
//     padding : '1rem'
//   }
//   return (
//     <div>
//     <Hello />
//     <div style={style}>{name}</div>
//     <div className="gray-box"></div>
//     </div>
//     )
// }

// export default App;



// import React from 'react';
// import Hello from './Hello';

// function App() {
//   return (
//     <Hello name="react" color="red" />
//     )
// }

// export default App;


// import React from 'react';
// import Hello from './Hello';

// function App() {
//   return (
//     <>
//     <Hello name="react" color="red" />
//     <Hello color ="pink" />
//     </>
//     )
// }

// export default App;

import React from 'react';
import Hello from './Hello';
import Wrapper from './Wrapper';

function App() {
 return(
  <Wrapper>
  <Hello name="react" color="red" />
  <Hello color="pink"/>
  </Wrapper>
  )
   /* comment */
}

export default App;
 
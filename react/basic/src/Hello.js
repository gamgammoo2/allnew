// import React from 'react';

// function Hello(props) {
//     return <div style={{color:props.color}}>Hello~!! {props.name}</div>
// }

// export default Hello;


// import React from 'react';

// function Hello({name,color}) {
//     return <div style={{color}}>Hello~!! {name}</div>
// }

// export default Hello;


import React from 'react';

function Hello({name, color }) {
    return <div style={{ color }}>Hello~!! { name } </div>
}

Hello.defaultProps = {
    name: 'NoName'
}


export default Hello;

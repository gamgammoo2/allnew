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

// import React from 'react';
// import Hello from './Hello';
// import Wrapper from './Wrapper';

// function App() {
//  return(
//   <Wrapper>
//   <Hello name="react" color="red" />
//   <Hello color="pink"/>
//   </Wrapper>
//   )
//    /* comment */
// }

// export default App;

// import React from 'react';
// import Hello from './Hello';
// import Wrapper from './Wrapper';

// function App() {
//   return (
//     <Wrapper>
//     <Hello name="react" color="red" isSpecial={true} />
//     <Hello color="pink" />
//     </Wrapper>
//     )
// }

// export default App;

// import React from 'react';
// import InputSample from './InputSample';

// function App() {
//   return (
//     <InputSample />
//   )
// }

// export default App;

import React, { useRef, useState } from 'react';
import UserList from './UserList';
import CreateUser from './CreateUser';

function App() {
  const [inputs, setInputs] = useState({
    username: '',
    email: ''
  })

  const { username, email } = inputs;

  const onChange = e => {
    const { name, value } = e.target;
    setInputs({
      ...inputs,
      [name]: value
    })
  }

  const [users, setUsers] = useState(
    [
      {
        id: 1,
        username: 'developer',
        email: 'public.developer@gamil.com'
      },
      {
        id: 2,
        username: 'tester',
        email: 'public.tester@gmail.com'
      },
      {
        id: 3,
        username: 'yoon',
        email: 'public.yoon@gmail.com'
      }
    ]
  )

  const nextId = useRef(4);
  const onCreate = () => {
    const user = {
      id: nextId.current,
      username,
      email
    }

    setUsers(users.concat(user));
    setInputs({
      username: '',
      email: ''
    })

    nextId.current += 1;
  }

  const onRemove = id => {
    setUsers(users.filter(user => user.id !== id));
  }

  const onToggle = id => {
    setUsers(users.map(user => user.id === id ? { ...user, active: !user.active } : user));
  }

  return (
    <>
      <CreateUser username={username} email={email} onChange={onChange} onCreate={onCreate} />
      <UserList users={users} onRemove={onRemove} onToggle={onToggle} />
    </>
  )
}

export default App;
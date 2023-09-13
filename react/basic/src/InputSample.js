import React, { useState } from 'react';

function InputSample(props) {
    const [inputs, setInputs] = useState({
        name: '',
        nickname: ''
    })

    const { name, nickname } = inputs;

    const onChange = (e) => {
    }

    const onReset = () => {
    }

    return (
        <div>
            <input name="name" onChange={onChange} value={name} placeholder='이름' />
            <input name="nickname" onChange={onChange} value={nickname} placeholder='닉네임' />
            <button onClick={onReset}>초기화</button>
            <div>
                <b>값:</b>
                {name} ({nickname})
            </div>
        </div>
    );
}

export default InputSample;
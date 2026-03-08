import React from 'react';

function SimpleTest() {
  return React.createElement('div', {
    style: {
      padding: '50px',
      backgroundColor: 'lightblue',
      textAlign: 'center'
    }
  }, 
    React.createElement('h1', { style: { color: 'red' } }, 'SIMPLE TEST WORKING!'),
    React.createElement('p', null, 'If you see this, React is working!')
  );
}

export default SimpleTest;

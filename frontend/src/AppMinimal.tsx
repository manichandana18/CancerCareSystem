import React from 'react';

function AppMinimal() {
  return React.createElement('div', {
    style: {
      padding: '50px',
      backgroundColor: 'yellow',
      textAlign: 'center',
      minHeight: '100vh'
    }
  }, 
    React.createElement('h1', { style: { color: 'blue', fontSize: '48px' } }, '🎉 MINIMAL APP WORKING!'),
    React.createElement('p', { style: { fontSize: '24px' } }, 'React is rendering correctly!'),
    React.createElement('div', { style: { marginTop: '30px' } }, 
      React.createElement('button', {
        style: {
          padding: '15px 30px',
          fontSize: '18px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        },
        onClick: () => alert('Button clicked!')
      }, '🔬 Test Button')
    )
  );
}

export default AppMinimal;

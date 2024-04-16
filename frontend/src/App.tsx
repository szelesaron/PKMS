import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';  // Import the CSS file  
import { Header } from './components/Header';
import { Form } from './components/Form';
import { Message } from './components/Response';

function App() {
  const [message, setMessage] = useState('');

  const handleFormSubmit = (name: any) => {
    axios.post('http://localhost:8000', { name })
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((error) => {
        console.error(error);
      });
  };



  return (
    <div>
      <Header /> {/* Use the 'Header' component */}
      <Form onFormSubmit={handleFormSubmit} />
      <Message message={message} />
    </div>
  );
}

export default App;
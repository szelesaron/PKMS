import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';  // Import the CSS file  
import { Header } from './components/Header';
import { Form } from './components/Form';
import { Message } from './components/Response';

function App() {
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFormSubmit = (query: any) => {
    setIsLoading(true);
    axios.post('http://localhost:8001', { query })
      .then((response) => {
        setMessage(response.data.message);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
      });

  };



  return (
    <div>
      <Header /> {/* Use the 'Header' component */}
      <Form onFormSubmit={handleFormSubmit} />
      {isLoading ? <div className="response">Loading...</div> : <Message message={message} />}  {/* Render the loading animation if isLoading is true */}
    </div>
  );
}

export default App;
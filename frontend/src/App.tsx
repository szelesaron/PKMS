import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState('');
  const [message, setMessage] = useState(''); // New state for storing the response message  

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(event.target.value);
  };

  const handleSubmit = () => {
    axios.post('http://localhost:8000', { name: formData })
      .then((response: { data: any; }) => {
        // Handle the response from the backend  
        console.log(response.data);
        setMessage(response.data.message); // Set the response message  
      })
      .catch((error: any) => {
        // Handle any errors that occur during the request  
        console.error(error);
      });
  };

  return (
    <div>
      <h1>Welcome to Google Copilot</h1>
      <input type="text" placeholder="Enter your name" onChange={handleInputChange} />
      <button onClick={handleSubmit}>Submit</button>
      {message && <div>{message}</div>}

    </div>
  );
}

export default App;  

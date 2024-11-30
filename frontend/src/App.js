import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Swal from 'sweetalert2';
import EventLog from './components/EventLog';
import Login from './components/Login';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      if (token) {
        axios.post('http://127.0.0.1:8000/refresh-token', {}, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          setToken(response.data.access_token);
        })
        .catch(error => {
          console.error('Error refreshing token:', error);
          setIsAuthenticated(false);
          setToken(null);
        });
      }
    }, 14 * 60 * 1000); // 14 minutes

    return () => clearInterval(interval);
  }, [token]);

  const handleLogin = async (username, password) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/login', { username, password });
      setToken(response.data.access_token);
      setIsAuthenticated(true);
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error de autenticación',
        text: 'Username or password is incorrect',
      });
      throw error;
    }
  };

  return (
    <div>
      {isAuthenticated ? (
        <EventLog token={token} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
};

export default App;
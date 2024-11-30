import React, { useState } from 'react';
import { Form, Button, Container, Row, InputGroup } from 'react-bootstrap';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onLogin(username, password);
    } catch (error) {
      setIsSubmitting(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
      <Row>
        <div className="shadow p-4 rounded">
          <h2 className="text-center mb-4">EVA-TEC-PYTHON</h2>
          <Form onSubmit={handleSubmit} className='text-center'>
            <Form.Group controlId="username" className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="password" className="mb-3">
              <Form.Label>Password</Form.Label>
              <InputGroup>
                <Form.Control
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <Button variant="outline-secondary" onClick={togglePasswordVisibility}>
                  <i className={`bi ${showPassword ? 'bi-eye-slash' : 'bi-eye'}`}></i>
                </Button>
              </InputGroup>
            </Form.Group>
            <div className="d-grid">
              <Button variant="primary" type="submit" className="mt-3" disabled={isSubmitting}>
                {isSubmitting ? 'Iniciando sesión...' : 'Login'}
              </Button>
            </div>
          </Form>
        </div>
      </Row>
    </Container>
  );
};

export default Login;
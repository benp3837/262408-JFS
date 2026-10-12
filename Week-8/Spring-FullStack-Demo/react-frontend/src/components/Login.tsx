import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login } from '../services/authService';

function Login() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch {
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Welcome back</h2>

      <div className="form-group">
        <label>Username</label>
        <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Enter your username" />
      </div>

      <div className="form-group">
        <label>Password</label>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter your password" />
      </div>

      <button type="submit">Login</button>

      <p className="register-link">
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
    </form>
  );
}

export default Login;

import { useState } from 'react';
import { register } from '../services/authService';

function Register() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(username, password);
      alert('Registration successful! You can now log in.');
    } catch {
      alert('Registration failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create an account</h2>

      <div className="form-group">
        <label>Username</label>
        <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Choose a username" />
      </div>

      <div className="form-group">
        <label>Password</label>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Choose a password" />
      </div>

      <div className="form-group">
        <label>Confirm Password</label>
        <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} placeholder="Confirm your password" />
      </div>

      <button type="submit">Register</button>
    </form>
  );
}

export default Register;
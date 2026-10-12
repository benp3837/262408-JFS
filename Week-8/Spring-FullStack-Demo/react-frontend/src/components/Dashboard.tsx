interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

const users: User[] = [
  { id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin' },
  { id: 2, name: 'Bob Smith',     email: 'bob@example.com',   role: 'Editor' },
  { id: 3, name: 'Carol White',   email: 'carol@example.com', role: 'Viewer' }
];

function Dashboard() {
  return (
    <div style={{ maxWidth: '75%', margin: '60px auto', fontFamily: 'Segoe UI, sans-serif' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.8rem', color: '#7a1a1a' }}>Dashboard</h2>
        <p style={{ color: '#b05c5c', marginTop: '0.25rem' }}>Welcome back! Here's an overview of your users.</p>
      </div>

      <div style={{ background: 'white', border: '1px solid #e8a8a8', borderRadius: '12px', padding: '1.5rem', boxShadow: '0 4px 16px rgba(180,30,30,0.1)' }}>
        <h3 style={{ marginBottom: '1rem', color: '#7a1a1a' }}>Users</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ background: '#fde8e8' }}>
            <tr>
              {['ID', 'Name', 'Email', 'Role'].map(h => (
                <th key={h} style={{ textAlign: 'left', padding: '0.75rem 1rem', fontSize: '0.85rem', color: '#8a2a2a', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}
                onMouseEnter={e => (e.currentTarget.style.background = '#fff4f4')}
                onMouseLeave={e => (e.currentTarget.style.background = 'white')}>
                <td style={{ padding: '0.75rem 1rem', borderTop: '1px solid #fde8e8', color: '#333' }}>{user.id}</td>
                <td style={{ padding: '0.75rem 1rem', borderTop: '1px solid #fde8e8', color: '#333' }}>{user.name}</td>
                <td style={{ padding: '0.75rem 1rem', borderTop: '1px solid #fde8e8', color: '#333' }}>{user.email}</td>
                <td style={{ padding: '0.75rem 1rem', borderTop: '1px solid #fde8e8', color: '#333' }}>
                  <span style={{ background: '#fde8e8', color: '#dd2a2a', padding: '0.2rem 0.6rem', borderRadius: '999px', fontSize: '0.8rem', fontWeight: 600 }}>{user.role}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
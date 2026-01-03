export default function NotFound() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      textAlign: 'center',
      background: '#f5f5f5'
    }}>
      <h1 style={{ fontSize: '48px', margin: '0' }}>404</h1>
      <p style={{ fontSize: '18px', color: '#666' }}>Page Not Found</p>
      <a href="/" style={{
        marginTop: '20px',
        padding: '10px 20px',
        background: '#667eea',
        color: 'white',
        textDecoration: 'none',
        borderRadius: '5px'
      }}>
        Go to Dashboard
      </a>
    </div>
  )
}

import Sidebar from './Sidebar'

export default function Layout({ children }) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <main style={{
        marginLeft: 'var(--sidebar-w)',
        flex: 1,
        padding: '36px 40px',
        maxWidth: 'calc(100vw - var(--sidebar-w))',
        minHeight: '100vh',
      }}>
        {children}
      </main>
    </div>
  )
}

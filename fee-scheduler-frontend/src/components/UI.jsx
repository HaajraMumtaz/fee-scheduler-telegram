import { useState } from 'react'

/* ── Spinner ── */
export function Spinner({ size = 18 }) {
  return (
    <span style={{
      display: 'inline-block', width: size, height: size,
      border: `2px solid var(--border-bright)`,
      borderTopColor: 'var(--gold)',
      borderRadius: '50%',
      animation: 'spin 0.7s linear infinite',
    }} />
  )
}

/* ── Badge ── */
const badgeColors = {
  paid:     { color: 'var(--green)', bg: 'var(--green-dim)' },
  unpaid:   { color: 'var(--red)',   bg: 'var(--red-dim)'   },
  draft:    { color: 'var(--amber)', bg: 'var(--amber-dim)' },
  approved: { color: 'var(--blue)',  bg: 'var(--blue-dim)'  },
  active:   { color: 'var(--green)', bg: 'var(--green-dim)' },
  inactive: { color: 'var(--text-muted)', bg: 'var(--bg-overlay)' },
  overdue:  { color: 'var(--red)',   bg: 'var(--red-dim)'   },
}
export function Badge({ status }) {
  const s = status?.toLowerCase()
  const c = badgeColors[s] || { color: 'var(--text-secondary)', bg: 'var(--bg-overlay)' }
  return (
    <span style={{
      display: 'inline-block',
      padding: '2px 9px', borderRadius: '99px',
      fontSize: 11, fontWeight: 600, letterSpacing: '0.04em',
      textTransform: 'uppercase',
      color: c.color, background: c.bg,
    }}>{status}</span>
  )
}

/* ── Card ── */
export function Card({ children, style, className }) {
  return (
    <div className={className} style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      ...style,
    }}>{children}</div>
  )
}

/* ── Stat Card ── */
export function StatCard({ label, value, sub, accent }) {
  return (
    <Card style={{ padding: '20px 24px' }}>
      <div style={{ color: 'var(--text-muted)', fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 8 }}>{label}</div>
      <div style={{
        fontFamily: 'var(--font-mono)', fontSize: 28, fontWeight: 500,
        color: accent || 'var(--text-primary)',
        lineHeight: 1,
      }}>{value ?? '—'}</div>
      {sub && <div style={{ color: 'var(--text-muted)', fontSize: 11, marginTop: 6 }}>{sub}</div>}
    </Card>
  )
}

/* ── Table ── */
export function Table({ cols, rows, emptyMsg = 'No data' }) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {cols.map(c => (
              <th key={c.key ?? c.label} style={{
                padding: '10px 16px', textAlign: 'left',
                fontSize: 11, letterSpacing: '0.08em', textTransform: 'uppercase',
                color: 'var(--text-muted)',
                borderBottom: '1px solid var(--border)',
                fontWeight: 600,
              }}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0
            ? <tr><td colSpan={cols.length} style={{ padding: '32px 16px', textAlign: 'center', color: 'var(--text-muted)' }}>{emptyMsg}</td></tr>
            : rows.map((row, i) => (
              <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}
                onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-elevated)'}
                onMouseLeave={e => e.currentTarget.style.background = ''}>
                {cols.map(c => (
                  <td key={c.key ?? c.label} style={{
                    padding: '11px 16px',
                    color: c.mono ? 'var(--text-secondary)' : 'var(--text-primary)',
                    fontFamily: c.mono ? 'var(--font-mono)' : undefined,
                    fontSize: c.mono ? 13 : 14,
                  }}>
                    {c.render ? c.render(row) : row[c.key]}
                  </td>
                ))}
              </tr>
            ))
          }
        </tbody>
      </table>
    </div>
  )
}

/* ── Button ── */
export function Btn({ children, onClick, variant = 'primary', size = 'md', disabled, loading, style }) {
  const base = {
    display: 'inline-flex', alignItems: 'center', gap: 6,
    border: 'none', borderRadius: 'var(--radius)',
    fontFamily: 'var(--font-ui)', fontWeight: 600, cursor: disabled || loading ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'background 0.15s, transform 0.1s',
    fontSize: size === 'sm' ? 12 : 14,
    padding: size === 'sm' ? '5px 12px' : '8px 18px',
    ...style,
  }
  const variants = {
    primary: { background: 'var(--gold)', color: '#0d0f14' },
    ghost:   { background: 'transparent', color: 'var(--text-secondary)', border: '1px solid var(--border)' },
    danger:  { background: 'var(--red-dim)', color: 'var(--red)', border: '1px solid rgba(240,98,146,0.3)' },
    success: { background: 'var(--green-dim)', color: 'var(--green)', border: '1px solid rgba(62,207,142,0.3)' },
  }
  return (
    <button style={{ ...base, ...variants[variant] }} onClick={onClick} disabled={disabled || loading}>
      {loading ? <Spinner size={14} /> : null}
      {children}
    </button>
  )
}

/* ── Page Header ── */
export function PageHeader({ title, sub, action }) {
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 28 }}>
      <div>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 400, lineHeight: 1.1, color: 'var(--text-primary)' }}>{title}</h1>
        {sub && <p style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 4 }}>{sub}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}

/* ── Alert ── */
export function Alert({ msg, type = 'error' }) {
  if (!msg) return null
  const color = type === 'error' ? 'var(--red)' : 'var(--green)'
  const bg    = type === 'error' ? 'var(--red-dim)' : 'var(--green-dim)'
  return (
    <div style={{
      background: bg, color, border: `1px solid ${color}33`,
      borderRadius: 'var(--radius)', padding: '10px 14px', fontSize: 13, marginBottom: 16,
    }}>{msg}</div>
  )
}

/* ── Input ── */
export function Input({ label, ...props }) {
  return (
    <label style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      {label && <span style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase' }}>{label}</span>}
      <input {...props} style={{
        background: 'var(--bg-elevated)', border: '1px solid var(--border-bright)',
        borderRadius: 'var(--radius)', padding: '9px 12px',
        color: 'var(--text-primary)', fontSize: 14, outline: 'none',
        transition: 'border-color 0.15s',
        ...props.style,
      }}
        onFocus={e => e.target.style.borderColor = 'var(--gold)'}
        onBlur={e => e.target.style.borderColor = 'var(--border-bright)'}
      />
    </label>
  )
}

/* ── Modal ── */
export function Modal({ open, onClose, title, children }) {
  if (!open) return null
  return (
    <div onClick={onClose} style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000,
    }}>
      <div onClick={e => e.stopPropagation()} style={{
        background: 'var(--bg-surface)', border: '1px solid var(--border-bright)',
        borderRadius: 'var(--radius-lg)', padding: 28, minWidth: 380, maxWidth: 520, width: '90%',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 20, fontWeight: 400 }}>{title}</h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', fontSize: 20, lineHeight: 1 }}>×</button>
        </div>
        {children}
      </div>
    </div>
  )
}

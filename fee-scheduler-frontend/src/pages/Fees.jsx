import { useState, useEffect } from 'react'
import { api } from '../services/api'
import { PageHeader, Card, Table, Btn, Badge, Spinner, Alert, Input, Modal } from '../components/UI'

export default function Fees() {
  const [fees, setFees] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ student_id:'', status:'', year:'', month:'' })
  const [genMsg, setGenMsg] = useState({ err:'', ok:'' })
  const [generating, setGenerating] = useState(false)
  const [dismissModal, setDismissModal] = useState(null)
  const [dismissDate, setDismissDate] = useState('')
  const [dismissing, setDismissing] = useState(false)

  const setF = k => e => setFilters(f => ({ ...f, [k]: e.target.value }))

  const load = () => {
    setLoading(true)
    const p = new URLSearchParams()
    Object.entries(filters).forEach(([k,v]) => v && p.set(k, v))
    api.get(`/api/fees/?${p}`).then(d => setFees(d.fees)).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const generate = async () => {
    setGenerating(true); setGenMsg({ err:'', ok:'' })
    try {
      const p = new URLSearchParams()
      if (filters.year) p.set('year', filters.year)
      if (filters.month) p.set('month', filters.month)
      await api.post(`/api/fees/generate?${p}`)
      setGenMsg({ ok:'Fees generated.', err:'' }); load()
    } catch(e) { setGenMsg({ err:e.message, ok:'' }) }
    finally { setGenerating(false) }
  }

  const dismiss = async () => {
    setDismissing(true)
    try { await api.post(`/api/fees/${dismissModal.id}/dismiss?until=${dismissDate}`); setDismissModal(null); load() }
    catch(e) { alert(e.message) }
    finally { setDismissing(false) }
  }

  const cols = [
    { label:'Student ID', key:'student_id', mono:true },
    { label:'Period', render: r => <span className="mono">{r.year}/{String(r.month).padStart(2,'0')}</span> },
    { label:'Amount', render: r => <span className="mono">PKR {Number(r.amount).toLocaleString()}</span> },
    { label:'Due', render: r => <span className="mono" style={{ fontSize:12 }}>{r.due_date}</span> },
    { label:'Status', render: r => <Badge status={r.status} /> },
    { label:'Paid On', render: r => <span className="mono" style={{ fontSize:12, color:'var(--text-muted)' }}>{r.paid_on || '—'}</span> },
    { label:'', render: r => r.status !== 'paid' && <Btn size="sm" variant="ghost" onClick={() => { setDismissModal(r); setDismissDate('') }}>Dismiss</Btn> },
  ]

  return (
    <div className="fade-up">
      <PageHeader title="Fees" action={<Btn onClick={generate} loading={generating}>Generate</Btn>} />
      <Alert msg={genMsg.err} type="error" />
      <Alert msg={genMsg.ok} type="success" />

      {/* Filters */}
      <div style={{ display:'flex', gap:10, marginBottom:16, flexWrap:'wrap' }}>
        {[['student_id','Student ID'],['year','Year'],['month','Month']].map(([k,l]) => (
          <Input key={k} label={l} value={filters[k]} onChange={setF(k)} style={{ width:120 }} />
        ))}
        <label style={{ display:'flex', flexDirection:'column', gap:5 }}>
          <span style={{ fontSize:12, color:'var(--text-muted)', fontWeight:600, letterSpacing:'0.05em', textTransform:'uppercase' }}>Status</span>
          <select value={filters.status} onChange={setF('status')} style={{ background:'var(--bg-elevated)', border:'1px solid var(--border-bright)', borderRadius:'var(--radius)', padding:'9px 12px', color:'var(--text-primary)', fontSize:14 }}>
            <option value="">All</option>
            <option value="unpaid">Unpaid</option>
            <option value="paid">Paid</option>
          </select>
        </label>
        <div style={{ display:'flex', alignItems:'flex-end' }}>
          <Btn variant="ghost" onClick={load}>Search</Btn>
        </div>
      </div>

      <Card>
        {loading ? <div style={{ padding:40, textAlign:'center' }}><Spinner /></div> : <Table cols={cols} rows={fees} />}
      </Card>

      <Modal open={!!dismissModal} onClose={() => setDismissModal(null)} title="Dismiss Fee">
        <p style={{ color:'var(--text-muted)', fontSize:13, marginBottom:16 }}>Dismiss until date (fee won't appear in reminders until then).</p>
        <Input label="Until" type="date" value={dismissDate} onChange={e => setDismissDate(e.target.value)} style={{ marginBottom:16 }} />
        <Btn onClick={dismiss} loading={dismissing} style={{ width:'100%', justifyContent:'center' }}>Confirm</Btn>
      </Modal>
    </div>
  )
}

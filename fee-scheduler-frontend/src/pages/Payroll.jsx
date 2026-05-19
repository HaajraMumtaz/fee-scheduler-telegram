import { useState, useEffect } from 'react'
import { api } from '../services/api'
import { PageHeader, Card, Table, Btn, Badge, Spinner, Alert, Input } from '../components/UI'

export default function Payroll() {
  const [payrolls, setPayrolls] = useState([])
  const [loading, setLoading] = useState(true)
  const [month, setMonth] = useState('')
  const [running, setRunning] = useState(false)
  const [msg, setMsg] = useState({ err:'', ok:'' })

  const load = () => {
    setLoading(true)
    const p = month ? `?month=${month}` : ''
    api.get(`/api/payroll/${p}`).then(d => setPayrolls(d.payrolls)).finally(() => setLoading(false))
  }
  useEffect(() => { load() }, [])

  const runPayroll = async () => {
    if (!confirm('Run payroll for today?')) return
    setRunning(true); setMsg({ err:'', ok:'' })
    try { await api.post('/api/payroll/run'); setMsg({ ok:'Payroll run complete.', err:'' }); load() }
    catch(e) { setMsg({ err:e.message, ok:'' }) }
    finally { setRunning(false) }
  }

  const action = async (id, act) => {
    try { await api.post(`/api/payroll/${id}/${act}`); load() }
    catch(e) { alert(e.message) }
  }

  const cols = [
    { label:'ID', key:'id', mono:true },
    { label:'Teacher ID', key:'teacher_id', mono:true },
    { label:'Month', key:'month', mono:true },
    { label:'Amount', render: r => <span className="mono">PKR {Number(r.total_amount).toLocaleString()}</span> },
    { label:'Status', render: r => <Badge status={r.status} /> },
    { label:'Actions', render: r => (
      <div style={{ display:'flex', gap:6 }}>
        {r.status === 'draft'    && <Btn size="sm" variant="success" onClick={() => action(r.id,'approve')}>Approve</Btn>}
        {r.status === 'approved' && <Btn size="sm" variant="primary" onClick={() => action(r.id,'mark-paid')}>Mark Paid</Btn>}
      </div>
    )},
  ]

  return (
    <div className="fade-up">
      <PageHeader title="Payroll" action={<Btn onClick={runPayroll} loading={running}>Run Payroll</Btn>} />
      <Alert msg={msg.err} type="error" />
      <Alert msg={msg.ok} type="success" />
      <div style={{ display:'flex', gap:10, marginBottom:16, alignItems:'flex-end' }}>
        <Input label="Filter by month" value={month} onChange={e => setMonth(e.target.value)} placeholder="e.g. 2025-01" style={{ width:180 }} />
        <Btn variant="ghost" onClick={load}>Search</Btn>
      </div>
      <Card>
        {loading ? <div style={{ padding:40, textAlign:'center' }}><Spinner /></div> : <Table cols={cols} rows={payrolls} />}
      </Card>
    </div>
  )
}

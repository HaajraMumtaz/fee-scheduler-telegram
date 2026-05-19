import { useState, useEffect } from 'react'
import { api } from '../services/api'
import { PageHeader, Card, Table, Btn, Badge, Spinner, Alert, Modal, Input } from '../components/UI'

export default function Students() {
  const [unpaid, setUnpaid] = useState([])
  const [loading, setLoading] = useState(true)
  const [modal, setModal] = useState(null) // { student_id, name }
  const [form, setForm] = useState({ year:'', month:'', amount:'' })
  const [msg, setMsg] = useState({ err:'', ok:'' })
  const [paying, setPaying] = useState(false)

  const load = () => api.get('/api/students/unpaid').then(d => setUnpaid(d.students)).finally(() => setLoading(false))
  useEffect(() => { load() }, [])

  const openModal = row => { setModal(row); setForm({ year:'', month:'', amount:'' }); setMsg({ err:'', ok:'' }) }

  const markPaid = async () => {
    setPaying(true); setMsg({ err:'', ok:'' })
    try {
      const params = new URLSearchParams()
      if (form.year)   params.set('year', form.year)
      if (form.month)  params.set('month', form.month)
      if (form.amount) params.set('amount', form.amount)
      await api.post(`/api/students/${modal.student_id}/mark-paid?${params}`)
      setMsg({ err:'', ok:'Marked as paid.' })
      load()
    } catch (e) { setMsg({ err: e.message, ok:'' }) }
    finally { setPaying(false) }
  }

  const cols = [
    { label:'Name', key:'name' },
    { label:'Student ID', key:'student_id', mono:true },
    { label:'Unpaid Months', key:'unpaid_months', mono:true },
    { label:'Action', render: row => <Btn size="sm" variant="success" onClick={() => openModal(row)}>Mark Paid</Btn> },
  ]

  if (loading) return <div style={{ display:'flex', justifyContent:'center', paddingTop:80 }}><Spinner size={28} /></div>

  return (
    <div className="fade-up">
      <PageHeader title="Students" sub="Unpaid fee records" />
      <Card>
        <Table cols={cols} rows={unpaid} emptyMsg="All students are paid up ✓" />
      </Card>

      <Modal open={!!modal} onClose={() => setModal(null)} title={`Mark Paid — ${modal?.name}`}>
        <Alert msg={msg.err} type="error" />
        <Alert msg={msg.ok} type="success" />
        <div style={{ display:'flex', flexDirection:'column', gap:12, marginBottom:20 }}>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
            <Input label="Year" type="number" placeholder={new Date().getFullYear()} value={form.year} onChange={e => setForm(f=>({...f,year:e.target.value}))} />
            <Input label="Month (1–12)" type="number" placeholder={new Date().getMonth()+1} value={form.month} onChange={e => setForm(f=>({...f,month:e.target.value}))} />
          </div>
          <Input label="Amount" type="number" placeholder="0.00" value={form.amount} onChange={e => setForm(f=>({...f,amount:e.target.value}))} />
        </div>
        <Btn onClick={markPaid} loading={paying} style={{ width:'100%', justifyContent:'center' }}>Confirm Payment</Btn>
      </Modal>
    </div>
  )
}

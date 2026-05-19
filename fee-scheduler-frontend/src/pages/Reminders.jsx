import { useState, useEffect } from 'react'
import { api } from '../services/api'
import { PageHeader, Card, Table, Spinner } from '../components/UI'

export default function Reminders() {
  const [reminders, setReminders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/api/reminders/').then(d => setReminders(d.data || [])).finally(() => setLoading(false))
  }, [])

  const cols = [
    { label:'Student ID', key:'student_id', mono:true },
    { label:'Name', key:'student_name' },
    { label:'Amount Due', render: r => <span className="mono">PKR {Number(r.amount_due ?? 0).toLocaleString()}</span> },
    { label:'Due Date', render: r => <span className="mono" style={{ fontSize:12 }}>{r.due_date || '—'}</span> },
    { label:'Period', render: r => <span className="mono" style={{ fontSize:12 }}>{r.period || '—'}</span> },
  ]

  if (loading) return <div style={{ display:'flex', justifyContent:'center', paddingTop:80 }}><Spinner size={28} /></div>

  return (
    <div className="fade-up">
      <PageHeader title="Reminders" sub={`${reminders.length} due today`} />
      <Card><Table cols={cols} rows={reminders} emptyMsg="No reminders due." /></Card>
    </div>
  )
}

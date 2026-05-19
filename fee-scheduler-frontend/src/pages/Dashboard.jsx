import { useState, useEffect } from 'react'
import { api } from '../services/api'
import { StatCard, Spinner, PageHeader } from '../components/UI'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/api/dashboard').then(setData).finally(() => setLoading(false))
  }, [])

  if (loading) return <div style={{ display:'flex', justifyContent:'center', paddingTop:80 }}><Spinner size={28} /></div>

  return (
    <div className="fade-up">
      <PageHeader title="Dashboard" sub={`As of ${data?.as_of ?? '—'}`} />
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(200px, 1fr))', gap:16 }}>
        <StatCard label="Total Students" value={data?.total_students} />
        <StatCard label="Active Teachers" value={data?.active_teachers} />
        <StatCard label="Overdue Fees" value={data?.overdue_fees_count} accent="var(--red)" />
        <StatCard label="Overdue Amount" value={`PKR ${(data?.overdue_fees_amount ?? 0).toLocaleString()}`} accent="var(--red)" />
        <StatCard label="Pending Payrolls" value={data?.pending_payrolls} accent="var(--amber)" />
      </div>
    </div>
  )
}

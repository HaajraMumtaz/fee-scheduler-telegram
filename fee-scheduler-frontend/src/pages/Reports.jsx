import { useState } from 'react'
import { api } from '../services/api'
import { PageHeader, Card, Btn, Alert, Input } from '../components/UI'

function ResultBlock({ data }) {
  if (!data) return null
  return (
    <pre style={{
      background:'var(--bg-elevated)', border:'1px solid var(--border)',
      borderRadius:'var(--radius)', padding:16, marginTop:12,
      fontSize:12, fontFamily:'var(--font-mono)', color:'var(--text-secondary)',
      overflowX:'auto', whiteSpace:'pre-wrap', wordBreak:'break-word',
    }}>
      {JSON.stringify(data, null, 2)}
    </pre>
  )
}

function ReportCard({ title, desc, onRun, loading, result, err, children }) {
  return (
    <Card style={{ padding:20 }}>
      <div style={{ fontWeight:600, marginBottom:4 }}>{title}</div>
      <div style={{ color:'var(--text-muted)', fontSize:13, marginBottom:14 }}>{desc}</div>
      {children}
      <Alert msg={err} type="error" />
      <Btn onClick={onRun} loading={loading} variant="ghost" style={{ marginTop:8 }}>Run</Btn>
      <ResultBlock data={result} />
    </Card>
  )
}

export default function Reports() {
  const now = new Date()
  const [period, setPeriod] = useState({ year: String(now.getFullYear()), month: String(now.getMonth()+1) })
  const [states, setStates] = useState({ monthStart:{}, monthEnd:{}, daily:{} })

  const setP = k => e => setPeriod(p => ({ ...p, [k]: e.target.value }))

  const run = async key => {
    setStates(s => ({ ...s, [key]:{ loading:true, result:null, err:'' } }))
    try {
      let res
      if (key === 'daily') {
        res = await api.post('/api/reports/daily-reminders')
      } else {
        const endpoint = key === 'monthStart' ? '/api/reports/month-start' : '/api/reports/month-end'
        res = await api.post(`${endpoint}?year=${period.year}&month=${period.month}`)
      }
      setStates(s => ({ ...s, [key]:{ loading:false, result:res, err:'' } }))
    } catch(e) {
      setStates(s => ({ ...s, [key]:{ loading:false, result:null, err:e.message } }))
    }
  }

  const PeriodInputs = () => (
    <div style={{ display:'flex', gap:10, marginBottom:12 }}>
      <Input label="Year" value={period.year} onChange={setP('year')} style={{ width:100 }} />
      <Input label="Month" value={period.month} onChange={setP('month')} style={{ width:80 }} />
    </div>
  )

  return (
    <div className="fade-up">
      <PageHeader title="Reports" sub="Generate billing & payroll reports" />
      <div style={{ display:'grid', gap:16 }}>
        <ReportCard title="Month Start" desc="Generate monthly fees for all active students."
          onRun={() => run('monthStart')} loading={states.monthStart.loading}
          result={states.monthStart.result} err={states.monthStart.err}>
          <PeriodInputs />
        </ReportCard>
        <ReportCard title="Month End / Payroll" desc="Calculate and create payroll runs for all teachers."
          onRun={() => run('monthEnd')} loading={states.monthEnd.loading}
          result={states.monthEnd.result} err={states.monthEnd.err}>
          <PeriodInputs />
        </ReportCard>
        <ReportCard title="Daily Reminders" desc="Process and send payment reminders for overdue fees."
          onRun={() => run('daily')} loading={states.daily.loading}
          result={states.daily.result} err={states.daily.err} />
      </div>
    </div>
  )
}

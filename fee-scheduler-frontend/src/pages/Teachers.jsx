import { useState, useEffect } from 'react'
import { api } from '../services/api'
import { PageHeader, Card, Table, Btn, Badge, Spinner, Modal } from '../components/UI'

export default function Teachers() {
  const [teachers, setTeachers] = useState([])
  const [loading, setLoading] = useState(true)
  const [detail, setDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)

  const load = () => api.get('/api/teachers/').then(d => setTeachers(d.teachers)).finally(() => setLoading(false))
  useEffect(() => { load() }, [])

  const openDetail = async row => {
    setDetail({}); setDetailLoading(true)
    const d = await api.get(`/api/teachers/${row.teacher_id}`)
    setDetail(d); setDetailLoading(false)
  }

  const deactivate = async id => {
    if (!confirm('Deactivate this teacher?')) return
    await api.patch(`/api/teachers/${id}/deactivate`)
    load()
    setDetail(null)
  }

  const cols = [
    { label:'Name', key:'name' },
    { label:'Teacher ID', key:'teacher_id', mono:true },
    { label:'Phone', key:'phone' },
    { label:'Status', render: r => <Badge status={r.status} /> },
    { label:'', render: r => <Btn size="sm" variant="ghost" onClick={() => openDetail(r)}>View</Btn> },
  ]

  if (loading) return <div style={{ display:'flex', justifyContent:'center', paddingTop:80 }}><Spinner size={28} /></div>

  return (
    <div className="fade-up">
      <PageHeader title="Teachers" sub={`${teachers.length} total`} />
      <Card><Table cols={cols} rows={teachers} /></Card>

      <Modal open={!!detail} onClose={() => setDetail(null)} title={detail?.name || 'Teacher Detail'}>
        {detailLoading ? <div style={{ textAlign:'center', padding:20 }}><Spinner /></div> : detail && (
          <>
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:10, marginBottom:16 }}>
              {[['ID', detail.teacher_id], ['Phone', detail.phone], ['Status', detail.status]].map(([k,v]) => (
                <div key={k}>
                  <div style={{ fontSize:11, color:'var(--text-muted)', textTransform:'uppercase', letterSpacing:'0.06em' }}>{k}</div>
                  <div style={{ fontFamily:'var(--font-mono)', fontSize:13, marginTop:2 }}>{v}</div>
                </div>
              ))}
            </div>
            <div style={{ fontSize:12, color:'var(--text-muted)', marginBottom:8, textTransform:'uppercase', letterSpacing:'0.06em' }}>Assignments</div>
            {(detail.assignments || []).length === 0
              ? <div style={{ color:'var(--text-muted)', fontSize:13 }}>No assignments</div>
              : detail.assignments.map(a => (
                <div key={a.id} style={{ background:'var(--bg-elevated)', borderRadius:'var(--radius)', padding:'10px 12px', marginBottom:6, fontSize:13 }}>
                  <span style={{ fontWeight:600 }}>{a.subject}</span>
                  <span style={{ color:'var(--text-muted)', marginLeft:12 }}>{a.lessons_per_month} lessons/mo · PKR {a.rate_per_lesson}/lesson</span>
                  {!a.active && <Badge status="inactive" />}
                </div>
              ))}
            {detail.status === 'active' && (
              <Btn variant="danger" onClick={() => deactivate(detail.teacher_id)} style={{ marginTop:16, width:'100%', justifyContent:'center' }}>
                Deactivate Teacher
              </Btn>
            )}
          </>
        )}
      </Modal>
    </div>
  )
}

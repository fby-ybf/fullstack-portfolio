import axios from 'axios'

const http = axios.create({ baseURL: '' })

export const listDocuments = () => http.get('/api/documents').then(r => r.data)
export const addDocument = (title, text) =>
  http.post('/api/documents', { title, text }).then(r => r.data)
export const deleteDocument = (id) => http.delete(`/api/documents/${id}`).then(r => r.data)
export const getHistory = (sessionId) =>
  http.get(`/api/history/${sessionId}`).then(r => r.data)

// 同步问答（测试 / 非流式可用）
export const chatSync = (payload) => http.post('/api/chat', payload).then(r => r.data)

// 流式问答：手动消费 SSE，逐事件回调
export async function chatStream(payload, handlers) {
  const res = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok || !res.body) throw new Error('流式请求失败: ' + res.status)
  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let idx
    while ((idx = buffer.indexOf('\n\n')) !== -1) {
      const chunk = buffer.slice(0, idx)
      buffer = buffer.slice(idx + 2)
      const dataLine = chunk.split('\n').find((l) => l.startsWith('data:'))
      if (dataLine) {
        const json = JSON.parse(dataLine.slice(5).trim())
        routeEvent(json, handlers)
      }
    }
  }
}

function routeEvent(json, h) {
  if (json.type === 'meta' && h.onMeta) h.onMeta(json)
  else if (json.type === 'sources' && h.onSources) h.onSources(json.docs)
  else if (json.type === 'token' && h.onToken) h.onToken(json.text)
  else if (json.type === 'done' && h.onDone) h.onDone()
}

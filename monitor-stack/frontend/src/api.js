import axios from 'axios'

const http = axios.create({ baseURL: '' })

export const listAlerts = () => http.get('/api/alerts').then(r => r.data.alerts)
export const ackAlert = (id) => http.post(`/api/alerts/${id}/ack`).then(r => r.data)

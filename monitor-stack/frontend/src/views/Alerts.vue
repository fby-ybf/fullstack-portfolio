<template>
  <div class="panel">
    <el-card shadow="never" class="head">
      <div class="title">
        <span>🚨 告警面板</span>
        <el-tag :type="firingCount ? 'danger' : 'success'">
          firing: {{ firingCount }}
        </el-tag>
      </div>
      <div class="actions">
        <el-button size="small" @click="refresh">手动刷新</el-button>
        <el-button size="small" type="primary" tag="a" :href="GRAFANA_URL" target="_blank">
          打开 Grafana
        </el-button>
      </div>
    </el-card>

    <el-card shadow="never">
      <el-table :data="alerts" empty-text="暂无告警" style="width: 100%">
        <el-table-column label="级别" width="100">
          <template #default="{ row }">
            <el-tag :type="sevType(row.labels.severity)">{{ row.labels.severity || 'info' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="告警名" prop="labels.alertname" />
        <el-table-column label="实例" prop="labels.instance" />
        <el-table-column label="摘要" prop="annotations.summary" show-overflow-tooltip />
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="row.status === 'firing' ? 'danger' : 'info'">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="已处理" width="90">
          <template #default="{ row }">
            <el-tag v-if="row.acked" type="success">已处理</el-tag>
            <el-tag v-else type="warning">待处理</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="接收时间" width="180">
          <template #default="{ row }">{{ fmt(row.received_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button
              size="small"
              type="success"
              :disabled="row.acked"
              @click="ack(row)">标记已处理</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listAlerts, ackAlert } from '../api.js'

// 容器编排里 Grafana 映射到主机 3000；按需修改
const GRAFANA_URL = 'http://localhost:3000'

const alerts = ref([])
let timer = null

async function refresh() {
  try {
    alerts.value = await listAlerts()
  } catch (e) {
    ElMessage.error('拉取告警失败')
  }
}
const firingCount = computed(() =>
  alerts.value.filter(a => a.status === 'firing' && !a.acked).length)

async function ack(row) {
  await ackAlert(row.id)
  ElMessage.success('已标记为处理')
  await refresh()
}
function sevType(s) {
  if (s === 'critical') return 'danger'
  if (s === 'warning') return 'warning'
  return 'info'
}
function fmt(ts) {
  if (!ts) return '-'
  return new Date(ts * 1000).toLocaleString('zh-CN')
}

onMounted(() => { refresh(); timer = setInterval(refresh, 5000) })
onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.panel { padding: 16px; }
.head { margin-bottom: 16px; display: flex; }
.title { font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 10px; flex: 1; }
.actions { display: flex; gap: 8px; align-items: center; }
</style>

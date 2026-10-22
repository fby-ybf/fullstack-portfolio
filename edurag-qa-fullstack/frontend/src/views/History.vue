<template>
  <div class="history">
    <el-card shadow="never" class="bar">
      <el-input v-model="sid" placeholder="输入会话 ID" style="max-width: 360px" />
      <el-button type="primary" @click="load" style="margin-left: 10px">查询历史</el-button>
    </el-card>

    <el-card shadow="never" v-if="messages.length">
      <el-timeline>
        <el-timeline-item
          v-for="(m, i) in messages"
          :key="i"
          :type="m.role === 'user' ? 'primary' : 'success'"
          :hollow="m.role !== 'user'">
          <strong>{{ m.role === 'user' ? '用户' : '助手' }}</strong>
          <div class="bubble">{{ m.content }}</div>
        </el-timeline-item>
      </el-timeline>
    </el-card>
    <el-empty v-else description="输入会话 ID 查看历史对话" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getHistory } from '../api.js'

const sid = ref('')
const messages = ref([])
async function load() {
  if (!sid.value.trim()) return
  const data = await getHistory(sid.value.trim())
  messages.value = data.messages || []
}
</script>

<style scoped>
.history { padding: 16px; }
.bar { max-width: 720px; margin-bottom: 16px; }
.bubble { margin-top: 6px; white-space: pre-wrap; line-height: 1.6; color: #374151; }
</style>

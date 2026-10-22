<template>
  <div class="chat-wrap">
    <div class="chat-main">
      <div class="msg-list" ref="listRef">
        <div v-for="(m, i) in messages" :key="i" :class="['msg', m.role]">
          <div class="bubble">
            <span v-if="m.role === 'user'">{{ m.content }}</span>
            <span v-else>{{ m.content || '▌' }}</span>
          </div>
        </div>
      </div>
      <div class="composer">
        <el-input
          v-model="input"
          type="textarea"
          :rows="2"
          placeholder="输入你的问题，回车发送（Shift+Enter 换行）"
          @keydown.enter.exact.prevent="send"
        />
        <el-button type="primary" :loading="streaming" @click="send">发送</el-button>
      </div>
    </div>

    <div class="chat-side">
      <el-card shadow="never">
        <template #header>检索信息</template>
        <div v-if="meta">
          <el-tag :type="meta.can_answer ? 'success' : 'warning'">
            {{ meta.can_answer ? '可回答' : '拒答（低置信度）' }}
          </el-tag>
          <p class="meta-row">置信度：{{ (meta.confidence * 100).toFixed(1) }}%</p>
          <p class="meta-row">会话 ID：{{ meta.session_id }}</p>
        </div>
        <el-empty v-else description="提问后展示检索来源" :image-size="60" />
      </el-card>

      <el-card shadow="never" class="src-card">
        <template #header>引用片段（{{ sources.length }}）</template>
        <div v-for="(s, i) in sources" :key="i" class="src">
          <div class="src-title">{{ s.title }}</div>
          <div class="src-text">{{ s.text }}</div>
          <div class="src-score">相关度 {{ (s.score * 100).toFixed(0) }}%</div>
        </div>
        <el-empty v-if="!sources.length" description="暂无" :image-size="50" />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { chatStream } from '../api.js'

const input = ref('')
const messages = ref([])
const streaming = ref(false)
const sources = ref([])
const meta = ref(null)
const listRef = ref(null)

async function send() {
  const q = input.value.trim()
  if (!q || streaming.value) return
  input.value = ''
  messages.value.push({ role: 'user', content: q })
  messages.value.push({ role: 'assistant', content: '' })
  streaming.value = true
  sources.value = []
  meta.value = null

  const last = messages.value[messages.value.length - 1]
  try {
    await chatStream({ question: q }, {
      onMeta: (m) => (meta.value = m),
      onSources: (docs) => (sources.value = docs),
      onToken: (t) => (last.content += t),
      onDone: () => {},
    })
  } catch (e) {
    last.content = '请求出错：' + e.message
    ElMessage.error('流式请求失败')
  } finally {
    streaming.value = false
    await nextTick()
    if (listRef.value) listRef.value.scrollTop = listRef.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-wrap { display: flex; height: 100vh; }
.chat-main { flex: 1; display: flex; flex-direction: column; padding: 16px; }
.msg-list { flex: 1; overflow-y: auto; padding: 8px; }
.msg { display: flex; margin-bottom: 12px; }
.msg.user { justify-content: flex-end; }
.bubble {
  max-width: 70%; padding: 10px 14px; border-radius: 10px;
  background: #fff; border: 1px solid #e3e8ef; white-space: pre-wrap; line-height: 1.6;
}
.msg.user .bubble { background: #2f6fed; color: #fff; border-color: #2f6fed; }
.composer { display: flex; gap: 10px; align-items: flex-end; }
.composer .el-button { flex: none; }
.chat-side { width: 340px; padding: 16px; overflow-y: auto; border-left: 1px solid #e3e8ef; background: #fff; }
.src-card { margin-top: 12px; }
.meta-row { font-size: 13px; color: #6b7280; margin: 6px 0 0; }
.src { border-bottom: 1px dashed #eee; padding: 8px 0; }
.src-title { font-weight: 600; font-size: 13px; }
.src-text { font-size: 12px; color: #6b7280; margin: 4px 0; max-height: 80px; overflow: hidden; }
.src-score { font-size: 12px; color: #2f6fed; }
</style>

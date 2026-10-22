<template>
  <div class="docs">
    <el-card shadow="never" class="form-card">
      <template #header>新增文档（自动分块入检索索引）</template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="如：产品使用 FAQ" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="form.text" type="textarea" :rows="6"
            placeholder="粘贴文档正文，系统会自动按长度切块并进行双路召回索引" />
        </el-form-item>
        <el-form-item>
          <el-upload
            :auto-upload="false"
            :show-file-list="false"
            :on-change="onFile"
            accept=".txt,.md">
            <el-button>上传 .txt/.md 文件</el-button>
          </el-upload>
          <el-button type="primary" :disabled="!canSubmit" @click="submit"
            style="margin-left: 10px">添加文档</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <template #header>已收录文档（{{ docs.length }}）</template>
      <el-table :data="docs" empty-text="暂无文档">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="chunk_count" label="分块数" width="90" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="danger" link @click="remove(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listDocuments, addDocument, deleteDocument } from '../api.js'

const form = ref({ title: '', text: '' })
const docs = ref([])
const canSubmit = computed(() => form.value.title.trim() && form.value.text.trim())

async function refresh() { docs.value = await listDocuments() }
async function submit() {
  await addDocument(form.value.title.trim(), form.value.text.trim())
  ElMessage.success('已添加并重建索引')
  form.value = { title: '', text: '' }
  await refresh()
}
async function remove(id) {
  await deleteDocument(id)
  ElMessage.success('已删除')
  await refresh()
}
function onFile(file) {
  const raw = file.raw
  if (!raw) return
  const reader = new FileReader()
  reader.onload = () => {
    form.value.text = String(reader.result || '')
    if (!form.value.title) form.value.title = file.name
  }
  reader.readAsText(raw)
}
onMounted(refresh)
</script>

<style scoped>
.docs { padding: 16px; display: grid; gap: 16px; }
.form-card { max-width: 720px; }
</style>

<template>
  <el-container class="layout">
    <el-aside width="200px" class="aside">
      <div class="logo">EduRAG</div>
      <el-menu :default-active="active" @select="onSelect">
        <el-menu-item index="chat">
          <el-icon><ChatDotRound /></el-icon><span>智能问答</span>
        </el-menu-item>
        <el-menu-item index="docs">
          <el-icon><Document /></el-icon><span>文档管理</span>
        </el-menu-item>
        <el-menu-item index="history">
          <el-icon><Clock /></el-icon><span>会话历史</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main class="main">
      <Chat v-if="active === 'chat'" />
      <Documents v-else-if="active === 'docs'" />
      <History v-else-if="active === 'history'" />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import Chat from './views/Chat.vue'
import Documents from './views/Documents.vue'
import History from './views/History.vue'
import { ChatDotRound, Document, Clock } from '@element-plus/icons-vue'

const active = ref('chat')
const onSelect = (i) => (active.value = i)
</script>

<style scoped>
.layout { height: 100vh; }
.aside { background: #fff; border-right: 1px solid #e3e8ef; }
.logo { font-size: 20px; font-weight: 700; color: #2f6fed; padding: 18px 20px; }
.main { padding: 0; background: #f5f7fa; }
</style>

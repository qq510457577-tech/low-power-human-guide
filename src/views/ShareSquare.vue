<template>
  <div class="page-container max-w-3xl">
    <div class="flex items-center justify-between mb-8">
      <h1 class="section-title mb-0">💬 分享广场</h1>
      <router-link to="/share/submit" class="btn-primary text-sm">
        分享心得
      </router-link>
    </div>

    <p class="text-brown/70 mb-8 font-serif">
      看看他人在低功耗道路上的实践与感悟。
    </p>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16">
      <div class="text-4xl mb-4 animate-pulse">⏳</div>
      <p class="text-brown/50 font-serif">加载中...</p>
    </div>

    <!-- Error -->
    <div v-else-if="loadError" class="text-center py-16">
      <div class="text-4xl mb-4">😔</div>
      <p class="text-brown/50 font-serif mb-2">加载失败，请检查服务器是否可用</p>
      <p class="text-brown/30 text-xs mb-4">{{ loadError }}</p>
      <button @click="loadShares" class="btn-outline text-sm">
        重新加载
      </button>
    </div>

    <!-- Empty -->
    <div v-else-if="shares.length === 0" class="text-center py-16">
      <div class="text-5xl mb-4">🌱</div>
      <p class="text-brown/50 font-serif mb-4">还没有人分享心得</p>
      <router-link to="/share/submit" class="btn-outline">
        成为第一个分享的人
      </router-link>
    </div>

    <!-- Share List -->
    <div v-else class="space-y-4">
      <div v-for="share in shares" :key="share.id" class="card">
        <div class="flex items-start justify-between mb-3">
          <h3 class="font-serif text-brown font-semibold text-base">
            {{ share['标题'] || '无标题' }}
          </h3>
          <button
            @click="toggleLike(share)"
            class="flex items-center gap-1 px-2.5 py-1 rounded-full text-sm transition-colors"
            :class="likingId === share.id ? 'opacity-50' : 'hover:bg-earth/30'"
          >
            <span class="text-lg">{{ share['点赞数'] > 0 ? '❤️' : '🤍' }}</span>
            <span class="text-brown/60 text-xs">{{ share['点赞数'] || 0 }}</span>
          </button>
        </div>

        <div class="text-brown/80 text-sm whitespace-pre-wrap leading-relaxed mb-4">
          {{ share['内容'] }}
        </div>

        <div class="flex flex-wrap gap-2 mb-3">
          <span
            v-for="(point, i) in (share['提炼要点'] || [])"
            :key="i"
            class="bg-brown/10 text-brown/70 text-xs px-2.5 py-1 rounded-full"
          >
            {{ point }}
          </span>
        </div>

        <div class="flex items-center justify-between">
          <div class="text-xs text-brown/40">
            {{ formatDate(share['创建时间']) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://43.133.192.17:8888'

const shares = ref([])
const loading = ref(true)
const loadError = ref('')
const likingId = ref(null)

onMounted(() => {
  loadShares()
})

async function loadShares() {
  loading.value = true
  loadError.value = ''

  try {
    const response = await fetch(`${API_BASE}/api/share`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    shares.value = await response.json()
  } catch (e) {
    loadError.value = e.message || '无法连接服务器'
    shares.value = []
  } finally {
    loading.value = false
  }
}

async function toggleLike(share) {
  if (likingId.value) return

  likingId.value = share.id
  try {
    const response = await fetch(`${API_BASE}/api/share/${share.id}/like`, {
      method: 'POST',
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)

    const data = await response.json()
    share['点赞数'] = data.likes
  } catch (e) {
    console.error('点赞失败:', e)
  } finally {
    likingId.value = null
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''

  // 尝试解析"2026-04-27 11:53"格式
  const match = dateStr.match(/^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})/)
  if (match) {
    const [, y, m, d, h, mi] = match
    return `${y}年${parseInt(m)}月${parseInt(d)}日 ${h}:${mi}`
  }

  return dateStr
}
</script>

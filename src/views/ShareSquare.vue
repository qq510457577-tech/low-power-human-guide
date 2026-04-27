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

    <div v-if="shares.length === 0" class="text-center py-16">
      <div class="text-5xl mb-4">🌱</div>
      <p class="text-brown/50 font-serif mb-4">还没有人分享心得</p>
      <router-link to="/share/submit" class="btn-outline">
        成为第一个分享的人
      </router-link>
    </div>

    <div v-else class="space-y-4">
      <div v-for="share in shares" :key="share.id" class="card">
        <div class="text-brown/80 text-sm whitespace-pre-wrap leading-relaxed mb-4">
          {{ share.content }}
        </div>
        <div class="flex flex-wrap gap-2 mb-3">
          <span
            v-for="(point, i) in share.points"
            :key="i"
            class="bg-brown/10 text-brown/70 text-xs px-2.5 py-1 rounded-full"
          >
            {{ point }}
          </span>
        </div>
        <div class="text-xs text-brown/40">
          {{ formatDate(share.date) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const shares = ref([])

onMounted(() => {
  loadShares()
})

function loadShares() {
  const data = localStorage.getItem('low-power-shares')
  shares.value = data ? JSON.parse(data) : []
}

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const h = String(d.getHours()).padStart(2, '0')
  const m = String(d.getMinutes()).padStart(2, '0')
  return `${year}年${month}月${day}日 ${h}:${m}`
}
</script>

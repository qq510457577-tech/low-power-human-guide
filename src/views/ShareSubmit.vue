<template>
  <div class="page-container max-w-2xl">
    <h1 class="section-title text-center">💬 分享你的心得</h1>
    <p class="text-brown/70 text-center mb-8 font-serif">
      写下你在低功耗生活中的体会，让AI帮你提炼出最核心的智慧。
    </p>

    <!-- Step 1: Input -->
    <div class="card mb-6">
      <label class="block text-brown font-serif mb-2">你的心得体会</label>
      <textarea
        v-model="content"
        rows="6"
        placeholder="写下你的故事、感悟、经验……"
        class="w-full px-4 py-3 rounded-xl bg-white/60 border border-earth/30 focus:outline-none focus:border-brown placeholder:text-brown/30 text-brown resize-none"
      ></textarea>
    </div>

    <!-- AI Extract -->
    <div class="text-center mb-6">
      <button
        @click="extractWithAI"
        class="btn-primary"
        :disabled="extracting || !content.trim()"
      >
        {{ extracting ? '🤖 提炼中...' : '🤖 AI 提炼核心要素' }}
      </button>
    </div>

    <!-- Error -->
    <div
      v-if="error"
      class="card mb-6 border border-red-300 bg-red-50/50"
    >
      <p class="text-red-600 text-sm">{{ error }}</p>
    </div>

    <!-- Summary -->
    <div v-if="summary" class="card mb-6 border border-earth/30 bg-earth/10">
      <p class="font-serif text-brown/80 text-center text-sm italic">
        「{{ summary }}」
      </p>
    </div>

    <!-- Step 3: Edit Result -->
    <div v-if="extractedPoints.length" class="card mb-6">
      <h3 class="font-serif text-brown mb-3">提炼结果（可编辑）</h3>
      <div class="space-y-3">
        <div
          v-for="(point, i) in extractedPoints"
          :key="i"
          class="flex items-start gap-2"
        >
          <span class="text-brown/50 mt-1 flex-shrink-0">{{ i + 1 }}.</span>
          <input
            v-model="extractedPoints[i]"
            class="flex-1 px-3 py-2 rounded-lg bg-white/60 border border-earth/30 focus:outline-none focus:border-brown text-brown text-sm"
          />
          <button
            @click="removePoint(i)"
            class="text-brown/30 hover:text-red-500 mt-1"
          >
            ✕
          </button>
        </div>
      </div>
      <button
        @click="addPoint"
        class="mt-3 text-sm text-brown/50 hover:text-brown"
      >
        + 添加一条
      </button>
    </div>

    <!-- Step 4: Title & Publish -->
    <div v-if="extractedPoints.length" class="card mb-6">
      <label class="block text-brown font-serif mb-2">标题</label>
      <input
        v-model="title"
        type="text"
        placeholder="给这次分享取个标题……"
        class="w-full px-4 py-2.5 rounded-xl bg-white/60 border border-earth/30 focus:outline-none focus:border-brown placeholder:text-brown/30 text-brown"
      />
    </div>

    <!-- Step 5: Preview -->
    <div v-if="extractedPoints.length" class="card mb-6">
      <h3 class="font-serif text-brown mb-3">预览</h3>
      <div class="bg-earth/20 rounded-xl p-4">
        <p class="text-brown/80 text-sm whitespace-pre-wrap">{{ content }}</p>
      </div>
      <div class="mt-3 flex flex-wrap gap-2">
        <span
          v-for="(point, i) in extractedPoints"
          :key="i"
          class="bg-brown/10 text-brown/70 text-xs px-2 py-1 rounded-full"
        >
          {{ point }}
        </span>
      </div>
    </div>

    <div v-if="extractedPoints.length" class="text-center">
      <button
        @click="publish"
        class="btn-primary"
        :disabled="publishing || !title.trim()"
      >
        {{ publishing ? '📤 发布中...' : '📤 发布到分享广场' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API_BASE = 'http://43.133.192.17:8888'

const router = useRouter()

const content = ref('')
const title = ref('')
const extracting = ref(false)
const publishing = ref(false)
const error = ref('')
const extractedPoints = ref([])
const summary = ref('')

function addPoint() {
  extractedPoints.value.push('')
}

function removePoint(i) {
  extractedPoints.value.splice(i, 1)
}

async function extractWithAI() {
  if (!content.value.trim()) {
    error.value = '请输入心得内容'
    return
  }

  extracting.value = true
  error.value = ''
  summary.value = ''

  try {
    const response = await fetch(`${API_BASE}/api/extract`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: content.value }),
    })

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}))
      throw new Error(errData.detail || `请求失败 (${response.status})`)
    }

    const data = await response.json()
    extractedPoints.value = (data.points || []).slice(0, 5)
    summary.value = data.summary || ''

    if (extractedPoints.value.length === 0) {
      extractedPoints.value = ['未能自动提炼，请手动编辑']
    }
  } catch (e) {
    error.value = e.message || '提炼失败，请稍后再试'
    extractedPoints.value = []
  } finally {
    extracting.value = false
  }
}

async function publish() {
  const validPoints = extractedPoints.value.filter((p) => p.trim())
  if (validPoints.length === 0) {
    error.value = '请至少保留一条核心要点'
    return
  }
  if (!title.value.trim()) {
    error.value = '请输入标题'
    return
  }

  publishing.value = true
  error.value = ''

  try {
    const response = await fetch(`${API_BASE}/api/share`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: title.value,
        content: content.value,
        points: validPoints,
      }),
    })

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}))
      throw new Error(errData.detail || `发布失败 (${response.status})`)
    }

    // Reset form
    content.value = ''
    title.value = ''
    extractedPoints.value = []
    summary.value = ''

    // Navigate to square
    router.push('/share/square')
  } catch (e) {
    error.value = e.message || '发布失败，请稍后再试'
  } finally {
    publishing.value = false
  }
}
</script>

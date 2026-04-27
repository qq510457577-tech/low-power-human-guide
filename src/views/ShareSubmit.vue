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

    <!-- API Key -->
    <div class="card mb-6">
      <label class="block text-brown font-serif mb-2">DeepSeek API Key</label>
      <div class="flex gap-2">
        <input
          v-model="apiKey"
          type="password"
          placeholder="sk-..."
          class="flex-1 px-4 py-2.5 rounded-xl bg-white/60 border border-earth/30 focus:outline-none focus:border-brown placeholder:text-brown/30 text-brown text-sm"
        />
        <button
          @click="showKey = !showKey"
          class="px-3 py-2 rounded-xl border border-earth/30 text-brown/60 hover:text-brown text-sm"
        >
          {{ showKey ? '隐藏' : '显示' }}
        </button>
      </div>
      <p class="text-xs text-brown/40 mt-2">API Key 仅存储在本地浏览器，不会上传到服务器</p>
    </div>

    <!-- Step 2: AI Extract -->
    <div class="text-center mb-6">
      <button
        @click="extractWithAI"
        class="btn-primary"
        :disabled="extracting || !content.trim() || !apiKey.trim()"
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

    <!-- Step 4: Preview & Publish -->
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
      >
        📤 发布到分享广场
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const content = ref('')
const apiKey = ref('')
const showKey = ref(false)
const extracting = ref(false)
const error = ref('')
const extractedPoints = ref([])

onMounted(() => {
  // Restore API key from localStorage
  const savedKey = localStorage.getItem('low-power-deepseek-key')
  if (savedKey) {
    apiKey.value = savedKey
  }
})

function addPoint() {
  extractedPoints.value.push('')
}

function removePoint(i) {
  extractedPoints.value.splice(i, 1)
}

async function extractWithAI() {
  if (!content.value.trim() || !apiKey.value.trim()) {
    error.value = '请输入心得内容和API Key'
    return
  }

  // Save API key
  localStorage.setItem('low-power-deepseek-key', apiKey.value)

  extracting.value = true
  error.value = ''

  try {
    const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`,
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          {
            role: 'system',
            content: '你是一个低功耗生活方式的提炼者。用户会分享一段关于健康生活、极简主义、冥想、运动、欲望管理等方面的心得体会。请从中提炼出3-5条最核心的要素/要点。每一条必须是精炼的一句话（15字以内），不要使用序号。用以下JSON格式回复：{"points": ["要点1", "要点2", ...]}',
          },
          {
            role: 'user',
            content: content.value,
          },
        ],
        temperature: 0.3,
        max_tokens: 500,
      }),
    })

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}))
      throw new Error(errData.error?.message || `API 请求失败 (${response.status})`)
    }

    const data = await response.json()
    const text = data.choices?.[0]?.message?.content || ''

    // Try to parse JSON from response
    let points = []
    try {
      const parsed = JSON.parse(text)
      points = parsed.points || []
    } catch {
      // Fallback: extract lines
      points = text
        .split('\n')
        .map((l) => l.replace(/^[\d.、\-*]+\s*/, '').trim())
        .filter(Boolean)
    }

    extractedPoints.value = points.slice(0, 5)
    if (extractedPoints.value.length === 0) {
      extractedPoints.value = ['未能自动提炼，请手动编辑']
    }
  } catch (e) {
    error.value = e.message || '提炼失败，请检查API Key是否正确'
    extractedPoints.value = []
  } finally {
    extracting.value = false
  }
}

function publish() {
  const validPoints = extractedPoints.value.filter((p) => p.trim())
  if (validPoints.length === 0) {
    error.value = '请至少保留一条核心要点'
    return
  }

  const share = {
    id: Date.now(),
    content: content.value,
    points: validPoints,
    date: new Date().toISOString(),
  }

  // Save to localStorage
  const existing = JSON.parse(localStorage.getItem('low-power-shares') || '[]')
  existing.unshift(share)
  localStorage.setItem('low-power-shares', JSON.stringify(existing))

  // Reset form
  content.value = ''
  extractedPoints.value = []

  // Navigate to square
  router.push('/share/square')
}
</script>

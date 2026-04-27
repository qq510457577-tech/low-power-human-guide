<template>
  <div class="page-container max-w-3xl">
    <h1 class="section-title text-center">📖 指南文章</h1>
    <p class="text-brown/70 text-center mb-8 font-serif">
      系统化的低功耗生存知识库
    </p>

    <!-- Search -->
    <div class="mb-8">
      <input
        v-model="search"
        type="text"
        placeholder="搜索文章..."
        class="w-full px-4 py-3 rounded-xl bg-white/60 border border-earth/30 focus:outline-none focus:border-brown placeholder:text-brown/30 text-brown"
      />
    </div>

    <!-- Category Filter -->
    <div class="flex flex-wrap gap-2 mb-8">
      <button
        @click="activeCategory = ''"
        class="px-3 py-1.5 rounded-full text-sm font-serif transition-colors"
        :class="activeCategory === '' ? 'bg-brown text-cream' : 'bg-earth/30 text-brown/70 hover:bg-earth/50'"
      >
        全部
      </button>
      <button
        v-for="cat in categories"
        :key="cat"
        @click="activeCategory = cat"
        class="px-3 py-1.5 rounded-full text-sm font-serif transition-colors"
        :class="activeCategory === cat ? 'bg-brown text-cream' : 'bg-earth/30 text-brown/70 hover:bg-earth/50'"
      >
        {{ cat }}
      </button>
    </div>

    <!-- Articles Grid -->
    <div v-if="filteredArticles.length" class="space-y-4">
      <router-link
        v-for="article in filteredArticles"
        :key="article.id"
        :to="`/articles/${article.id}`"
        class="card block hover:bg-earth/20 transition-colors"
      >
        <div class="flex items-start gap-4">
          <div class="text-3xl flex-shrink-0">{{ article.emoji }}</div>
          <div>
            <h2 class="font-serif text-brown text-lg mb-1">{{ article.title }}</h2>
            <p class="text-brown/60 text-sm mb-2">{{ article.summary }}</p>
            <div class="flex items-center gap-3 text-xs text-brown/40">
              <span>{{ article.category }}</span>
              <span>{{ article.readTime }}</span>
            </div>
          </div>
        </div>
      </router-link>
    </div>
    <div v-else class="text-center py-12 text-brown/50 font-serif">
      没有找到匹配的文章
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const search = ref('')
const activeCategory = ref('')

const articles = [
  {
    id: 1,
    emoji: '🧠',
    title: '心外无物：你的注意力就是你的现实',
    summary: '当王阳明说"心外无物"时，他揭示了一个被现代科学验证的真相：你的注意力塑造了你的现实世界。',
    category: '哲学',
    readTime: '5 分钟阅读',
  },
  {
    id: 2,
    emoji: '📱',
    title: '数字极简主义：如何夺回被偷走的注意力',
    summary: '社交媒体和短视频是如何在不知不觉中消耗你的生命能量？重新审视你和屏幕的关系。',
    category: '数字生活',
    readTime: '8 分钟阅读',
  },
  {
    id: 3,
    emoji: '💪',
    title: '最低功耗的身体：每天15分钟的高效运动法',
    summary: '不需要去健身房、不需要专业器械，用最低的时间投入维持身体的最佳状态。',
    category: '运动',
    readTime: '6 分钟阅读',
  },
  {
    id: 4,
    emoji: '🛡️',
    title: '欲望的真相：区分真实需求与被制造的欲望',
    summary: '消费主义如何将"想要"伪装成"需要"？掌握辨别的方法，从欲望的枷锁中解脱。',
    category: '欲望管理',
    readTime: '7 分钟阅读',
  },
  {
    id: 5,
    emoji: '🧘',
    title: '冥想入门：从1分钟开始的正念练习',
    summary: '你不必成为禅师才能冥想。从每天1分钟开始，逐步建立自己的正念习惯。',
    category: '冥想',
    readTime: '4 分钟阅读',
  },
  {
    id: 6,
    emoji: '🌙',
    title: '睡眠优先：最低成本最高回报的健康投资',
    summary: '没有什么比良好的睡眠更能提升生活质量。建立以睡眠为核心的作息体系。',
    category: '健康',
    readTime: '6 分钟阅读',
  },
  {
    id: 7,
    emoji: '🎯',
    title: '意志力的使用指南：如何保护你的决策能量',
    summary: '意志力是有限的资源。学会像管理预算一样管理你的意志力。',
    category: '心理',
    readTime: '5 分钟阅读',
  },
  {
    id: 8,
    emoji: '🥗',
    title: '最简单的饮食法则：人体的最低能耗燃料',
    summary: '不需要复杂食谱和昂贵的超级食物。回归最基础、最天然的食物选择。',
    category: '饮食',
    readTime: '6 分钟阅读',
  },
  {
    id: 9,
    emoji: '🌿',
    title: '极简主义生活实践：从整理房间到整理心灵',
    summary: '外在的秩序带来内心的秩序。从最小行动开始，逐步简化你的生活。',
    category: '生活',
    readTime: '7 分钟阅读',
  },
  {
    id: 10,
    emoji: '📝',
    title: '每日复盘：5分钟的自省仪式',
    summary: '用最简短的复盘日记，将每一天的经验内化为成长的养分。',
    category: '反思',
    readTime: '4 分钟阅读',
  },
  {
    id: 11,
    emoji: '🤝',
    title: '低功耗社交：告别社交焦虑的关系法则',
    summary: '减少无效社交，培养真正有意义的人际关系。少而精胜过多而浅。',
    category: '社交',
    readTime: '6 分钟阅读',
  },
  {
    id: 12,
    emoji: '💡',
    title: '一次只做一件事：单任务的复利效应',
    summary: '多任务处理是一个谎言。拥抱单任务模式，你会发现效率和质量都会提升。',
    category: '效率',
    readTime: '5 分钟阅读',
  },
]

const categories = computed(() => {
  const set = new Set(articles.map((a) => a.category))
  return [...set]
})

const filteredArticles = computed(() => {
  return articles.filter((a) => {
    const matchSearch =
      !search.value ||
      a.title.includes(search.value) ||
      a.summary.includes(search.value)
    const matchCategory =
      !activeCategory.value || a.category === activeCategory.value
    return matchSearch && matchCategory
  })
})
</script>

<template>
  <div class="page-container max-w-2xl">
    <h1 class="section-title text-center">低功耗自测</h1>
    <p class="text-brown/70 text-center mb-8 font-serif">
      诚实地回答以下问题，评估你的生活方式能耗水平。
    </p>

    <div v-if="!finished" class="space-y-6">
      <div v-for="(q, i) in questions" :key="i" class="card">
        <p class="font-serif text-brown mb-4">
          <span class="text-brown/50 text-sm">{{ i + 1 }}/{{ questions.length }}</span>
          {{ q.text }}
        </p>
        <div class="space-y-2">
          <label
            v-for="(opt, oi) in q.options"
            :key="oi"
            class="flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-colors"
            :class="answers[i] === oi ? 'bg-earth/40' : 'hover:bg-earth/20'"
          >
            <input
              type="radio"
              :name="'q-' + i"
              :value="oi"
              v-model="answers[i]"
              class="accent-brown"
            />
            <span class="text-sm text-brown/80">{{ opt.label }}</span>
          </label>
        </div>
      </div>

      <div class="text-center pt-4">
        <button @click="submitTest" class="btn-primary" :disabled="!allAnswered">
          查看结果
        </button>
      </div>
    </div>

    <!-- Results -->
    <div v-else class="text-center">
      <div class="card mb-8">
        <div class="text-5xl mb-4">{{ resultEmoji }}</div>
        <h2 class="text-2xl font-serif text-brown mb-2">{{ resultTitle }}</h2>
        <p class="text-brown/70 mb-6">{{ resultDesc }}</p>
        <div class="flex justify-center gap-2 mb-4">
          <span
            v-for="level in 5"
            :key="level"
            class="w-8 h-8 rounded-full transition-colors"
            :class="level <= scoreLevel ? 'bg-brown' : 'bg-earth/40'"
          ></span>
        </div>
        <p class="text-sm text-brown/50">能耗等级：{{ scoreLevel }}/5</p>
      </div>

      <div class="grid sm:grid-cols-2 gap-4">
        <router-link to="/daily-actions" class="btn-primary">
          查看每日微行动
        </router-link>
        <button @click="resetTest" class="btn-outline">
          重新测试
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const questions = [
  {
    text: '你每天花在短视频/社交媒体上的时间大约多久？',
    options: [
      { label: '不到30分钟', score: 1 },
      { label: '30分钟~1小时', score: 2 },
      { label: '1~2小时', score: 3 },
      { label: '2~4小时', score: 4 },
      { label: '超过4小时', score: 5 },
    ],
  },
  {
    text: '你每天起床后第一件事是什么？',
    options: [
      { label: '静坐/冥想/拉伸', score: 1 },
      { label: '喝水/洗漱/规划一天', score: 2 },
      { label: '看手机消息', score: 3 },
      { label: '刷社交媒体', score: 4 },
      { label: '打开短视频App', score: 5 },
    ],
  },
  {
    text: '你每周运动几次？',
    options: [
      { label: '每天都有运动习惯', score: 1 },
      { label: '3~5次', score: 2 },
      { label: '1~2次', score: 3 },
      { label: '偶尔想起来才动', score: 4 },
      { label: '几乎不运动', score: 5 },
    ],
  },
  {
    text: '面对想买的东西，你通常会？',
    options: [
      { label: '认真评估是否真的需要，设置冷静期', score: 1 },
      { label: '考虑几天后再决定', score: 2 },
      { label: '想买就买，但控制预算', score: 3 },
      { label: '被广告/推荐打动就下单', score: 4 },
      { label: '经常冲动消费后后悔', score: 5 },
    ],
  },
  {
    text: '你的睡眠质量如何？',
    options: [
      { label: '规律作息，睡醒精力充沛', score: 1 },
      { label: '基本规律，偶尔熬夜', score: 2 },
      { label: '经常熬夜但能补觉', score: 3 },
      { label: '睡眠不规律，经常失眠', score: 4 },
      { label: '严重睡眠不足或昼夜颠倒', score: 5 },
    ],
  },
  {
    text: '你能够专注做一件事多久？（不被打断）',
    options: [
      { label: '2小时以上', score: 1 },
      { label: '1~2小时', score: 2 },
      { label: '30分钟~1小时', score: 3 },
      { label: '10~30分钟', score: 4 },
      { label: '不到10分钟就想切换', score: 5 },
    ],
  },
  {
    text: '你觉得自己的信息过载程度如何？',
    options: [
      { label: '能主动筛选信息，很少焦虑', score: 1 },
      { label: '有一定的信息筛选能力', score: 2 },
      { label: '经常被信息轰炸但能处理', score: 3 },
      { label: '感觉信息太多，经常焦虑', score: 4 },
      { label: '完全被信息淹没，无法思考', score: 5 },
    ],
  },
  {
    text: '你每天独处/静默的时间有多长？',
    options: [
      { label: '超过1小时', score: 1 },
      { label: '30分钟~1小时', score: 2 },
      { label: '15~30分钟', score: 3 },
      { label: '不到15分钟', score: 4 },
      { label: '几乎没有独处时间', score: 5 },
    ],
  },
]

const answers = ref(questions.map(() => null))
const finished = ref(false)

const allAnswered = computed(() => answers.value.every((a) => a !== null))

const totalScore = computed(() => {
  return answers.value.reduce((sum, ai, i) => {
    return sum + (ai !== null ? questions[i].options[ai].score : 0)
  }, 0)
})

const scoreLevel = computed(() => {
  const s = totalScore.value
  if (s <= 10) return 1
  if (s <= 16) return 2
  if (s <= 22) return 3
  if (s <= 28) return 4
  return 5
})

const resultEmoji = computed(() => {
  const map = { 1: '🌟', 2: '🌿', 3: '⚡', 4: '🔥', 5: '🚨' }
  return map[scoreLevel.value] || '🌿'
})

const resultTitle = computed(() => {
  const map = {
    1: '低功耗大师',
    2: '节能先锋',
    3: '中等能耗',
    4: '高能耗预警',
    5: '超载危机',
  }
  return map[scoreLevel.value] || '中等能耗'
})

const resultDesc = computed(() => {
  const map = {
    1: '你的生活方式非常可持续！你已经掌握了低功耗生存的精髓。继续保持，并分享你的经验帮助他人。',
    2: '你的能耗水平良好，在多数方面做得不错。还有少量优化空间，加油！',
    3: '你的生活方式处于平均水平。有很多可以改进的地方，从每日微行动开始吧。',
    4: '你的能耗偏高。是时候认真审视自己的习惯了，建议从减少屏幕时间和增加运动入手。',
    5: '你的生活方式处于高能耗状态。请立即采取行动，从最小的改变开始——哪怕只是放下手机深呼吸一分钟。',
  }
  return map[scoreLevel.value] || ''
})

function submitTest() {
  if (!allAnswered.value) return
  finished.value = true
}

function resetTest() {
  answers.value = questions.map(() => null)
  finished.value = false
}
</script>

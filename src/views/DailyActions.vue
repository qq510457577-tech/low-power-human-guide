<template>
  <div class="page-container max-w-2xl">
    <h1 class="section-title text-center">🌱 每日微行动</h1>
    <p class="text-brown/70 text-center mb-8 font-serif">
      每天一个低门槛的小行动，不追求完美，只追求开始。
    </p>

    <!-- Today's Card -->
    <div class="card mb-8 text-center">
      <p class="text-sm text-brown/50 mb-1">{{ todayLabel }}</p>
      <div class="text-4xl mb-3">{{ dailyItem.emoji }}</div>
      <h2 class="text-xl font-serif text-brown mb-2">{{ dailyItem.title }}</h2>
      <p class="text-brown/70 text-sm leading-relaxed mb-4">{{ dailyItem.desc }}</p>
      <div class="flex justify-center gap-2">
        <span
          v-for="tag in dailyItem.tags"
          :key="tag"
          class="text-xs bg-earth/30 text-brown/70 px-2 py-1 rounded-full"
        >
          {{ tag }}
        </span>
      </div>
    </div>

    <!-- Completed Toggle -->
    <div class="text-center mb-8">
      <button
        @click="toggleDone"
        class="btn-primary"
        :class="{ 'opacity-60': todayDone }"
      >
        {{ todayDone ? '✅ 已完成' : '标记完成' }}
      </button>
    </div>

    <!-- All Actions -->
    <div class="mb-12">
      <h3 class="font-serif text-brown text-lg mb-4">全部微行动</h3>
      <div class="space-y-3">
        <div
          v-for="(act, i) in actions"
          :key="i"
          class="card flex items-start gap-4 cursor-pointer hover:bg-earth/20 transition-colors"
          :class="{ 'opacity-50': completedActions[i] }"
          @click="toggleAction(i)"
        >
          <div class="text-2xl flex-shrink-0 pt-1">{{ act.emoji }}</div>
          <div class="flex-1">
            <h4 class="font-serif text-brown mb-1" :class="{ 'line-through': completedActions[i] }">
              {{ act.title }}
            </h4>
            <p class="text-brown/60 text-xs">{{ act.desc }}</p>
          </div>
          <div class="flex-shrink-0 pt-1">
            <span v-if="completedActions[i]" class="text-green-600">✓</span>
            <span v-else class="text-brown/30 w-5 h-5 rounded-full border border-brown/30 inline-block"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress -->
    <div class="card text-center">
      <p class="text-sm text-brown/60 font-serif">
        已完成 {{ completedCount }} / {{ actions.length }}
      </p>
      <div class="w-full bg-earth/30 rounded-full h-2 mt-2 overflow-hidden">
        <div
          class="bg-brown h-full rounded-full transition-all duration-500"
          :style="{ width: progressPercent + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const actions = [
  { emoji: '🧘', title: '晨起静坐5分钟', desc: '起床后，不碰手机，静坐5分钟，感受呼吸', tags: ['冥想', '早晨'] },
  { emoji: '💧', title: '空腹喝一杯温水', desc: '起床后第一杯水，唤醒身体代谢', tags: ['健康', '早晨'] },
  { emoji: '📝', title: '写下三件感恩的事', desc: '花3分钟写下昨天值得感恩的三件事', tags: ['心态', '早晨'] },
  { emoji: '🚶', title: '散步15分钟', desc: '不戴耳机，不刷手机，单纯地走路', tags: ['运动', '户外'] },
  { emoji: '📵', title: '无手机用餐', desc: '吃饭时不看任何屏幕，品味食物', tags: ['专注', '饮食'] },
  { emoji: '📖', title: '读纸质书10页', desc: '放下手机，读一本真正的纸质书', tags: ['学习', '专注'] },
  { emoji: '🌿', title: '整理一个角落', desc: '整理房间中最小的一块区域，建立秩序感', tags: ['整理', '环境'] },
  { emoji: '🤫', title: '沉默1小时', desc: '不说不必要的话，感受沉默的力量', tags: ['冥想', '挑战'] },
  { emoji: '✍️', title: '手写日记3分钟', desc: '用笔和纸写下今天的感受，不追求文采', tags: ['反思', '书写'] },
  { emoji: '🧹', title: '关闭一个App通知', desc: '关掉一个不必要的通知，夺回注意力', tags: ['数字极简', '专注'] },
  { emoji: '🏋️', title: '做10个俯卧撑', desc: '不需要去健身房，随时随地开始', tags: ['运动', '力量'] },
  { emoji: '🧠', title: '学习一个新词', desc: '学一个外语单词或新概念，扩充认知边界', tags: ['学习', '成长'] },
  { emoji: '🎯', title: '设定今日三件要事', desc: '早晨花2分钟确定今天最重要的三件事', tags: ['效率', '规划'] },
  { emoji: '🌙', title: '提前30分钟放下手机', desc: '睡前半小时不碰任何电子设备', tags: ['睡眠', '数字极简'] },
  { emoji: '🥗', title: '吃一份绿叶蔬菜', desc: '今天至少吃一份深绿色蔬菜', tags: ['饮食', '健康'] },
  { emoji: '💨', title: '深呼吸1分钟', desc: '闭上眼睛，4-7-8呼吸法：吸气4秒，屏息7秒，呼气8秒', tags: ['冥想', '减压'] },
  { emoji: '🎧', title: '听一首纯音乐', desc: '不带歌词的纯音乐，让大脑休息', tags: ['放松', '音乐'] },
  { emoji: '📦', title: '断舍离一样物品', desc: '扔/捐/卖掉一件不需要的东西', tags: ['整理', '极简'] },
  { emoji: '☀️', title: '晒太阳10分钟', desc: '早晨或傍晚晒10分钟太阳，补充维生素D', tags: ['健康', '户外'] },
  { emoji: '🤝', title: '真诚地赞美一个人', desc: '对身边的人说一句真心话的赞美', tags: ['社交', '心态'] },
  { emoji: '⏰', title: '设置一个勿扰时段', desc: '今天安排1小时勿扰时间，专注做一件事', tags: ['专注', '效率'] },
  { emoji: '🧩', title: '完成一件拖延的事', desc: '挑一件拖延已久的小事，用5分钟搞定它', tags: ['效率', '心态'] },
]

const completedActions = ref(actions.map(() => false))
const todayDone = ref(false)

const todayIndex = computed(() => {
  const day = new Date().getDate()
  return day % actions.length
})

const dailyItem = computed(() => actions[todayIndex.value])

const todayLabel = computed(() => {
  const now = new Date()
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  return `${now.getMonth() + 1}月${now.getDate()}日 星期${weekdays[now.getDay()]}`
})

const completedCount = computed(() => completedActions.value.filter(Boolean).length)

const progressPercent = computed(() => {
  return Math.round((completedCount.value / actions.length) * 100)
})

function toggleAction(i) {
  completedActions.value[i] = !completedActions.value[i]
  saveState()
  trackDaily()
}

function toggleDone() {
  todayDone.value = !todayDone.value
  saveState()
}

function saveState() {
  localStorage.setItem(
    'low-power-actions',
    JSON.stringify({
      completed: completedActions.value,
      todayDone: todayDone.value,
      date: new Date().toDateString(),
    })
  )
}

function trackDaily() {
  // Check if today's action is marked
  if (completedActions.value[todayIndex.value]) {
    todayDone.value = true
  }
}

onMounted(() => {
  const saved = localStorage.getItem('low-power-actions')
  if (saved) {
    const data = JSON.parse(saved)
    if (data.date === new Date().toDateString()) {
      completedActions.value = data.completed
      todayDone.value = data.todayDone
    }
  }
})
</script>

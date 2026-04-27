<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="sticky top-0 z-50 bg-cream/90 backdrop-blur-sm border-b border-earth/30">
      <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-2">
          <span class="text-2xl">🧘</span>
          <span class="font-serif text-brown text-lg hidden sm:inline">人类低功耗生存指南</span>
          <span class="font-serif text-brown text-lg sm:hidden">低功耗指南</span>
        </router-link>
        <nav class="flex items-center gap-1 md:gap-4">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="px-3 py-1.5 rounded-full text-sm font-serif text-brown/70 hover:text-brown hover:bg-earth/30 transition-colors"
            :class="{ 'bg-earth/40 text-brown': isActive(item.path) }"
          >
            {{ item.name }}
          </router-link>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="border-t border-earth/30 py-8 mt-12">
      <div class="max-w-6xl mx-auto px-4 text-center">
        <p class="text-brown/60 text-sm font-serif">
          「心外无物，心外无理」—— 王阳明
        </p>
        <p class="text-brown/40 text-xs mt-2">
          人类低功耗生存指南 · 以主观意志照亮生活
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/', name: '首页' },
  { path: '/self-test', name: '低功耗自测' },
  { path: '/daily-actions', name: '每日微行动' },
  { path: '/articles', name: '指南文章' },
  { path: '/share/square', name: '分享广场' },
]

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

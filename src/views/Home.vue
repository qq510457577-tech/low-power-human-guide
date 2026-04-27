<template>
  <div class="page-container">
    <!-- Hero -->
    <section class="text-center py-12 md:py-20">
      <div class="text-6xl mb-6">🧘</div>
      <h1 class="text-4xl md:text-5xl font-serif text-dark mb-4">人类低功耗生存指南</h1>
      <p class="text-lg md:text-xl text-brown/80 font-serif max-w-2xl mx-auto leading-relaxed">
        在这个信息过载、欲望横流的时代，<br class="hidden sm:block" />
        回归内心的秩序，以最少的能耗活出最大的意义。
      </p>
    </section>

    <!-- 心外无物 -->
    <section class="max-w-3xl mx-auto mb-16">
      <div class="card text-center">
        <h2 class="section-title">心外无物 · 心外无理</h2>
        <p class="text-brown/80 leading-relaxed mb-4">
          王阳明说：「你未看此花时，此花与汝心同归于寂。你来看此花时，则此花颜色一时明白起来。」
        </p>
        <p class="text-brown/80 leading-relaxed">
          外在的世界，不过是内心投射的镜像。当我们调整内心的频率，外在的现实也随之改变。
          这不是唯心主义的幻想，而是被现代神经科学验证的真理——<strong>你的注意力塑造你的现实</strong>。
        </p>
      </div>
    </section>

    <!-- 三大支柱 -->
    <section class="max-w-5xl mx-auto mb-16">
      <h2 class="section-title text-center">三大生存支柱</h2>
      <div class="grid md:grid-cols-3 gap-6 mt-8">
        <div class="card text-center">
          <div class="text-4xl mb-4">🧠</div>
          <h3 class="text-xl font-serif text-brown mb-3">主观意志</h3>
          <p class="text-brown/70 text-sm leading-relaxed">
            你的意志是唯一真正的力量。在被动接收信息的洪流中，主动选择你的注意力投向何处。
          </p>
        </div>
        <div class="card text-center">
          <div class="text-4xl mb-4">🛡️</div>
          <h3 class="text-xl font-serif text-brown mb-3">抵御欲望</h3>
          <p class="text-brown/70 text-sm leading-relaxed">
            区分真实需求与被制造的欲望。少即是多，简单即是自由。每拒绝一个不必要的欲望，就节省一份能量。
          </p>
        </div>
        <div class="card text-center">
          <div class="text-4xl mb-4">💪</div>
          <h3 class="text-xl font-serif text-brown mb-3">锻炼身体</h3>
          <p class="text-brown/70 text-sm leading-relaxed">
            身体是意志的载体。最低功耗的生存需要一个高效运转的身体作为基础。
          </p>
        </div>
      </div>
    </section>

    <!-- 快速入口 -->
    <section class="max-w-3xl mx-auto mb-16">
      <div class="grid sm:grid-cols-2 gap-4">
        <router-link to="/self-test" class="card hover:bg-earth/20 transition-colors block">
          <div class="text-2xl mb-2">📋</div>
          <h3 class="font-serif text-brown text-lg mb-1">低功耗自测</h3>
          <p class="text-brown/60 text-sm">评估你的生活方式能耗水平</p>
        </router-link>
        <router-link to="/daily-actions" class="card hover:bg-earth/20 transition-colors block">
          <div class="text-2xl mb-2">🌱</div>
          <h3 class="font-serif text-brown text-lg mb-1">每日微行动</h3>
          <p class="text-brown/60 text-sm">每天一个小行动，改变从今天开始</p>
        </router-link>
        <router-link to="/articles" class="card hover:bg-earth/20 transition-colors block">
          <div class="text-2xl mb-2">📖</div>
          <h3 class="font-serif text-brown text-lg mb-1">指南文章</h3>
          <p class="text-brown/60 text-sm">系统化的生存指南内容</p>
        </router-link>
        <router-link to="/share/square" class="card hover:bg-earth/20 transition-colors block">
          <div class="text-2xl mb-2">💬</div>
          <h3 class="font-serif text-brown text-lg mb-1">分享广场</h3>
          <p class="text-brown/60 text-sm">看看他人在低功耗道路上的心得</p>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

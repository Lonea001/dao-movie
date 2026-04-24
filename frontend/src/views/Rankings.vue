<template>
  <div>
    <h2 class="page-title">🏆 精选榜单</h2>

    <div v-loading="loading">
      <div class="ranking-grid" v-if="rankings.length">
        <div
          class="ranking-card"
          v-for="(r, index) in rankings"
          :key="r.id"
          @click="$router.push(`/rankings/${r.id}`)"
        >
          <div class="rank-no">#{{ index + 1 }}</div>
          <div class="card-body">
            <h3 class="name">{{ r.name }}</h3>
            <p class="desc">{{ r.description || '暂无简介' }}</p>
            <div class="footer">
              <span class="count">共 {{ r.movie_count }} 部电影</span>
              <span class="link">查看榜单 →</span>
            </div>
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无榜单，管理员可在后台创建" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRankings } from '@/api/rankings'

const rankings = ref([])
const loading  = ref(false)

onMounted(async () => {
  loading.value  = true
  const res      = await getRankings()
  rankings.value = res.items || []
  loading.value  = false
})
</script>

<style scoped>
.page-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
}
.ranking-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.ranking-card {
  display: flex;
  gap: 20px;
  align-items: center;
  background: white;
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 4px solid #e94560;
}
.ranking-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}
.rank-no {
  font-size: 36px;
  font-weight: 900;
  color: #e94560;
  min-width: 56px;
  text-align: center;
  opacity: 0.8;
}
.card-body  { flex: 1; }
.name       { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
.desc       { font-size: 14px; color: #888; margin-bottom: 12px; }
.footer     { display: flex; justify-content: space-between; }
.count      { font-size: 13px; color: #aaa; }
.link       { font-size: 13px; color: #e94560; }
</style>
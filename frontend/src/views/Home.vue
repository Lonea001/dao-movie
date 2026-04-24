<template>
  <div>
    <!-- Banner -->
    <div class="banner">
      <h1>大盗影视</h1>
      <p>发现好电影，探索精彩世界</p>
      <el-input
        v-model="searchQ"
        placeholder="搜索电影、导演、演员..."
        size="large"
        class="search-input"
        @keyup.enter="goSearch"
      >
        <template #append>
          <el-button type="primary" @click="goSearch">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 评分最高 -->
    <section class="section">
      <div class="section-header">
        <h2>⭐ 评分最高</h2>
        <router-link to="/movies?sort_by=rating">查看更多 →</router-link>
      </div>
      <div class="movie-grid" v-loading="loading">
        <MovieCard v-for="m in topMovies" :key="m.id" :movie="m" />
      </div>
    </section>

    <!-- 榜单入口 -->
    <section class="section">
      <div class="section-header">
        <h2>🏆 精选榜单</h2>
        <router-link to="/rankings">全部榜单 →</router-link>
      </div>
      <div class="ranking-list" v-if="rankings.length">
        <div
          class="ranking-card"
          v-for="r in rankings.slice(0, 4)"
          :key="r.id"
          @click="$router.push(`/rankings/${r.id}`)"
        >
          <div class="ranking-name">{{ r.name }}</div>
          <div class="ranking-desc">{{ r.description || '点击查看详情' }}</div>
          <div class="ranking-count">共 {{ r.movie_count }} 部</div>
        </div>
      </div>
      <el-empty v-else description="暂无榜单，管理员可在后台创建" />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MovieCard from '@/components/MovieCard.vue'
import { getTopMovies } from '@/api/movies'
import { getRankings } from '@/api/rankings'

const router   = useRouter()
const searchQ  = ref('')
const topMovies= ref([])
const rankings = ref([])
const loading  = ref(false)

const goSearch = () => {
  if (searchQ.value.trim()) {
    router.push({ path: '/movies', query: { q: searchQ.value } })
  }
}

onMounted(async () => {
  loading.value = true
  const [moviesRes, rankingsRes] = await Promise.all([
    getTopMovies(12),
    getRankings(),
  ])
  topMovies.value = moviesRes.items || []
  rankings.value  = rankingsRes.items || []
  loading.value   = false
})
</script>

<style scoped>
/* Banner */
.banner {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
  color: white;
  text-align: center;
  padding: 60px 24px;
  border-radius: 12px;
  margin-bottom: 40px;
}
.banner h1 {
  font-size: 42px;
  font-weight: 800;
  color: #e94560;
  margin-bottom: 8px;
}
.banner p {
  color: #aaa;
  font-size: 16px;
  margin-bottom: 24px;
}
.search-input {
  max-width: 500px;
}

/* 区块 */
.section {
  margin-bottom: 48px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.section-header h2 {
  font-size: 22px;
  font-weight: 700;
}
.section-header a {
  color: #e94560;
  text-decoration: none;
  font-size: 14px;
}

/* 电影网格 */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}

/* 榜单卡片 */
.ranking-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}
.ranking-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border-left: 4px solid #e94560;
  transition: transform 0.2s;
}
.ranking-card:hover {
  transform: translateY(-3px);
}
.ranking-name {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
}
.ranking-desc {
  font-size: 13px;
  color: #888;
  margin-bottom: 12px;
}
.ranking-count {
  font-size: 12px;
  color: #e94560;
}
</style>
<template>
  <div v-if="ranking">
    <!-- 榜单标题 -->
    <div class="ranking-hero">
      <el-button text @click="$router.back()" style="margin-bottom:12px">
        ← 返回榜单
      </el-button>
      <h1 class="title">🏆 {{ ranking.name }}</h1>
      <p class="desc" v-if="ranking.description">{{ ranking.description }}</p>
    </div>

    <!-- 电影列表 -->
    <div class="movie-list">
      <div
        class="movie-row"
        v-for="(movie, index) in ranking.movies"
        :key="movie.id"
        @click="$router.push(`/movies/${movie.id}`)"
      >
        <!-- 排名 -->
        <div class="rank-badge" :class="rankClass(index)">
          {{ index + 1 }}
        </div>

        <!-- 海报 -->
        <img
          :src="posterUrl(movie.id)"
          class="poster"
          :alt="movie.title"
          @error="handlePosterError"
        />

        <!-- 信息 -->
        <div class="info">
          <h3 class="movie-title">{{ movie.title }}</h3>
          <p class="meta">
            {{ movie.year }}
            <span v-if="movie.directors?.length">· {{ movie.directors[0] }} 导演</span>
            <span v-if="movie.genres?.length">· {{ movie.genres.slice(0,2).join(' / ') }}</span>
          </p>
          <p class="summary-short">{{ movie.summary?.slice(0, 100) }}...</p>
        </div>

        <!-- 评分 -->
        <div class="rating-col">
          <span class="score">{{ movie.rating || '-' }}</span>
          <span class="score-label">豆瓣评分</span>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading-wrap">
    <el-skeleton :rows="6" animated />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getRanking } from '@/api/rankings'
import { posterUrl, handlePosterError } from '@/api/poster'

const route   = useRoute()
const ranking = ref(null)

const rankClass = (index) => {
  if (index === 0) return 'gold'
  if (index === 1) return 'silver'
  if (index === 2) return 'bronze'
  return ''
}

onMounted(async () => {
  ranking.value = await getRanking(route.params.id)
})
</script>

<style scoped>
.ranking-hero {
  background: white;
  border-radius: 12px;
  padding: 28px 32px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.title { font-size: 26px; font-weight: 800; margin-bottom: 8px; }
.desc  { color: #888; font-size: 15px; }

.movie-list { display: flex; flex-direction: column; gap: 12px; }

.movie-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  border-radius: 10px;
  padding: 16px 20px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  transition: transform 0.15s;
}
.movie-row:hover { transform: translateX(4px); }

/* 排名徽章 */
.rank-badge {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 16px;
  background: #eee;
  color: #888;
  min-width: 36px;
}
.rank-badge.gold   { background: #ffd700; color: #8B6914; }
.rank-badge.silver { background: #C0C0C0; color: #555; }
.rank-badge.bronze { background: #CD7F32; color: white; }

.poster {
  width: 64px;
  height: 88px;
  object-fit: cover;
  border-radius: 6px;
  min-width: 64px;
}

.info          { flex: 1; }
.movie-title   { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.meta          { font-size: 13px; color: #999; margin-bottom: 6px; }
.summary-short { font-size: 13px; color: #777; line-height: 1.5; }

.rating-col   { text-align: center; min-width: 64px; }
.score        { display: block; font-size: 24px; font-weight: 800; color: #e94560; }
.score-label  { font-size: 11px; color: #aaa; }

.loading-wrap { padding: 40px; }
</style>
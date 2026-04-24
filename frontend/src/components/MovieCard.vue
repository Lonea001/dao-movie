<template>
  <div class="movie-card" @click="$router.push(`/movies/${movie.id}`)">
    <!-- 海报 -->
    <div class="poster-wrap">
      <img
        :src=" posterUrl(movie.id) || fallback"
        :alt="movie.title"
        class="poster"
        @error="handlePosterError"
      />
      <!-- 评分角标 -->
      <span class="rating-badge" v-if="movie.rating">
        ⭐ {{ movie.rating }}
      </span>
    </div>

    <!-- 信息 -->
    <div class="info">
      <p class="title" :title="movie.title">{{ movie.title }}</p>
      <p class="meta">{{ movie.year }} · {{ movie.genres?.slice(0,2).join(' / ') }}</p>
    </div>
  </div>
</template>

<script setup>
import { posterUrl, handlePosterError } from '@/api/poster'

defineProps({
  movie: { type: Object, required: true }
})
</script>

<style scoped>
.movie-card {
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}
.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.poster-wrap {
  position: relative;
  width: 100%;
  padding-top: 140%; /* 2:3 比例 */
  overflow: hidden;
  background: #eee;
}
.poster {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.movie-card:hover .poster {
  transform: scale(1.05);
}

.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0,0,0,0.65);
  color: #ffd700;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.info {
  padding: 10px 10px 12px;
}
.title {
  font-size: 14px;
  font-weight: 600;
  color: #222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}
.meta {
  font-size: 12px;
  color: #999;
}
</style>
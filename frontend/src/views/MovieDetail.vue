<template>
  <div v-if="movie" class="detail-page">
    <!-- 顶部主信息区 -->
    <div class="hero">
      <img
        :src="posterUrl(movie.id)"
        class="poster"
        :alt="movie.title"
        @error="handlePosterError"
      />
      <div class="hero-info">
        <h1 class="title">{{ movie.title }}</h1>

        <div class="tags">
          <el-tag v-for="g in movie.genres" :key="g" class="tag">{{ g }}</el-tag>
        </div>

        <div class="meta-grid">
          <div class="meta-item" v-if="movie.year">
            <span class="label">年份</span>
            <span>{{ movie.year }}</span>
          </div>
          <div class="meta-item" v-if="movie.duration">
            <span class="label">片长</span>
            <span>{{ movie.duration }} 分钟</span>
          </div>
          <div class="meta-item" v-if="movie.countries?.length">
            <span class="label">地区</span>
            <span>{{ movie.countries.join(' / ') }}</span>
          </div>
          <div class="meta-item" v-if="movie.languages?.length">
            <span class="label">语言</span>
            <span>{{ movie.languages.join(' / ') }}</span>
          </div>
          <div class="meta-item" v-if="movie.directors?.length">
            <span class="label">导演</span>
            <span>{{ movie.directors.join(' / ') }}</span>
          </div>
          <div class="meta-item" v-if="movie.imdb">
            <span class="label">IMDb</span>
            <span>{{ movie.imdb }}</span>
          </div>
        </div>

        <!-- 评分 -->
        <div class="rating-block">
          <span class="score">{{ movie.rating || '暂无' }}</span>
          <div>
            <el-rate
              :model-value="movie.rating / 2"
              disabled
              allow-half
              style="display:inline-flex"
            />
            <p class="rating-count">{{ movie.rating_count?.toLocaleString() }} 人评价</p>
          </div>
        </div>

        <!-- 点赞收藏按钮 -->
        <div class="actions">
          <el-button
            :type="liked ? 'danger' : 'default'"
            :icon="liked ? 'StarFilled' : 'Star'"
            round
            @click="handleLike"
          >
            {{ liked ? '已点赞' : '点赞' }} · {{ likeCount }}
          </el-button>
          <el-button
            :type="collected ? 'warning' : 'default'"
            :icon="collected ? 'CollectionTag' : 'Collection'"
            round
            @click="handleCollect"
          >
            {{ collected ? '已收藏' : '收藏' }} · {{ collectCount }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主演 -->
    <div class="section" v-if="movie.casts?.length">
      <h3 class="section-title">主演</h3>
      <div class="cast-list">
        <el-tag v-for="c in movie.casts" :key="c" type="info" effect="plain">{{ c }}</el-tag>
      </div>
    </div>

    <!-- 剧情简介 -->
    <div class="section" v-if="movie.summary">
      <h3 class="section-title">剧情简介</h3>
      <p class="summary">{{ movie.summary }}</p>
    </div>
  </div>

  <!-- 加载中 -->
  <div v-else class="loading-wrap">
    <el-skeleton :rows="8" animated />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getMovie, likeMovie, collectMovie } from '@/api/movies'
import { ElMessage } from 'element-plus'
import { posterUrl, handlePosterError } from '@/api/poster'

const route   = useRoute()
const movie   = ref(null)


// 点赞/收藏状态（存 localStorage 简单实现）
const liked       = ref(false)
const collected   = ref(false)
const likeCount   = ref(0)
const collectCount= ref(0)

const storageKey = (type) => `movie_${type}_${route.params.id}`

const handleLike = async () => {
  const res  = await likeMovie(route.params.id)
  liked.value      = res.status === 'added'
  likeCount.value  = res.count
  localStorage.setItem(storageKey('like'), liked.value ? '1' : '')
  ElMessage.success(liked.value ? '点赞成功' : '已取消点赞')
}

const handleCollect = async () => {
  const res   = await collectMovie(route.params.id)
  collected.value   = res.status === 'added'
  collectCount.value= res.count
  localStorage.setItem(storageKey('collect'), collected.value ? '1' : '')
  ElMessage.success(collected.value ? '收藏成功' : '已取消收藏')
}

onMounted(async () => {
  movie.value       = await getMovie(route.params.id)
  likeCount.value   = movie.value.like_count    || 0
  collectCount.value= movie.value.collect_count || 0
  // 恢复本地状态
  liked.value     = !!localStorage.getItem(storageKey('like'))
  collected.value = !!localStorage.getItem(storageKey('collect'))
})
</script>

<style scoped>
.detail-page { max-width: 900px; margin: 0 auto; }

/* Hero 区 */
.hero {
  display: flex;
  gap: 36px;
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  margin-bottom: 24px;
}
.poster {
  width: 200px;
  min-width: 200px;
  height: 280px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
.hero-info { flex: 1; }

.title {
  font-size: 26px;
  font-weight: 800;
  margin-bottom: 12px;
  line-height: 1.3;
}

.tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
.tag  { font-size: 13px; }

.meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 24px;
  margin-bottom: 20px;
}
.meta-item { font-size: 14px; color: #555; }
.label     { color: #999; margin-right: 6px; }

/* 评分 */
.rating-block {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}
.score {
  font-size: 48px;
  font-weight: 800;
  color: #e94560;
  line-height: 1;
}
.rating-count { font-size: 12px; color: #999; margin-top: 4px; }

/* 操作按钮 */
.actions { display: flex; gap: 12px; }

/* 信息区块 */
.section {
  background: white;
  border-radius: 12px;
  padding: 24px 28px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: 16px;
}
.section-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e94560;
  display: inline-block;
}
.cast-list { display: flex; flex-wrap: wrap; gap: 8px; }
.summary   { line-height: 1.9; color: #555; font-size: 15px; }

.loading-wrap { padding: 40px; }
</style>
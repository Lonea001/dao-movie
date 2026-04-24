<template>
  <div>
    <h2 class="page-title">🎬 全部电影</h2>

    <!-- 搜索 + 筛选 -->
    <div class="filter-bar">
      <el-input
        v-model="params.q"
        placeholder="搜索片名、导演、演员..."
        clearable
        @keyup.enter="search"
        @clear="search"
        style="width: 280px"
      />

      <div class="genre-tags">
        <el-tag
          :type="params.genre === '' ? '' : 'info'"
          :effect="params.genre === '' ? 'dark' : 'plain'"
          class="genre-tag"
          @click="selectGenre('')"
        >全部</el-tag>
        <el-tag
          v-for="g in genres"
          :key="g"
          :type="params.genre === g ? '' : 'info'"
          :effect="params.genre === g ? 'dark' : 'plain'"
          class="genre-tag"
          @click="selectGenre(g)"
        >{{ g }}</el-tag>
      </div>

      <el-select v-model="params.sort_by" style="width: 140px" @change="search">
        <el-option label="按评分排序" value="rating" />
        <el-option label="按年份排序" value="year" />
        <el-option label="按评价人数" value="rating_count" />
      </el-select>
    </div>

    <!-- 电影网格 -->
    <div class="movie-grid" v-loading="loading">
      <MovieCard v-for="m in movies" :key="m.id" :movie="m" />
    </div>

    <!-- 无结果 -->
    <el-empty v-if="!loading && movies.length === 0" description="没有找到相关电影" />

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="params.page"
        :page-size="params.page_size"
        :total="total"
        layout="prev, pager, next, total"
        @current-change="fetchMovies"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import MovieCard from '@/components/MovieCard.vue'
import { getMovies, getGenres } from '@/api/movies'

const route  = useRoute()
const movies = ref([])
const genres = ref([])
const total  = ref(0)
const loading= ref(false)

const params = reactive({
  page     : 1,
  page_size: 24,
  q        : route.query.q || '',
  genre    : route.query.genre || '',
  sort_by  : 'rating',
})

const fetchMovies = async () => {
  loading.value = true
  const res = await getMovies(params)
  movies.value  = res.items || []
  total.value   = res.total || 0
  loading.value = false
}

const search = () => {
  params.page = 1
  fetchMovies()
}

const selectGenre = (g) => {
  params.genre = g
  params.page  = 1
  fetchMovies()
}

onMounted(async () => {
  const res = await getGenres()
  genres.value = res.genres || []
  fetchMovies()
})

// 监听路由参数变化（从首页搜索跳过来）
watch(() => route.query.q, (q) => {
  if (q !== undefined) {
    params.q    = q
    params.page = 1
    fetchMovies()
  }
})
</script>

<style scoped>
.page-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 20px;
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 24px;
  background: white;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  flex: 1;
}
.genre-tag {
  cursor: pointer;
  user-select: none;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
  min-height: 200px;
}

.pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}
</style>
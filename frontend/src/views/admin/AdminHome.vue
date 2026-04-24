<template>
  <div class="admin-page">
    <!-- 顶栏 -->
    <div class="admin-header">
      <span class="admin-title">🎬 大盗影视 · 后台管理</span>
      <div style="display:flex;gap:12px;align-items:center">
        <router-link to="/" style="color:#aaa;text-decoration:none;font-size:14px">
          前台首页 →
        </router-link>
        <el-button size="small" @click="logout">退出登录</el-button>
      </div>
    </div>

    <div class="admin-body">
      <!-- 榜单管理 -->
      <div class="panel">
        <div class="panel-header">
          <h3>榜单管理</h3>
          <el-button type="primary" @click="openCreateDialog">+ 新建榜单</el-button>
        </div>

        <el-table :data="rankings" v-loading="loading" stripe>
          <el-table-column prop="id"          label="ID"   width="60" />
          <el-table-column prop="name"        label="榜单名" />
          <el-table-column prop="description" label="简介"  show-overflow-tooltip />
          <el-table-column prop="movie_count" label="电影数" width="80" />
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 新建/编辑 榜单弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑榜单' : '新建榜单'"
      width="660px"
      destroy-on-close
      :close-on-press-escape="false"
      
    >
      <el-form :model="form" label-width="80px">
        <el-form-item label="榜单名">
          <el-input v-model="form.name" placeholder="如：2024最佳科幻" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="选择电影">
          <!-- 搜索电影 -->
          <el-input
            v-model="movieSearch"
            placeholder="搜索电影名..."
            @input="searchMovies"
            style="margin-bottom:10px"
          />
          <div class="movie-picker">
            <div class="picker-col">
              <p class="picker-label">搜索结果（点击添加）</p>
              <div class="picker-list">
                <div
                  class="picker-item"
                  v-for="m in searchResults"
                  :key="m.id"
                  @click="addMovie(m)"
                >
                  <span>{{ m.title }}</span>
                  <span class="picker-meta">{{ m.year }} ⭐{{ m.rating }}</span>
                </div>
                <p v-if="!searchResults.length" style="color:#aaa;font-size:13px;padding:8px">
                  {{ movieSearch ? '无结果' : '输入关键词搜索' }}
                </p>
              </div>
            </div>
            <div class="picker-col">
              <p class="picker-label">已选电影（拖动排序）</p>
              <div class="picker-list selected-list">
                <div
                  class="picker-item selected"
                  v-for="(m, i) in form.selectedMovies"
                  :key="m.id"
                >
                  <span class="rank-no">{{ i + 1 }}</span>
                  <span style="flex:1">{{ m.title }}</span>
                  <el-button
                    size="small"
                    circle
                    type="danger"
                    plain
                    @click="removeMovie(i)"
                  >×</el-button>
                </div>
                <p v-if="!form.selectedMovies.length" style="color:#aaa;font-size:13px;padding:8px">
                  从左边添加电影
                </p>
              </div>
            </div>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRankings, createRanking, updateRanking, deleteRanking, getRanking } from '@/api/rankings'
import { getMovies } from '@/api/movies'
import { ElMessage, ElMessageBox } from 'element-plus'

const router   = useRouter()
const rankings = ref([])
const loading  = ref(false)
const saving   = ref(false)

// 弹窗
const dialogVisible = ref(false)
const isEdit        = ref(false)
const editId        = ref(null)

const form = ref({ name: '', description: '', selectedMovies: [] })

// 电影搜索
const movieSearch  = ref('')
const searchResults= ref([])
let searchTimer    = null

const searchMovies = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    if (!movieSearch.value.trim()) { searchResults.value = []; return }
    const res = await getMovies({ q: movieSearch.value, page_size: 20 })
    searchResults.value = res.items || []
  }, 300)
}

const addMovie = (m) => {
  if (form.value.selectedMovies.find(x => x.id === m.id)) {
    ElMessage.warning('已在列表中'); return
  }
  form.value.selectedMovies.push(m)
}
const removeMovie = (i) => form.value.selectedMovies.splice(i, 1)

// 获取榜单列表
const fetchRankings = async () => {
  loading.value  = true
  const res      = await getRankings()
  rankings.value = res.items || []
  loading.value  = false
}

// 打开新建弹窗
const openCreateDialog = () => {
  isEdit.value  = false
  editId.value  = null
  form.value    = { name: '', description: '', selectedMovies: [] }
  movieSearch.value   = ''
  searchResults.value = []
  dialogVisible.value = true
}

// 打开编辑弹窗
const openEditDialog = async (row) => {
  isEdit.value  = true
  editId.value  = row.id
  const detail  = await getRanking(row.id)
  form.value    = {
    name           : detail.name,
    description    : detail.description || '',
    selectedMovies : detail.movies || [],
  }
  movieSearch.value   = ''
  searchResults.value = []
  dialogVisible.value = true
}

// 保存
const handleSave = async () => {
  if (!form.value.name.trim()) { ElMessage.warning('请输入榜单名'); return }
  saving.value = true
  const payload = {
    name      : form.value.name,
    description: form.value.description,
    movie_ids : form.value.selectedMovies.map(m => m.id),
  }
  try {
    if (isEdit.value) {
      await updateRanking(editId.value, payload)
      ElMessage.success('榜单已更新')
    } else {
      await createRanking(payload)
      ElMessage.success('榜单创建成功')
    }
    dialogVisible.value = false
    fetchRankings()
  } finally {
    saving.value = false
  }
}

// 删除
const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除这个榜单吗？', '提示', { type: 'warning' })
  await deleteRanking(id)
  ElMessage.success('已删除')
  fetchRankings()
}

const logout = () => {
  localStorage.removeItem('admin_token')
  router.push('/admin')
}

onMounted(fetchRankings)
</script>

<style scoped>
.admin-page   { min-height: 100vh; background: #f0f2f5; }

.admin-header {
  background: #1a1a2e;
  color: white;
  padding: 0 32px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.admin-title { font-size: 18px; font-weight: 700; color: #e94560; }

.admin-body { padding: 24px 32px; }

.panel {
  background: white;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.panel-header h3 { font-size: 18px; font-weight: 700; }

/* 电影选择器 */
.movie-picker {
  display: flex;
  gap: 12px;
  width: 100%;
}
.picker-col   { flex: 1; }
.picker-label { font-size: 13px; color: #666; margin-bottom: 6px; }
.picker-list  {
  border: 1px solid #eee;
  border-radius: 8px;
  height: 220px;
  overflow-y: auto;
  padding: 4px;
}
.picker-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  gap: 8px;
}
.picker-item:hover  { background: #f5f5f5; }
.picker-item.selected { cursor: default; }
.picker-meta { color: #aaa; font-size: 12px; white-space: nowrap; }
.rank-no     { color: #e94560; font-weight: 700; min-width: 20px; }

.selected-list .picker-item:hover { background: #fff5f5; }
</style>
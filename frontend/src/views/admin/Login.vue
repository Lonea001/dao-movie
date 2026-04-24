<template>
  <div class="login-wrap">
    <div class="login-card">
      <h2 class="login-title">🎬 大盗影视</h2>
      <p class="login-sub">管理员登录</p>

      <el-form :model="form" @submit.prevent="handleLogin" label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="admin" size="large" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="••••••••"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button
          type="primary"
          size="large"
          style="width:100%; margin-top:8px"
          :loading="loading"
          @click="handleLogin"
        >登录</el-button>
      </el-form>

      <p class="back-link">
        <router-link to="/">← 返回前台</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/admin'
import { ElMessage } from 'element-plus'

const router  = useRouter()
const loading = ref(false)
const form    = ref({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    const res = await login(form.value)
    localStorage.setItem('admin_token', res.token)
    ElMessage.success('登录成功')
    router.push('/admin/home')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
}
.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px 36px;
  width: 380px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.login-title {
  font-size: 24px;
  font-weight: 800;
  color: #e94560;
  text-align: center;
  margin-bottom: 4px;
}
.login-sub {
  text-align: center;
  color: #999;
  margin-bottom: 28px;
  font-size: 14px;
}
.back-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}
.back-link a { color: #aaa; text-decoration: none; }
.back-link a:hover { color: #e94560; }
</style>
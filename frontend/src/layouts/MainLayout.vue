<template>
  <div class="layout">
    <!-- 顶部导航栏 -->
    <header class="navbar">
      <div class="navbar-inner">
        <router-link to="/" class="logo">🎬 大盗影视</router-link>
        <nav class="nav-links">
          <router-link to="/">首页</router-link>
          <router-link to="/movies">电影</router-link>
          <router-link to="/rankings">榜单</router-link>
        </nav>
        <router-link to="/admin" class="admin-link">
          <el-icon><Setting /></el-icon> 管理
        </router-link>
      </div>
    </header>

    <!-- 页面内容 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 底部 -->
    <footer class="footer">
      <p>© 2024 大盗影视 · 毕业设计项目</p>
    </footer>
  </div>
</template>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 导航栏 */
.navbar {
  background: #1a1a2e;
  color: white;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  gap: 32px;
}
.logo {
  font-size: 20px;
  font-weight: 700;
  color: #e94560;
  text-decoration: none;
  white-space: nowrap;
}
.nav-links {
  display: flex;
  gap: 24px;
  flex: 1;
}
.nav-links a, .admin-link {
  color: #ccc;
  text-decoration: none;
  font-size: 15px;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}
.nav-links a:hover,
.nav-links a.router-link-active,
.admin-link:hover {
  color: #e94560;
}

/* 内容区 */
.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 24px;
}

/* 底部 */
.footer {
  background: #1a1a2e;
  color: #666;
  text-align: center;
  padding: 16px;
  font-size: 13px;
}
</style>
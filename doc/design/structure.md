<font color='red'>Dao-movie</font>



### 项目结构



│

​	**backend**/			      # Python + FastAPI

​		main.py			# 入口、注册路由、启动配置

​		database.py		# SQLite 连接、Session 管理

​		models.py		   # 数据库表结构

​		schemas.py		# 响应模型



​		routers/			# 功能接口拆分

​			movies.py	    # 分类、详情、列表、搜索、

​			interactions.py

​			admin.py	     # 登录、后台管理

​		data/

​			movies.csv

​			movies.db



​		**import_data.py**	# 初始化数据库

​		requirements.txt



​	**frontend**/			    # Vue3 + Vite

​		src/

​			main.js

​			App.vue

​	

​			api/				# 统一管理请求，前端所有接口调用都从这里走

​				movies.js

​				rankings.js



​			views/				# 页面

​				Home.vue		# 轮播 + 推荐 + 榜单

​				MovieList.vue

​				MovieDetail.vue

​				Rankings.vue

​				

​			

​			components/

​				MovieCard.vue

​				SearchBar.vue

​				Navbar.vue

​			

​			router/

​				index.js



​		index.html

​		vite.config.js

​		package.json



### 系统实现

1. **后端接口**实现

2. **数据库设计**与实现
3. 前端页面实现
4. 分类页面实现
5. 榜单与搜索实现




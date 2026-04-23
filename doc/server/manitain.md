

### 官方管理网站

[云服务器管理控制台](https://ecs.console.aliyun.com/keyPair/region/cn-wulanchabu)



[云服务器管理控制台](https://ecs.console.aliyun.com/server/i-0jl4ij8azd0ta0lvzjsq/detail?regionId=cn-wulanchabu)



[密钥对管理](https://ecs.console.aliyun.com/keyPair/region/cn-wulanchabu)



[欢迎 - Aliyun Workbench](https://ecs-workbench.aliyun.com/?from=ecs&instanceType=ecs&regionId=cn-wulanchabu&instanceId=i-0jl4ij8azd0ta0lvzjsq&resourceGroupId=&language=zh-CN)





![image-20260421025638299](C:\Users\sea\AppData\Roaming\Typora\typora-user-images\image-20260421025638299.png)



### 设置



> 公网 IP
>
> 8.147.71.17



![image-20260421030244781](D:\sea\Desktop\ZJBTI\毕业设计\Dao-movie\doc\image-20260421030244781.png)





### 安全

开放端口：

> 22	SSH
>
> 80	HTTP
>
> 443	HTTPS



重置密码



#### 远程连接

1. 公网 IP
2. 登录用户名
3. 登陆方式



![image-20260421031956205](C:\Users\sea\AppData\Roaming\Typora\typora-user-images\image-20260421031956205.png)



使用pem

```
ssh -i ~/.ssh/your-key.pem ubuntu@ip
```





为nginx 开放阿里云 80 443 安全组




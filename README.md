# 记忆卡片

[![image](https://badgen.net/badge/license/GPL-3.0/green)](https://github.com/lczmx/MemoryCard/blob/main/LICENSE)
## 简介
记忆卡片使用 [FastAPI](https://github.com/tiangolo/fastapi) 作为后端, [vue3](https://github.com/youzan/vant) 作为前端, 是一个用于科学复习记忆的工具。  
记忆卡片默认有科学的复习计划，并且可以让用户自定制最适合自己的记忆曲线。提供HTML5端，无需下载APP，可以随时随地进行记忆/复习。
## 线上 DEMO
扫描二维码访问demo:  
![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/QRcode.png)


- 用户名: `lczmx@foxmail.com`
- 密码: `lczmx@foxmail.com`


## 项目截图

![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/review-page.png)
![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/review-page-category-filter.png)
![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/review-mode.png)
![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/card-page.png)
![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/category-page.png)
![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/settings-page.png)
![](https://raw.githubusercontent.com/lczmx/MemoryCard/main/static/images/analyse-review.png)



## 快速开始
### 安装Docker和Docker Compose
使用国内源安装`Docker`:  
```bash
curl -sSL https://get.daocloud.io/docker | sh
```
> 适用于Ubuntu，Debian,Centos等大部分Linux，会3小时同步一次Docker官方资源  

使用国内源安装`docker-compose`:  
```bash
curl -L https://get.daocloud.io/docker/compose/releases/download/v2.3.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
> 你可以通过修改URL中的版本，可以自定义您的需要的版本  

### 部署到服务器
假如你的服务器已经安装了Docker和docker-compose, 就可以将本项目部署到服务器了 
```bash
# 下载并解压
wget --no-check-certificate --content-disposition -P /opt -c https://github.com/lczmx/MemoryCard/releases/download/v0.2.1/memorycard-0.2.1.tar.gz&&tar -zxvf /opt/memorycard-0.2.1.tar.gz -C /opt 
# cd到项目文件夹
cd /opt/MemoryCard
# 启动项目
docker-compose up -d
```
## Q&A
1. 部署后无法访问?
   - 假如是本地环境, 确认防火墙是否开放端口
     ```base
     firewall-cmd --permanent --add-port=58800/tcp
     firewall-cmd --permanent --add-port=8366/tcp
    
     firewall-cmd --reload
     ```
   - 假如是云服务器, 需要登录服务商的设置面板, 开放`58800/tcp`和`8366/tcp`这两个端口  
    具体操作自行搜索
2. 如何修改端口?  
   默认前端项目绑定`58800`端口, 假如需要修改端口, 只需要修改`docker-compose.yml`文件的nginx服务即可, 比如修改为`80`和`443`端口:
   ```yaml
   nginx:
     build: ./compose/nginx
       ports:
         - 80:80
         - 443:443
   ```
3. 如何修改nginx和mysql配置?  
   mysql配置位于: `MemoryCard/compose/mysql/conf/my.cnf`, 配置详解见: [MySQL5.7配置文件详细说明](https://developer.aliyun.com/article/838873)  
   nginx配置位于: `MemoryCard/compose/nginx/nginx.conf`, 配置详解见: [nginx配置文件](https://www.cnblogs.com/lczmx/p/14978241.html#%E4%BA%86%E8%A7%A3%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)  
   修改后需要执行: `docker-compose up --build`, 重新构建容器
## commit规范
假如想贡献自己的代码, 请按以下规范提交自己的`request`

- `feat`: 新增 feature
- `fix`: 修复 bug
- `docs`: 仅仅修改了文档，比如 README, CHANGELOG, CONTRIBUTE等等
- `style`: 仅仅修改了空格、格式缩进、逗号等等，不改变代码逻辑
- `refactor`: 代码重构，没有加新功能或者修复 bug
- `perf`: 优化相关，比如提升性能、体验
- `test`: 测试用例，包括单元测试、集成测试等
- `chore`: 改变构建流程、或者增加依赖库、工具等
- `revert`: 回滚到上一个版本

## 许可
本项目遵循 [GPL-3.0](https://github.com/lczmx/MemoryCard/blob/main/LICENSE) 开源许可。
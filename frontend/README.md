# 记忆卡片前端 (Memory Card)

一款基于 Vue 3 + Vite 的记忆卡片应用前端，支持卡片管理、分类组织、学习计划制定和复习回顾功能。

## 项目介绍

记忆卡片是一款帮助用户高效学习和复习知识的应用。通过创建卡片、管理分类、制定复习曲线，系统会根据艾宾浩斯遗忘曲线自动安排复习时间，帮助用户科学地记忆知识。

**主要功能：**
- 卡片管理：创建、编辑、删除学习卡片
- 分类组织：将卡片按类别分组管理
- 复习曲线：自定义复习间隔，科学规划学习
- 复习回顾：拖拽交互完成卡片复习
- 数据分析：查看学习进度和统计

## 技术栈

| 分类 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue 3 | ^3.5.27 |
| 构建工具 | Vite | ^5.4.10 |
| UI 组件库 | Vant | ^4.9.22 |
| 路由 | Vue Router | ^4.6.4 |
| 状态管理 | Vuex | ^4.1.0 |
| 富文本编辑 | Tiptap | ^3.16.0 |
| HTTP 客户端 | Axios | ^1.13.2 |
| 类型检查 | TypeScript | ~5.9.3 |
| 代码规范 | ESLint | ^9.39.2 |
| 样式预处理器 | Sass | ^1.97.3 |

## 环境要求

- **Node.js**: >= 18.0.0
- **pnpm**: >= 8.0.0 (推荐) 或 npm/yarn

## 安装步骤

```bash
# 克隆项目
git clone <repository-url>
cd frontend

# 安装依赖
pnpm install
```

## 开发模式启动

```bash
pnpm serve
```

项目将在 `http://localhost:5173` 启动，支持热模块替换（HMR）。

## 生产构建

```bash
# 构建生产版本
pnpm build

# 预览生产构建
pnpm preview
```

构建产物将输出到 `dist` 目录。

## 代码规范

项目使用 ESLint 进行代码检查和格式化：

```bash
# 检查并自动修复
pnpm lint
```

**规范要点：**
- Vue 组件使用 `<script setup>` 语法
- 使用 TypeScript 进行类型检查
- CSS 优先使用 SCSS 预处理器
- 组件文件使用 PascalCase 命名（如 `CardEditor.vue`）
- 工具函数使用 camelCase 命名（如 `request.ts`）

## 目录结构

```
frontend/
├── public/                 # 静态公共资源
├── src/
│   ├── assets/            # 项目资源（图片、字体、数据）
│   │   ├── css/
│   │   ├── data/
│   │   ├── font_*/        # 图标字体
│   │   └── images/
│   ├── components/        # 公共组件
│   │   ├── AddPlan.vue
│   │   ├── Analyse.vue
│   │   ├── cardEditor.vue
│   │   ├── cards.vue
│   │   ├── category.vue
│   │   ├── ColorPicker.vue
│   │   ├── IconPicker.vue
│   │   ├── review.vue
│   │   └── ...
│   ├── hook/              # 组合式函数
│   ├── router/            # 路由配置
│   ├── store/             # Vuex 状态管理
│   ├── types/             # TypeScript 类型定义
│   ├── utils/             # 工具函数
│   │   ├── request.ts     # HTTP 请求封装
│   │   └── assets.ts
│   ├── views/             # 页面视图
│   ├── App.vue            # 根组件
│   └── main.ts            # 入口文件
├── .eslintrc.js          # ESLint 配置
├── index.html             # HTML 入口
├── package.json
├── tsconfig.json          # TypeScript 配置
└── vite.config.ts         # Vite 配置
```

**目录说明：**

| 目录/文件 | 说明 |
|-----------|------|
| `src/components/` | 可复用的 Vue 组件 |
| `src/views/` | 页面级组件，与路由对应 |
| `src/store/` | Vuex 状态管理模块 |
| `src/utils/request.ts` | 封装了 HTTP 请求方法 |
| `src/types/` | TypeScript 接口类型定义 |
| `src/hook/` | Vue Composition API 组合式函数 |

## API 接口配置

前端通过 `Vuex store` 中的 `serverHost` 配置后端接口地址。

**配置位置：** `src/store/index.ts`

```typescript
state: {
  serverHost: 'http://localhost:8366',  // 修改为你的后端地址
  // ...
}
```

**接口规范：**
- 使用 RESTful API 设计
- 响应格式：

```json
{
  "status": 1,
  "msg": "操作成功",
  "data": {
    "items": [],
    "meta": {
      "total": 100,
      "limit": 10,
      "offset": 0,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

**主要接口：**

| 模块 | 接口路径 | 说明 |
|------|----------|------|
| 卡片 | `/cards` | 卡片 CRUD |
| 类别 | `/category` | 类别管理 |
| 复习 | `/review` | 复习记录 |
| 曲线 | `/plans` | 复习曲线 |
| 认证 | `/auth` | 登录注册 |

## 环境变量

如需在不同环境使用不同的后端地址，可在 `vite.config.ts` 中配置代理或使用环境变量。

## 贡献指南

欢迎提交 Issue 和 Pull Request！

**提交规范：**
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

**代码风格：**
- 遵循 ESLint 配置的代码规范
- 组件 props 使用 TypeScript 类型定义
- 优先使用组合式函数（Composition API）

## 许可证

本项目仅供个人学习使用，未经授权不得用于商业用途。

---

如有问题或建议，欢迎提交 Issue！

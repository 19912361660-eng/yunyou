# 云游智行 - Django 后端

基于 Django + Django REST Framework 的旅游服务系统后端API。

## 技术栈

- **框架**: Django 4.2+, Django REST Framework
- **数据库**: MySQL 8.0+
- **认证**: JWT (djangorestframework-simplejwt)
- **AI**: Google Gemini API
- **文档**: drf-spectacular (OpenAPI 3.0)

## 项目结构

```
yunyou_backend/
├── apps/
│   ├── users/          # 用户管理、认证
│   ├── attractions/    # 景点管理、路线规划
│   ├── orders/         # 订单管理
│   ├── products/       # 积分商城
│   ├── community/      # 社区交流
│   ├── ai_assistant/  # AI智能助手
│   └── backup/         # 数据备份
├── config/             # Django配置
├── media/              # 媒体文件
└── manage.py
```

## 快速开始

### 1. 安装依赖

```bash
cd yunyou_backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 配置数据库和API密钥
```

### 3. 创建数据库

```sql
CREATE DATABASE yunyou_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 运行迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建管理员

```bash
python manage.py createsuperuser
```

### 6. 启动服务

```bash
python manage.py runserver
```

## API文档

启动服务后访问: http://localhost:8000/api/docs/

## API接口一览

### 认证 (/api/users/)
- `POST /api/users/token/` - 获取JWT令牌
- `POST /api/users/token/refresh/` - 刷新令牌
- `POST /api/users/register/` - 用户注册
- `GET /api/users/profile/` - 获取个人资料
- `PUT /api/users/profile/` - 更新个人资料
- `POST /api/users/change-password/` - 修改密码

### 用户管理 (/api/users/management/)
- `GET /api/users/management/` - 用户列表
- `POST /api/users/management/` - 创建用户
- `GET /api/users/management/{id}/` - 用户详情
- `PUT /api/users/management/{id}/` - 更新用户
- `DELETE /api/users/management/{id}/` - 删除用户
- `POST /api/users/management/{id}/toggle_status/` - 切换状态
- `POST /api/users/management/{id}/reset_password/` - 重置密码

### 景点 (/api/attractions/)
- `GET /api/attractions/` - 景点列表
- `POST /api/attractions/` - 创建景点(管理员)
- `GET /api/attractions/{id}/` - 景点详情
- `GET /api/attractions/recommended/` - 推荐景点
- `GET /api/attractions/hot/` - 热门景点
- `GET /api/attractions/search/` - 搜索景点
- `POST /api/attractions/{id}/like/` - 点赞景点

### 路线 (/api/attractions/routes/)
- `GET /api/attractions/routes/` - 路线列表
- `POST /api/attractions/routes/` - 创建路线
- `GET /api/attractions/routes/{id}/` - 路线详情
- `POST /api/attractions/routes/{id}/share/` - 分享路线
- `GET /api/attractions/routes/public_routes/` - 公开路线

### 订单 (/api/orders/)
- `GET /api/orders/` - 订单列表
- `POST /api/orders/` - 创建订单
- `GET /api/orders/{id}/` - 订单详情
- `POST /api/orders/{id}/pay/` - 支付订单
- `POST /api/orders/{id}/cancel/` - 取消订单

### 商品 (/api/products/)
- `GET /api/products/` - 商品列表
- `GET /api/products/featured/` - 精选商品
- `GET /api/products/{id}/` - 商品详情
- `GET /api/products/categories/` - 商品分类
- `POST /api/products/exchanges/` - 兑换商品

### 社区 (/api/community/)
- `GET /api/community/posts/` - 帖子列表
- `POST /api/community/posts/` - 发布帖子
- `GET /api/community/posts/{id}/` - 帖子详情
- `POST /api/community/posts/{id}/like/` - 点赞
- `POST /api/community/comments/` - 发表评论

### AI助手 (/api/ai/)
- `POST /api/ai/sessions/send_message/` - 发送消息
- `GET /api/ai/sessions/` - 会话列表
- `GET /api/ai/sessions/{id}/messages/` - 历史消息

### 数据备份 (/api/backup/)
- `GET /api/backup/backups/` - 备份列表
- `POST /api/backup/backups/` - 创建备份
- `GET /api/backup/backups/{id}/download/` - 下载备份
- `POST /api/backup/restores/` - 恢复数据
- `GET /api/backup/stats/` - 数据统计

## 数据模型

### User (用户)
- id, username, email, phone, avatar
- role (admin/user), status (active/disabled)
- points (积分), bio, preferences

### Attraction (景点)
- id, name, location, description
- rating, price, tags, images
- latitude/longitude (地图坐标)
- is_recommended, is_hot

### Route (路线)
- id, title, user, start_date/end_date
- days (路线日程), attractions (包含景点)

### Order (订单)
- id, order_no, user, status
- total_amount, final_amount
- items (订单项)

### Product (商品)
- id, name, points (所需积分)
- stock, sold_count

### Post (帖子)
- id, user, title, content
- post_type (share/question/guide)
- like_count, comment_count

## 权限管理

| 角色 | 普通用户 | 管理员 |
|------|---------|--------|
| 查看景点/商品 | ✓ | ✓ |
| 发布内容 | ✓ | ✓ |
| 管理自己的订单 | ✓ | ✓ |
| 管理员面板 | ✗ | ✓ |
| 管理所有用户 | ✗ | ✓ |
| 景点/商品CRUD | ✗ | ✓ |
| 数据备份 | ✗ | ✓ |

## 前端对接

前端需要配置JWT认证:

```typescript
const API_BASE = 'http://localhost:8000/api';

// 登录获取token
const response = await fetch(`${API_BASE}/users/token/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});
const { access, refresh } = await response.json();

// 请求时添加Header
headers: {
  'Authorization': `Bearer ${access}`
}
```

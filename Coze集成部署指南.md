# 🎬 Streamlit + Coze API 集成部署指南

## 🎯 快速开始

**你的目标**：让Streamlit应用调用Coze API生成真实文案

**预计时间**：5分钟

---

## 📋 部署流程

### 第1步：准备文件

确保你有以下文件：
```
streamlit_app/
├── app_with_coze.py          # 集成Coze API的主应用（替代app.py）
├── requirements.txt          # 依赖包
├── .streamlit/
│   └── config.toml          # Streamlit配置
└── .env.example             # 环境变量示例
```

**重要**：使用 `app_with_coze.py` 作为主文件，而不是 `app.py`

---

### 第2步：上传到GitHub

1. 将 `app_with_coze.py` 重命名为 `app.py`
   - 或者在上传时直接用 `app_with_coze.py` 这个名字

2. 上传所有文件到GitHub仓库

---

### 第3步：配置环境变量（关键！）

#### 在Streamlit Cloud中配置

1. 访问：https://share.streamlit.io/
2. 进入你的应用设置
3. 点击「Advanced settings」或「Settings」
4. 找到「Secrets」或「Environment Variables」
5. 添加环境变量：

**COZE_API_KEY**（必需）
```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwMjFiZTE3LTM4MDMtNDEwOS1hODkxLTZlOTNmZTAwOTA0ZiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkNnN2Y5QVFyRk9YWFAyaHJVc0V3eFd6Sld3TGMyNE9pIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc1MTE5MTIxLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjIyNjAzNzA1MzMzODQxOTQ2Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjI0MDc4NTc0Mzc4NTQ5Mjg4In0.moCw4YIUgrgdd3Ic2XtS4B-zISqKXffdfNQO_2Z_gtCviwjXh2gaGvwrepe1dMWbGBi8OhYjloSEBlrMR3XWfvoC5PzMf4vlAk2puU0T-pFxhPa3zhYZI4XoIy6LiMwV5Z0ewX2Gamn_8wDjbmbD546aC3lVHmuDOmrWODuDyor6CPIwCL3h_fG6LuS4KeqTckq6k2UixawhmyzpGIlN3p1WFdhVpIU3M6ZTd-MH-G1qmJkClS9u-blyFAXH8eGK8Du4xMHIo2jynNlbCd-C3KaBfPNoONyuK8Ddtp_HbQ8e_GFiQMOk2md-Vy_gnyNI01f5JZwQnqPfxtsjjcjPlA
```

**COZE_BOT_ID**（可选）
```
你的Bot ID（如果有）
```

6. 保存设置

#### 在Vercel中配置

1. 打开Vercel项目
2. 点击「Settings」→「Environment Variables」
3. 添加上述环境变量
4. 重新部署

---

### 第4步：修改入口文件

#### 方法A：重命名文件（推荐）

在GitHub中：
1. 将 `app_with_coze.py` 重命名为 `app.py`
2. 提交更改
3. 重新部署

#### 方法B：使用app_with_coze.py作为入口

在Streamlit Cloud中：
1. 应用设置中，将入口文件改为 `app_with_coze.py`
2. 保存并重新部署

---

### 第5步：部署完成

1. 等待部署完成（1-2分钟）
2. 访问应用链接
3. 上传视频测试

---

## 🧪 测试应用

### 测试步骤

1. **打开应用**
   - 在浏览器访问应用链接

2. **上传视频**
   - 点击上传按钮
   - 选择一个视频文件

3. **生成文案**
   - 点击「生成文案」按钮
   - 等待AI分析

4. **查看结果**
   - 查看生成的文案
   - 应该和Coze中的效果一致

### 预期效果

生成的文案应该：
- ✅ 和你在Coze中使用的效果一致
- ✅ 包含智能分析的内容
- ✅ 符合你的要求（如果输入了提示）

---

## 🔧 故障排查

### 问题1：显示"未配置Coze API Key"

**原因**：环境变量未配置

**解决**：
1. 检查环境变量是否已添加
2. 确认变量名是 `COZE_API_KEY`（全大写）
3. 确认API Key值完整（不要有空格或换行）
4. 重新部署应用

---

### 问题2：API调用失败

**可能原因**：
- API Key过期
- API Key格式错误
- 网络问题

**解决**：
1. 确认API Key是否过期
2. 检查API Key是否完整复制
3. 查看应用日志，查看具体错误信息
4. 重新获取API Key

---

### 问题3：生成的内容和Coze不一致

**可能原因**：
- 调用的是不同的Bot
- 提示词不同
- 模型参数不同

**解决**：
1. 确认调用的是同一个Coze智能体
2. 对比Streamlit和Coze中的输入
3. 如果需要，添加 `COZE_BOT_ID` 环境变量

---

### 问题4：响应很慢

**可能原因**：
- 视频文件太大
- Coze API响应慢
- 网络问题

**解决**：
1. 使用较小的视频文件测试
2. 检查网络连接
3. 优化提示词，减少复杂度

---

## 📊 API调用说明

### 使用的API接口

当前代码支持两种调用方式：

#### 方式1：使用Bot ID（如果有）
```python
api_url = "https://api.coze.cn/open_api/v2/chat"
data = {
    "bot_id": COZE_BOT_ID,
    "query": user_message
}
```

#### 方式2：使用Workload Identity（默认）
```python
api_url = "https://api.coze.cn/open_api/v2/workflow/run"
data = {
    "query": user_message,
    "user": "streamlit_user"
}
```

**你的Token**使用的是Workload Identity方式，所以会自动使用方式2。

---

## 💡 优化建议

### 1. 添加视频AI分析

当前版本主要基于文件信息生成文案。如需分析视频内容，可以集成：

- OpenAI Vision API
- 阿里云视频AI
- 腾讯云视频AI

### 2. 优化提示词

在 `call_coze_api` 函数中优化提示词，让文案更符合你的需求。

### 3. 添加缓存

避免重复调用API，节省成本。

### 4. 添加更多功能

- 文案历史记录
- 多版本对比
- 一键发布到社交媒体

---

## 📝 环境变量配置示例

### .env文件（本地测试）
```bash
COZE_API_KEY=你的API_Key
COZE_BOT_ID=你的Bot_ID_可选
```

### Streamlit Cloud Secrets
```
[app]
COZE_API_KEY = "你的API_Key"
COZE_BOT_ID = "你的Bot_ID"
```

### Vercel Environment Variables
```
COZE_API_KEY = 你的API_Key
COZE_BOT_ID = 你的Bot_ID
```

---

## 🎉 完成！

配置完成后，你的Streamlit应用就能：

✅ 调用真实的Coze API
✅ 生成和Coze一致的文案
✅ 在手机上使用
✅ 自动适配屏幕

---

## 📞 需要帮助？

如果遇到问题：
1. 检查环境变量配置
2. 查看应用日志
3. 确认API Key是否有效
4. 参考Coze API文档

---

**祝你部署成功！** 🚀

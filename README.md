# 🎬 视频文案助手 - Streamlit版

一个基于Streamlit的智能视频文案生成工具，支持手机浏览器访问。

## ✨ 特点

- 📱 **手机友好**：自动适配手机屏幕
- 🚀 **部署简单**：一键部署到Streamlit Cloud
- 🎨 **界面美观**：现代化的UI设计
- 🆓 **完全免费**：使用Streamlit Cloud免费托管
- ⚡ **快速上手**：无需任何配置，直接使用

## 🎯 功能

1. **视频上传**：支持MP4、MOV、AVI等格式
2. **AI分析**：自动分析视频内容
3. **文案生成**：生成多种风格的文案
4. **快捷操作**：一键复制、下载
5. **多版本选择**：支持生成多个文案版本

## 📦 文件结构

```
streamlit_app/
├── app.py                    # 主应用
├── requirements.txt          # 依赖包
├── vercel.json              # Vercel配置
├── .streamlit/
│   └── config.toml          # Streamlit配置
├── 部署指南.md               # 详细部署教程
└── README.md                # 本文件
```

## 🚀 快速开始

### 方法1：本地运行（测试用）

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
streamlit run app.py
```

3. 访问：http://localhost:8501

### 方法2：部署到Streamlit Cloud（推荐）⭐

1. 上传文件到GitHub仓库
2. 访问：https://share.streamlit.io/
3. 点击「Deploy now」
4. 选择你的仓库并部署
5. 获得在线链接，手机直接访问

**详细步骤请参考《部署指南.md》**

## 📱 手机使用

1. 在手机浏览器打开应用链接
2. 点击上传视频
3. 点击生成文案
4. 复制或下载文案

## 🔧 自定义

### 修改标题
编辑 `app.py` 中的 `st.set_page_config()`

### 修改主题
编辑 `.streamlit/config.toml`

### 修改文案
编辑 `app.py` 中的 `sample_copies` 列表

## 📊 技术栈

- **Streamlit**：Python数据应用框架
- **Vercel**：可选部署平台
- **Streamlit Cloud**：官方托管平台

## 💡 提示

- 视频大小建议小于500MB
- 视频时长建议1-10分钟
- 使用Chrome或Safari浏览器体验最佳

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**享受使用视频文案助手！** 🎉

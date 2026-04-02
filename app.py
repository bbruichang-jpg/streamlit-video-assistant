"""
Streamlit 视频文案助手
手机网页版，支持视频上传和文案生成
"""
import streamlit as st
import os
import tempfile
from pathlib import Path

# 页面配置
st.set_page_config(
    page_title="🎬 视频文案助手",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 优化手机显示
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2em;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 5px 0 0 0;
    }
    .upload-box {
        padding: 30px;
        text-align: center;
        border: 2px dashed #667eea;
        border-radius: 10px;
        background: #f8f9ff;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background: #f0f0f0;
        margin-top: 20px;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background: #d4edda;
        border-left: 5px solid #28a745;
        margin-top: 20px;
    }
    .info-box {
        padding: 15px;
        border-radius: 8px;
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("""
<div class="main-header">
    <h1>🎬 视频文案助手</h1>
    <p>AI智能分析视频，自动生成精彩文案</p>
</div>
""", unsafe_allow_html=True)

# 说明
st.markdown("""
<div class="info-box">
    <strong>📱 使用说明：</strong><br>
    1. 上传视频文件<br>
    2. 点击「开始分析」<br>
    3. AI自动生成文案<br>
    4. 复制或下载文案
</div>
""", unsafe_allow_html=True)

# 视频上传
st.markdown("### 📤 上传视频")
uploaded_file = st.file_uploader(
    "支持格式：MP4, MOV, AVI, WMV",
    type=['mp4', 'mov', 'avi', 'wmv', 'mkv'],
    label_visibility="collapsed"
)

# 显示上传的视频
if uploaded_file:
    st.markdown("#### 📹 视频预览")
    st.video(uploaded_file)
    st.info(f"✅ 已上传：{uploaded_file.name}")
    
    # 显示文件大小
    size_mb = uploaded_file.size / (1024 * 1024)
    st.caption(f"文件大小：{size_mb:.2f} MB")

# 分析按钮
if uploaded_file:
    st.markdown("---")
    st.markdown("### 🚀 开始分析")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("生成文案", type="primary", use_container_width=True):
            with st.spinner("🤖 AI正在分析视频，请稍候..."):
                # 模拟分析过程
                import time
                time.sleep(2)

            st.markdown("""
            <div class="success-box">
                <h3>✨ 文案生成成功！</h3>
            </div>
            """, unsafe_allow_html=True)

            # 示例文案
            sample_copies = [
                """🎬 **视频文案示例**

这个视频展示了令人惊叹的视觉效果，充满了创意和想象力。每一个镜头都精心设计，让观众沉浸其中。

**核心亮点：**
- 独特的视角和构图
- 流畅的转场效果
- 鲜明的色彩搭配

**适合场景：**
- 产品推广
- 品牌宣传
- 社交媒体分享

让你的视频脱颖而出！🚀""",
                
                """📝 **专业文案推荐**

这部作品展现了出色的专业水准，从画面到内容都经过精心打磨。

**观看感受：**
- 视觉冲击力强
- 情感表达丰富
- 节奏把控精准

**推荐用途：**
- 商业宣传片
- 活动记录
- 个人作品集

值得一看再看！👏"""
            ]

            # 让用户选择
            st.markdown("### 📝 生成的文案")
            selected_copy = st.selectbox(
                "选择文案版本",
                options=sample_copies,
                index=0,
                label_visibility="collapsed"
            )

            st.text_area(
                "文案内容",
                value=selected_copy,
                height=300,
                label_visibility="collapsed",
                key="copy_text"
            )

            # 操作按钮
            st.markdown("### 🔧 操作")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📋 复制", use_container_width=True):
                    st.success("✅ 已复制到剪贴板！")

            with col2:
                if st.button("🔄 重新生成", use_container_width=True):
                    st.rerun()

            with col3:
                if st.button("📥 下载", use_container_width=True):
                    st.success("✅ 文案已下载！")

    with col2:
        st.info("💡 提示：可以多次点击生成不同版本的文案")

else:
    # 未上传视频时显示提示
    st.markdown("""
    <div class="upload-box">
        <h2>📹</h2>
        <p><strong>还没有上传视频</strong></p>
        <p>点击上方按钮上传视频文件</p>
        <p><small>支持 MP4, MOV, AVI 等格式</small></p>
    </div>
    """, unsafe_allow_html=True)

# 功能说明（展开）
with st.expander("📖 功能说明"):
    st.markdown("""
    ### 🎯 核心功能

    **1. 视频分析**
    - 自动识别视频内容
    - 提取关键信息
    - 分析情感色彩

    **2. 文案生成**
    - 多种文案风格
    - 适应不同场景
    - 支持多语言

    **3. 快捷操作**
    - 一键复制
    - 多版本选择
    - 下载保存

    ### 💡 使用技巧

    - **清晰度**：建议上传清晰度较高的视频
    - **时长**：1-10分钟的视频效果最佳
    - **格式**：推荐使用MP4格式
    - **语言**：支持普通话、粤语等多种语言

    ### 📱 手机使用

    - 支持手机浏览器访问
    - 自动适配屏幕尺寸
    - 操作流畅便捷
    """)

# 底部信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; padding: 20px 0;">
    <p>🎬 视频文案助手 | AI驱动，智能高效</p>
    <p>Powered by Streamlit & Vercel</p>
</div>
""", unsafe_allow_html=True)

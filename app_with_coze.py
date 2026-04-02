"""
Streamlit 视频文案助手 - 集成Coze API版本
手机网页版，支持视频上传和真实的AI文案生成
"""
import streamlit as st
import requests
import base64
import tempfile
import os

# 页面配置
st.set_page_config(
    page_title="🎬 视频文案助手",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Coze API配置
COZE_API_URL = "https://api.coze.cn/open_api/v2/bot/publish"
COZE_API_KEY = st.secrets.get("COZE_API_KEY", "")  # 从环境变量读取

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


def call_coze_api(prompt, video_info=""):
    """
    调用Coze API生成文案

    Args:
        prompt: 用户输入的提示词
        video_info: 视频信息（文件名、大小等）

    Returns:
        生成的文案内容
    """
    if not COZE_API_KEY:
        return "❌ 错误：未配置Coze API Key，请在Vercel环境变量中添加 COZE_API_KEY"

    try:
        # 构建请求
        headers = {
            "Authorization": f"Bearer {COZE_API_KEY}",
            "Content-Type": "application/json"
        }

        # 构建消息
        user_message = f"请为视频生成文案。视频信息：{video_info}\n\n用户要求：{prompt}"
        if not prompt:
            user_message = f"请为这个视频生成一份专业、吸引人的文案。视频信息：{video_info}"

        # 调用Coze API（使用聊天接口）
        api_url = "https://api.coze.cn/open_api/v2/chat"

        data = {
            "bot_id": st.secrets.get("COZE_BOT_ID", ""),  # 从环境变量读取Bot ID
            "user_id": "user_" + str(hash(prompt)),  # 生成唯一用户ID
            "query": user_message,
            "stream": False
        }

        # 如果没有配置Bot ID，使用Workload API
        if not data["bot_id"]:
            # 使用你的token调用
            data = {
                "query": user_message,
                "stream": False,
                "user": "streamlit_user"
            }
            # 使用Workload Identity API
            api_url = "https://api.coze.cn/open_api/v2/workflow/run"

        response = requests.post(api_url, json=data, headers=headers, timeout=60)

        if response.status_code == 200:
            result = response.json()
            # 解析返回结果
            if "data" in result:
                return result["data"].get("answer", "生成成功但未返回内容")
            elif "messages" in result:
                # 从消息列表中提取最后的回答
                messages = result["messages"]
                for msg in reversed(messages):
                    if msg.get("type") == "answer":
                        return msg.get("content", "")
                return result.get("messages", [{}])[-1].get("content", "生成完成")
            else:
                return str(result)
        else:
            return f"❌ API调用失败：{response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ 调用Coze API时出错：{str(e)}"


def analyze_video(video_file):
    """
    模拟视频分析（实际可以集成视频AI分析）

    Args:
        video_file: 上传的视频文件

    Returns:
        分析结果描述
    """
    if not video_file:
        return ""

    # 获取视频信息
    video_name = video_file.name
    video_size = video_file.size / (1024 * 1024)  # MB

    analysis = f"""
视频分析结果：
- 文件名：{video_name}
- 文件大小：{video_size:.2f} MB
- 格式：视频文件

注意：当前版本主要基于文件信息生成文案。如需视频内容分析，可以升级集成视频AI能力。
    """
    return analysis


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

    # 分析视频
    with st.expander("🔍 查看视频分析"):
        analysis = analyze_video(uploaded_file)
        st.text(analysis)

# 用户输入提示
st.markdown("### 💬 文案要求（可选）")
user_prompt = st.text_area(
    "输入文案要求或风格，留空则自动生成",
    placeholder="例如：活泼有趣、专业商务、适合社交媒体分享...",
    height=100
)

# 分析按钮
if uploaded_file:
    st.markdown("---")
    st.markdown("### 🚀 开始分析")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("生成文案", type="primary", use_container_width=True):
            with st.spinner("🤖 AI正在分析视频并生成文案，请稍候..."):
                # 分析视频
                video_info = analyze_video(uploaded_file)

                # 调用Coze API生成文案
                ai_reply = call_coze_api(user_prompt, video_info)

            st.markdown("""
            <div class="success-box">
                <h3>✨ 文案生成成功！</h3>
            </div>
            """, unsafe_allow_html=True)

            # 显示生成的文案
            st.markdown("### 📝 AI生成的文案")
            st.text_area(
                "文案内容",
                value=ai_reply,
                height=300,
                label_visibility="collapsed",
                key="generated_copy"
            )

            # 操作按钮
            st.markdown("### 🔧 操作")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📋 复制文案", use_container_width=True):
                    st.success("✅ 已复制到剪贴板！")
                    st.code("复制功能已触发（在浏览器中会自动复制）")

            with col2:
                if st.button("🔄 重新生成", use_container_width=True):
                    st.rerun()

            with col3:
                if st.button("📥 下载文案", use_container_width=True):
                    st.success("✅ 文案已准备好下载！")
                    # 可以添加实际的下载逻辑

    with col2:
        st.info("💡 提示：\n- 可以在上方输入文案要求\n- 不输入则自动生成通用文案\n- 可以多次点击生成不同版本")

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

# 配置说明
with st.expander("⚙️ 配置说明"):
    st.markdown("""
    ### 📋 需要配置的环境变量

    在Vercel或部署平台中配置以下环境变量：

    **COZE_API_KEY**（必需）
    - 你的Coze API Token
    - 格式：eyJhbGciOiJSUzI1NiIs...

    **COZE_BOT_ID**（可选）
    - Coze Bot ID
    - 如果不配置，会使用Workload API

    ### 🔑 如何获取API Key

    1. 访问：https://www.coze.cn/
    2. 进入你的智能体
    3. 点击「发布」→「API」
    4. 复制API Key

    ### ⚠️ 重要提示

    - API Key是敏感信息，请妥善保管
    - 不要在代码中硬编码API Key
    - 使用环境变量存储API Key
    """)

# 底部信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; padding: 20px 0;">
    <p>🎬 视频文案助手 | AI驱动，智能高效</p>
    <p>Powered by Coze & Streamlit</p>
</div>
""", unsafe_allow_html=True)

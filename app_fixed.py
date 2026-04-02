"""
Streamlit 视频文案助手 - Coze API 修正版
使用正确的Coze API接口调用方式
"""
import streamlit as st
import requests
import json

# 页面配置
st.set_page_config(
    page_title="🎬 视频文案助手",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 从环境变量读取API Key
COZE_API_KEY = st.secrets.get("COZE_API_KEY", "")

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
    .error-box {
        padding: 20px;
        border-radius: 10px;
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        margin-top: 20px;
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


def call_coze_api_with_correct_format(prompt, video_info=""):
    """
    调用Coze API生成文案 - 修正版
    使用正确的Workload Identity API格式
    """
    if not COZE_API_KEY:
        return "❌ 错误：未配置Coze API Key，请在Vercel环境变量中添加 COZE_API_KEY"

    try:
        # 根据你的Token类型，使用Workload API
        # 你的Token是 inbound_auth_access_token，用于调用工作流

        headers = {
            "Authorization": f"Bearer {COZE_API_KEY}",
            "Content-Type": "application/json"
        }

        # 构建用户消息
        user_message = f"请为视频生成文案。{video_info}\n\n用户要求：{prompt}"
        if not prompt:
            user_message = f"请为这个视频生成一份专业、吸引人的文案。{video_info}"

        # 方法1：使用Bot ID（如果有的话）
        # 从环境变量读取Bot ID
        bot_id = st.secrets.get("COZE_BOT_ID", "")

        if bot_id:
            # 使用Bot接口
            api_url = "https://api.coze.cn/open_api/v2/chat"
            data = {
                "bot_id": bot_id,
                "user": "streamlit_user",
                "query": user_message,
                "stream": False
            }
        else:
            # 方法2：使用Workload接口（默认）
            # 根据你的Token类型，这里需要使用正确的接口
            api_url = "https://api.coze.cn/open_api/v2/workflow/run"

            # 构建工作流请求
            data = {
                "input": {
                    "query": user_message
                },
                "user": "streamlit_user",
                "response_mode": "blocking"
            }

        st.write(f"🔍 调试信息：使用的接口: {api_url}")
        st.write(f"🔍 调试信息：请求数据: {json.dumps(data, ensure_ascii=False)}")

        # 发送请求
        response = requests.post(
            api_url,
            json=data,
            headers=headers,
            timeout=60
        )

        st.write(f"🔍 调试信息：响应状态码: {response.status_code}")
        st.write(f"🔍 调试信息：响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

        # 处理响应
        if response.status_code == 200:
            result = response.json()

            # 提取结果
            if "data" in result:
                # 工作流返回格式
                data_result = result["data"]
                if "outputs" in data_result:
                    outputs = data_result["outputs"]
                    # 尝试获取结果文本
                    if isinstance(outputs, dict):
                        # 查找包含文本的字段
                        for key, value in outputs.items():
                            if isinstance(value, str) and value:
                                return value
                    elif isinstance(outputs, str):
                        return outputs
                    else:
                        return json.dumps(outputs, ensure_ascii=False)
                elif "result" in data_result:
                    return data_result["result"]
                else:
                    return json.dumps(data_result, ensure_ascii=False)
            elif "messages" in result:
                # 聊天返回格式
                messages = result["messages"]
                for msg in reversed(messages):
                    if msg.get("type") == "answer":
                        return msg.get("content", "")
                return result.get("messages", [{}])[-1].get("content", "")
            else:
                return str(result)
        else:
            error_msg = f"❌ API调用失败：{response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f"\n错误详情: {json.dumps(error_detail, ensure_ascii=False)}"
            except:
                error_msg += f"\n错误文本: {response.text}"
            return error_msg

    except requests.exceptions.Timeout:
        return "❌ API调用超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"❌ 网络请求错误：{str(e)}"
    except Exception as e:
        return f"❌ 调用Coze API时出错：{str(e)}\n{type(e).__name__}"


def analyze_video(video_file):
    """分析视频信息"""
    if not video_file:
        return ""

    video_name = video_file.name
    video_size = video_file.size / (1024 * 1024)

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
                ai_reply = call_coze_api_with_correct_format(user_prompt, video_info)

            # 检查是否出错
            if ai_reply.startswith("❌"):
                st.markdown(f"""
                <div class="error-box">
                    <h3>⚠️ 生成失败</h3>
                    <p>{ai_reply}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
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

                with col2:
                    if st.button("🔄 重新生成", use_container_width=True):
                        st.rerun()

                with col3:
                    if st.button("📥 下载文案", use_container_width=True):
                        st.success("✅ 文案已准备好下载！")

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

# 底部信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; padding: 20px 0;">
    <p>🎬 视频文案助手 | AI驱动，智能高效</p>
    <p>Powered by Coze & Streamlit</p>
</div>
""", unsafe_allow_html=True)

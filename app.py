import streamlit as st
from openai import OpenAI

# 1. 基础配置：这里是以阿里通义千问为例的“通用插座”配置
# 如果以后换成腾讯或DeepSeek，只需修改下面这两行
client = OpenAI(
    api_key="sk-b52fd42209394181bb4cefc03d957377",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 2. 页面装修 (对应你设计的 AI 法务助手风格)
st.set_page_config(page_title="AI 法务助手", page_icon="⚖️")
st.title("⚖️ AI 法务助手 - 智能大脑")
st.caption("基于 OpenAI 标准库驱动 | 国内环境直连测试")

# 3. 初始化对话历史 (session_state 就像量化交易中的历史K线缓存)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个专业的中国法律助理，专注于为残疾人群体提供法律援助建议。请用温和、清晰、易懂的中文回答。"}
    ]

# 4. 在界面上显示历史对话 (对应你截图中的对话框)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. 处理用户输入并获取 AI 回答
if prompt := st.chat_input("请输入您的法律问题..."):
    # 用户问的内容
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 思考的部分
    with st.chat_message("assistant"):
        try:
            # 使用标准的 chat.completions.create 接口
            response = client.chat.completions.create(
                model="qwen-plus", # 阿里通义千问模型名
                messages=st.session_state.messages,
                stream=False
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            # 将回答存入历史，以便 AI 记得上下文
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"连接 AI 服务器失败，请检查 API Key 或网络：{str(e)}")
import streamlit as st
import requests
import json
import re
from datetime import datetime

# 页面配置
st.set_page_config(page_title="B 站评论分析器", page_icon="📊", layout="wide")

st.title("📊 B 站视频评论分析器")
st.markdown("---")

# 侧边栏 - AI 配置
with st.sidebar:
    st.header("️ AI 模型配置")
    baseurl = st.text_input("Base URL", value="https://api.openai.com/v1", help="AI 模型的 API 地址")
    model_id = st.text_input("模型 ID", value="gpt-3.5-turbo", help="使用的模型名称")
    api_key = st.text_input("API Key", type="password", help="您的 API 密钥")
    
    st.markdown("---")
    st.info("💡 提示：支持任意 OpenAI 兼容格式的 AI 模型")

# 主界面
col1, col2 = st.columns([2, 1])
with col1:
    video_url = st.text_input("🔗 B 站视频链接", placeholder="请输入 B 站视频链接（支持 BV/AV 号）", help="例如：https://www.bilibili.com/video/BV1xx411c7mD")
    
with col2:
    max_pages = st.number_input("📄 爬取页数", min_value=1, max_value=20, value=5, help="每页约 20 条评论")

# 辅助函数
def extract_video_id(url):
    bv_match = re.search(r'BV[a-zA-Z0-9]+', url)
    if bv_match:
        return bv_match.group()
    av_match = re.search(r'av(\d+)', url)
    if av_match:
        return f"av{av_match.group(1)}"
    return None

def bv_to_av(bv_id, headers):
    try:
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        if data['code'] == 0:
            return str(data['data']['aid'])
    except:
        pass
    return "0"

def clean_content(content):
    content = re.sub(r'\[.*?\]', '', content)
    content = re.sub(r'<[^>]+>', '', content)
    return ' '.join(content.split())

def fetch_comments(video_id, max_p
















































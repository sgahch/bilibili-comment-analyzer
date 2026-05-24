import requests
import json
import re
from datetime import datetime

class BilibiliCommentAnalyzer:
    """B 站视频评论爬取与 AI 分析工具"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.bilibili.com/'
        }
        self.comments_data = []
        self.ai_config = None
    
    def extract_video_id(self, url):
        """从 B 站视频链接中提取 BV 号或 AV 号"""
        # 提取 BV 号
        bv_match = re.search(r'BV[a-zA-Z0-9]+', url)
        if bv_match:
            return bv_match.group()
        
        # 提取 AV 号
        av_match = re.search(r'av(\d+)', url)
        if av_match:
            return f"av{av_match.group(1)}"
        
        raise ValueError("无法从链接中提取有效的 BV 号或 AV 号")
    
    def fetch_comments(self, video_id, max_pages=5):
        """爬取视频评论和子评论"""
        print(f"开始爬取视频 {video_id} 的评论...")
        
        # 获取视频 OID（需要先将 BV 号转换为 AV 号）
        if video_id.startswith('BV'):
            oid = self.bv_to_av(video_id)
        else:
            oid = video_id.replace('av', '')
        
        all_comments = []
        page = 1
        
        while page <= max_pages:
            try:
                api_url = f"https://api.bilibili.com/x/v2/reply?oid={oid}&type=1&sort=2&pn={page}&ps=20"
                response = requests.get(api_url, headers=self.headers, timeout=10)
                data = response.json()
                
                if data['code'] != 0:
                    print(f"API 返回错误：{data['message']}")
                    break
                
                replies = data['data'].get('replies',




















































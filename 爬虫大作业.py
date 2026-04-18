import requests
import re
import json
import csv
import time
import random

# 设置请求头，模拟浏览器访问
headers = {
    'Referer': 'https://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 定义一个函数，用于获取指定歌曲的评论
def get_comments(song_id, page):
    # 构造请求参数
    params = {
        'rid': 'R_SO_4_{}'.format(song_id),
        'offset': (page - 1) * 20,
        'total': 'false',
        'limit': '20'
    }
    # 发送请求
    try:
        response = requests.get('https://music.163.com/api/v1/resource/comments/R_SO_4_{}'.format(song_id), headers=headers, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('请求出错：', e)
        return
    # 解析响应数据
    data = json.loads(response.text)
    comments = data['comments']
    # 提取评论内容和点赞数
    with open('comments.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if page == 1:
            writer.writerow(['用户名', '评论内容', '点赞数量'])
        for comment in comments:
            content = comment['content']
            like_count = comment['likedCount']
            user = comment['user']['nickname']
            # 使用正则表达式去除评论中的表情和特殊字符
            content = re.sub(r'\[.*?\]', '', content)
            content = re.sub(r'[\n\ue003]', '', content)
            # 将数据写入csv文件
            writer.writerow([user, content, like_count])
    # 随机休眠1-3秒，防止被封IP
    time.sleep(1 + 2 * random.random())

# 爬取前5页评论
song_id = '186016'
for page in range(1, 6):
    get_comments(song_id, page)
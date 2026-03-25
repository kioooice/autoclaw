import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://github.com/trending'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)

try:
    html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
except:
    # 使用缓存的 HTML
    html = open('C:/Users/Administrator/.openclaw-autoclaw/workspace/scripts/github-trending.html', encoding='utf-8').read()

# 查找 article 标签
pattern = r'<article[^>]*>.*?</article>'
articles = re.findall(pattern, html, re.DOTALL)

repos = []
for article in articles:
    # 提取仓库链接
    link_match = re.search(r'href="(/[^/"]+/[^/"]+)"', article)
    if link_match:
        repo_path = link_match.group(1)
        if not any(x in repo_path.lower() for x in ['login', 'signup', 'settings', 'trending']):
            # 提取仓库描述
            desc_match = re.search(r'<p[^>]*>([^<]*)</p>', article)
            desc = desc_match.group(1).strip() if desc_match else ''
            # 提取 stars
            star_match = re.search(r'([0-9,]+)\s*stars?\s*today', article, re.IGNORECASE)
            stars = star_match.group(1) if star_match else ''
            repos.append((repo_path, desc, stars))

print('GitHub Trending 今日热点')
print('=' * 50)
for i, (repo, desc, stars) in enumerate(repos[:15], 1):
    print(f'{i}. [{repo.strip("/")}]{" (" + stars + " stars today)" if stars else ""}')
    if desc:
        print(f'   {desc[:70]}')
print()
print(f'数据来源：https://github.com/trending')
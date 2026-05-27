import requests
from bs4 import BeautifulSoup
import datetime
import os

if not os.path.exists('content/posts'):
    os.makedirs('content/posts')

base_url = "https://books.toscrape.com/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('article', class_='product_pod', limit=5)
today = datetime.date.today().strftime('%Y-%m-%d')

for i, book in enumerate(books):
    # 1. 목록 페이지에서 상세 페이지 링크 가져오기
    detail_url = base_url + book.h3.a['href']
    
    # 2. 상세 페이지 접속
    detail_res = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
    
    # 3. 데이터 추출
    title = detail_soup.find('h1').text
    price = detail_soup.find('p', class_='price_color').text
    # 상세 설명(요약) 가져오기: <article> 안의 <p> 태그 텍스트
    description = detail_soup.find_all('p')[3].text 
    
    file_path = f"content/posts/{today}-book-{i+1}.md"
    
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: \"{title}\"\ndate: {datetime.datetime.now()}\n---\n\n")
            f.write(f"# {title}\n\n")
            f.write(f"**가격:** {price}\n\n")
            f.write(f"## 요약\n{description}\n")
        print(f"상세 정보 포함 생성 완료: {file_path}")
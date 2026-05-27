import requests
from bs4 import BeautifulSoup
import datetime
import os

# 1. content/posts/ 폴더가 없으면 자동으로 만들기
if not os.path.exists('content/posts'):
    os.makedirs('content/posts')

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 책 5권 가져오기
books = soup.find_all('article', class_='product_pod', limit=5)
today = datetime.date.today().strftime('%Y-%m-%d')

for i, book in enumerate(books):
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    
    # 2. 파일 저장 경로 수정 (content/posts/ 폴더 안으로)
    file_path = f"content/posts/{today}-book-{i+1}.md"
    
    # 이미 파일이 있다면 중복 생성 방지
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: \"{title}\"\ndate: {datetime.datetime.now()}\n---\n\n")
            f.write(f"# 책 제목: {title}\n\n")
            f.write(f"**가격:** {price}\n")
        print(f"생성 완료: {file_path}")
    else:
        print(f"이미 존재함: {file_path}")
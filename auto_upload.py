import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime # 날짜를 자동으로 넣어주기 위해 추가

# 1. 크롤링 함수 (정보 가져오기)
def get_books():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books_data = []
    # 5개만 가져오기
    articles = soup.find_all('article', class_='product_pod', limit=5)
    for article in articles:
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text
        books_data.append({"title": title, "price": price})
    return books_data

# 2. 파일 저장 함수 (마크다운 생성)
def save_md(book):
    # 날짜(오늘 날짜)를 파일 이름에 추가 (블로그 필수 양식)
    date_str = datetime.now().strftime("%Y-%m-%d")
    clean_title = book['title'].replace(' ', '_').replace('/', '') # 파일명에 쓰기 부적합한 기호 제거
    filename = f"content/posts/{date_str}-{clean_title}.md"
    
    content = f"---\nlayout: post\ntitle: '{book['title']}'\n---\n\n# {book['title']}\n\n가격: {book['price']}"
    
    # 디렉토리가 없으면 생성
    if not os.path.exists('_posts'):
        os.makedirs('_posts')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

# 3. 깃허브 업로드 함수
def upload_to_github(filename):
    os.system(f'git add "{filename}"')
    os.system('git commit -m "Add new book post"')
    os.system('git push origin main')

# 4. 전체 실행
if __name__ == "__main__":
    books = get_books()
    for book in books:
        file = save_md(book)
        upload_to_github(file)
        print(f"{book['title']} 업로드 완료!")
        time.sleep(300) # 5분 대기
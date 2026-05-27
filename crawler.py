import requests
from bs4 import BeautifulSoup
import datetime
import os
import random  # 랜덤 기능을 사용하기 위해 추가

if not os.path.exists('content/posts'):
    os.makedirs('content/posts')

base_url = "https://books.toscrape.com/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# 1. 전체 책 목록 가져오기
all_books = soup.find_all('article', class_='product_pod')

# 2. 전체 목록에서 랜덤하게 5개 선택
selected_books = random.sample(all_books, 5)

today = datetime.date.today().strftime('%Y-%m-%d')

for book in selected_books:
    detail_url = base_url + book.h3.a['href']
    detail_res = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
    
    # 데이터 추출
    title = detail_soup.find('h1').text
    price = detail_soup.find('p', class_='price_color').text
    description = detail_soup.find_all('p')[3].text
    # 평점 가져오기 (클래스 이름에서 star-rating 뒤의 단어 추출)
    rating_class = detail_soup.find('p', class_='star-rating')['class']
    rating = rating_class[1] 
    
    file_path = f"content/posts/{today}-{title[:10].replace(' ', '_')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"---\ntitle: \"{title}\"\ndate: {datetime.datetime.now()}\n---\n\n")
        f.write(f"# {title}\n\n")
        f.write(f"**가격:** {price}\n")
        f.write(f"**평점:** {rating}\n\n")
        f.write(f"## 요약\n{description}\n")
    print(f"랜덤 생성 완료: {title}")
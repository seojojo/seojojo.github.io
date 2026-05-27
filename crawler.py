import requests
from bs4 import BeautifulSoup
import datetime
import os
import random

if not os.path.exists('content/posts'):
    os.makedirs('content/posts')

base_url = "https://books.toscrape.com/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

all_books = soup.find_all('article', class_='product_pod')

# 5개를 뽑을 때, 만약 목록이 5개보다 작으면 전체를 뽑도록 조정
num_to_pick = min(5, len(all_books))
selected_books = random.sample(all_books, num_to_pick)

today = datetime.date.today().strftime('%Y-%m-%d')
count = 0

for book in selected_books:
    try: # 오류가 나도 멈추지 않게 try-except 추가
        detail_url = base_url + book.h3.a['href']
        detail_res = requests.get(detail_url)
        detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
        
        title = detail_soup.find('h1').text
        price = detail_soup.find('p', class_='price_color').text
        # description이 없을 경우를 대비
        desc_tags = detail_soup.find_all('p')
        description = desc_tags[3].text if len(desc_tags) > 3 else "설명 없음"
        
        rating_class = detail_soup.find('p', class_='star-rating')['class']
        rating = rating_class[1] 
        
        # 파일명 중복 피하기 위해 count 추가
        file_path = f"content/posts/{today}-{count}-{title[:5].replace(' ', '_')}.md"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: \"{title}\"\ndate: {datetime.datetime.now()}\n---\n\n")
            f.write(f"# {title}\n\n")
            f.write(f"**가격:** {price}\n")
            f.write(f"**평점:** {rating}\n\n")
            f.write(f"## 요약\n{description}\n")
        count += 1
        print(f"성공: {title}")
    except Exception as e:
        print(f"오류 발생: {e}")
import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

# 노션 토큰, DB ID 가져오기
NOTION_TOKEN = os.getenv("NOTION_KEY")
DB_ID  = os.getenv("DATABASE_ID")

# 노션 DB 조회
url = f"https://api.notion.com/v1/databases/{DB_ID}/query"

# 정렬 조건 설정 (오름차순)
payload = {
    "sorts": [
        {
            "property": "재료명",
            "direction": "ascending"
        }
    ]
}

# 헤더 설정
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 냉장고 DB에서 재료 가져오기
def get_notion_refrigerator():
    response = requests.post(url, headers=headers, json=payload, timeout=10) # post 요청

    data = response.json()

    ingredients_list = [] # 재료 리스트 저장

    # 결과 페이지
    for page in data.get("results", []):
        props = page.get("properties", {})

        # 재료명 가져오기
        title_list = props.get("재료명", {}).get("title", [])

        # 값이 존재할 경우
        if title_list:
            ingredient = title_list[0].get("plain_text", "")

            if ingredient:
                ingredients_list.append(ingredient)

    # 최종 재료 리스트 반환
    return ingredients_list


# 재료 번역 함수 (한국어 -> 영어)
def ingredients_translate(ingredients):
    """한국어 재료 리스트를 영어로 번역"""

    translated_list = []

    # 입력된 재료 리스트를 하나씩 반복
    for ingredient in ingredients:
        ingredient = ingredient.strip()  # 공백 제거

        if not ingredient: # 빈 값 건너뜀
            continue

        try:
            # Google 번역 사용
            translated = GoogleTranslator(source='ko', target='en').translate(ingredient)

        except Exception as e:
            # 번역 실패 시 원래 단어 그대로 사용
            print(f"[번역 실패]: {ingredient} ({e})")
            translated = ingredient

        # 결과 리스트에 추가
        translated_list.append(translated)

    return translated_list


# 확인용
if __name__ == "__main__":

    # 노션에서 재료 가져오기
    result = get_notion_refrigerator()
    print("냉장고 재료:", result)

    # 영어로 번역!
    translated = ingredients_translate(result)
    print("번역 결과:", translated)

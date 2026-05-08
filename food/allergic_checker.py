"""
[API 요청 계획]
1. 냉장고 처럼 남아 있는 음식 재료를 가지고 만들 수 있는 음식을 찾기
=> 'Search Recipes' API
- intolerance : 알레르기 파라미터
- includeIngredients : 음식 재료 파라미터

2. API에서 제공하는 알레르기 종류는 총 9가지.
=> 알레르기 데이터베이스에서 체크한 것을 가지고 api 호출의 intolerance 파라미터에 추가

[필요 메소드]
- API 호출 메소드
- 알레르기 조회 메소드
- 재료 조회 메소드

[순서도]

알레르기 DB 접속 후 체크박스 체크 -> 체크된 알레르기 성분 조회 -> 냉장고 데이터베이스 조회 -> 번역 -> 파라미터화 -> API 요청

"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_allergic():
    """
        알레르기 데이터베이스에서 체크된 알레르기 유발 물질을 수집하는 메소드
        - 파라미터 : 없음
        - 리턴값 : 알레르기 유발 물질 (List)
    """
    # 환경 변수 세팅
    NOTION_KEY = os.getenv("NOTION_KEY")
    ALL_DB_ID = os.getenv("ALLERGIC_DB_ID")

    if not NOTION_KEY or not ALL_DB_ID:
        raise ValueError("env값 부재!")

    url = f"https://api.notion.com/v1/databases/{ALL_DB_ID}/query" 

    headers = {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    allergic_list = []
    
    # 알레르기 유발 물질 체크 유무 조회
    try:
        response = requests.post(url, headers=headers, timeout=10)
        data = response.json()
        
        page_list = data.get("results", {})

        for page in page_list:
            props = page.get("properties", {})
            check = props.get("활성화 여부", {}).get("checkbox", False)
            title_list = props.get("이름", {}).get("title", [])
            title = title_list[0].get("plain_text", "")

            if check:
                allergic_list.append(title)

    except Exception as e:
        print(e)    
    return allergic_list
    

if __name__ == "__main__":
    get_allergic()


import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_notion_refrigerator():
    """
    노션에서 냉장고 데이터베이스를 읽어와서
    딕셔너리 리스트 형태로 반환하는 함수
    """

    NOTION_TOKEN = os.getenv("NOTION_KEY")
    DB_ID = os.getenv("DATABASE_ID")

    if not NOTION_TOKEN or not DB_ID:
        return {"error": ".env 설정 확인 필요"}

    url = f"https://api.notion.com/v1/databases/{DB_ID}/query"

    # 헤더 설정
    headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, timeout=10)
        response.raise_for_status()
    
    except Exception as e:
        return {"error": str(e)}
    
    else:
        data = response.json()
        page_list = data.get("results", [])

        # 냉장고 재료 리스트
        refrigerator_list = []

        for page in page_list:
            props = page.get("properties")

            # 고유 id 추가
            page_id = page.get("id", "id 없음")

            # 재료명 (title)
            title_list = props.get("재료명", {}).get("title", [])
            title = title_list[0].get("plain_text") if title_list else "이름 없음"

            # 활성화 여부 (checkbox)
            is_active = props.get("활성화 여부", {}).get("checkbox", False)

            quantity = props.get("수량", {}).get("number") or 0

            refrigerator_list.append({
                "id": page_id,
                "title" : title,
                "is_active": is_active,
                "quantity": quantity
            })

        return refrigerator_list
        # [{'id': '358e9b8c-de0a-806d-8132-f629e092e090', 'title': '달걀', 'is_active': True, 'quantity': 5}, 
        # {'id': '358e9b8c-de0a-8084-85b2-dd351805e8ac', 'title': '오이', 'is_active': False, 'quantity': 0}, 
        # {'id': '358e9b8c-de0a-808a-94ef-d4b337caebe7', 'title': '우유', 'is_active': True, 'quantity': 1}, 
        # {'id': '358e9b8c-de0a-80b0-92e7-efdd845fa4b5', 'title': '당근', 'is_active': True, 'quantity': 1}, 
        # {'id': '358e9b8c-de0a-80de-8e5e-c28e072105c6', 'title': '설탕', 'is_active': True, 'quantity': 5}, 
        # {'id': '359e9b8c-de0a-810e-9fe7-dd90f403280d', 'title': '소고기', 'is_active': False, 'quantity': 10}, 
        # {'id': '359e9b8c-de0a-81be-bffd-e7960ef7c391', 'title': '무', 'is_active': False, 'quantity': 3}, 
        # {'id': '359e9b8c-de0a-81f2-a66b-df9f541521f8', 'title': '오이', 'is_active': False, 'quantity': 4}]

def get_available_refrigerator():
    """
    사용가능한 재료
    quantity가 0 이상인 재료들만 반환
    """
    ingredient_list = get_notion_refrigerator()

    available_ingredients = [ingreient for ingreient in ingredient_list if ingreient["quantity"] > 0]

    return available_ingredients
    # [{'id': '358e9b8c-de0a-806d-8132-f629e092e090', 'title': '달걀', 'is_active': True, 'quantity': 5}, 
    # {'id': '358e9b8c-de0a-808a-94ef-d4b337caebe7', 'title': '우유', 'is_active': True, 'quantity': 1},
    # {'id': '358e9b8c-de0a-80b0-92e7-efdd845fa4b5', 'title': '당근', 'is_active': True, 'quantity': 1}, 
    # {'id': '358e9b8c-de0a-80de-8e5e-c28e072105c6', 'title': '설탕', 'is_active': True, 'quantity': 5}, 
    # {'id': '359e9b8c-de0a-810e-9fe7-dd90f403280d', 'title': '소고기', 'is_active': False, 'quantity': 10}, 
    # {'id': '359e9b8c-de0a-81be-bffd-e7960ef7c391', 'title': '무', 'is_active': False, 'quantity': 3}, 
    # {'id': '359e9b8c-de0a-81f2-a66b-df9f541521f8', 'title': '오이', 'is_active': False, 'quantity': 4}]


def print_available_refrigerator():
    """
    사용 가능한 재료 출력
    """
    available_ingredients = get_available_refrigerator()
    print("현재 사용 가능한 냉장고 재료")
    print("-"*30)
    if not available_ingredients:
        print("현재 남은 재료가 없습니다")
    else:
        for idx, ingredient in enumerate(available_ingredients, 1):
            print(f"{idx}. {ingredient["title"]} : {ingredient["quantity"]}개")
    print("-"*30)
    #현재 사용 가능한 냉장고 재료
    # ------------------------------
    # 1. 달걀 : 5개
    # 2. 우유 : 1개
    # 3. 당근 : 1개
    # 4. 설탕 : 5개
    # 5. 소고기 : 10개
    # 6. 무 : 3개
    # 7. 오이 : 4개
    # ------------------------------
    
# 테스트용 출력
if __name__ == "__main__":
    print(get_notion_refrigerator())
    print(get_available_refrigerator())
    print_available_refrigerator()
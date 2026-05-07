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

            # 재료명 (title)
            title_list = props.get("재료명", {}).get("title", [])
            title = title_list[0].get("plain_text") if title_list else "이름 없음"

            # 활성화 여부 (checkbox)
            is_active = props.get("활성화 여부", {}).get("checkbox", False)

            quantity = props.get("수량", {}).get("number")
            if quantity == None:
                quantity = 0

            refrigerator_list.append({
                "title" : title,
                "is_active": is_active,
                "quantity": quantity
            })

        return refrigerator_list
        # refrigerator_list = [
        # {'title': '달걀', 'is_active': False, 'quantity': 0}, 
        # {'title': '오이', 'is_active': False, 'quantity': 0}, 
        # {'title': '우유', 'is_active': False, 'quantity': 0}, 
        # {'title': '당근', 'is_active': False, 'quantity': 0}, 
        # {'title': '설탕', 'is_active': False, 'quantity': 0}, 
        # {'title': '소고기', 'is_active': False, 'quantity': 10}]
    
# 테스트용 출력
if __name__ == "__main__":
    print(get_notion_refrigerator())
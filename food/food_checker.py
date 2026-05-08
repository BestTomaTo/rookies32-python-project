import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_food():
    """
        냉장고 데이터베이스에서 체크된 냉장고 재료를 수집하는 메소드
        - 파라미터 : 없음
        - 리턴값 : 냉장고 재료 (List)
    """
    # 환경 변수 세팅
    NOTION_KEY = os.getenv("NOTION_KEY")
    DB_ID = os.getenv("DATABASE_ID")

    if not NOTION_KEY or not DB_ID:
        raise ValueError("env값 부재!")

    url = f"https://api.notion.com/v1/databases/{DB_ID}/query" 

    headers = {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    food_list = []
    
    # 냉장고 재료 체크 유무 조회
    try:
        response = requests.post(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        page_list = data.get("results", {})
        # print(page_list)

        for page in page_list:
            props = page.get("properties", {})
            
            qty = props.get("수량", {}).get("number", 0)
            check = props.get("활성화 여부", {}).get("checkbox", False)
            
            if check and qty:
                title_list = props.get("재료명", {}).get("title", [])
                title = title_list[0].get("plain_text", "")

                food_list.append(title)

    except Exception as e:
        print(e)    
    return food_list
    

if __name__ == "__main__":
    get_food()


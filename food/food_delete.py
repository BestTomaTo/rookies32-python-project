import os, requests
from dotenv import load_dotenv

load_dotenv()

# 공통 설정
HEADERS = {
    "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
DB_ID = os.getenv("DATABASE_ID")

def delete_food(name, amount):
    # 1. 노션 DB에서 입력받은 이름으로 재료 찾기
    query_url = f"https://api.notion.com/v1/databases/{DB_ID}/query"
    query_data = {
        "filter": {
            "property": "재료명", 
            "title": {"equals": name}
        }
    }
    
    try:
        # 검색 요청
        res = requests.post(query_url, headers=HEADERS, json=query_data).json()
        results = res.get("results")

        if not results:
            print(f"'{name}'(은)는 냉장고에 없어.")
            return

        # 2. 해당 재료의 ID랑 현재 수량 파악
        page_id = results[0]["id"]
        current = results[0]["properties"]["수량"]["number"] or 0

        # 3. 차감 계산 (0보다 작아지지 않게)
        new_val = max(0, current - amount)

        # 4. 계산된 값을 노션에 업데이트
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        update_payload = {
            "properties": {
                "수량": {"number": new_val}
            }
        }
        
        response = requests.patch(update_url, headers=HEADERS, json=update_payload)
        
        if response.status_code == 200:
            print(f"✅ {name} 차감 완료: {current} -> {new_val}")
        else:
            print("❌ 노션 업데이트 실패")

    except Exception as e:
        print(f"에러 났음: {e}")

if __name__ == "__main__":
    name = input("제거할 음식 재료를 입력하세요: ")
    amount = int(input("제거할 수량을 입력하세요: "))
    delete_food(name, amount)
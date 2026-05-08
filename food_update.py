import os
import requests
from dotenv import load_dotenv
from check_refrigerator import get_notion_refrigerator

load_dotenv()

def update_food():
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

    ingredients_list = get_notion_refrigerator()
    
    if not ingredients_list:
        print("수정할 재료가 없습니다.")
        return

    while True:
        try:
            # 현재 재료 목록 출력
            print("현재 재료 목록 : ")
            for i, ingredient in enumerate(ingredients_list):
                print(f"{i+1}. {ingredient}")

            # 수정할 재료 선택(번호 or 뒤로가기(b) 입력받기)
            user_input = input("수정할 재료 번호 (뒤로가기 : b)): ").strip()

            if user_input.lower() == "b":
                return

            idx = int(user_input) - 1

            if idx < 0 or idx >= len(ingredients_list):
                raise ValueError("유효한 번호를 입력해주세요.")

            while True:
                new_ingredient = input("새로운 재료를 입력하세요 : ").strip()
                # 재료 이름이 비어있을 경우
                if not new_ingredient:
                    print("재료 이름은 비어 있을 수 없습니다.")
                    continue

                # 중복 체크
                if new_ingredient in ingredients_list:
                    print("이미 있는 재료입니다. 다른 재료를 입력해주세요.")
                    continue

                break 

            old_ingredient = ingredients_list[idx]
            ingredients_list[idx] = new_ingredient
            save_ingredients() # 변경된 재료 저장

            print(f"재료 '{old_ingredient}'가 '{new_ingredient}'로 변경되었습니다.")
            break

        except Exception as e:
            print(e)

if __name__ == "__main__":
    update_food()
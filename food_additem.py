import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_KEY")
DB_ID = os.getenv("DATABASE_ID")

notion_url = f"https://api.notion.com/v1/pages"

additem_headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}", 
    "Notion-Version": "2022-06-28", 
    "Content-Type": "application/json"
}

def add_imgredient():
    """ 사용자에게 재료명과 수량을 입력받음
    노션 데이터베이스에 추가
    기존 재료가 있을시 수량 추가
    없을시 새로 생성"""

    # 재료명과 수량 입력 받기
    ingredient_name = input("재료명을 입력해주세요 : ")
    ingredient_count = int(input("수량을 입력해주세요 : "))

    # 기존 재료 확인
    try:
        search_url = f"https://api.notion.com/v1/databases/{DB_ID}/query"

        search_payload = {
            "filter": {
                "property": "재료명", 
                "title": {
                    "equals": ingredient_name
                }
            }
        }

        response = requests.post(search_url, headers=HEADERS, json=search_payload, timeout=10)
        response = response.json()

        # 기존 재료가 존재하는 경우
        if result["results"]:
            page = result["results"][0]
            page_id = page["id"]
            old_count = page["properties"]["수량"]["number"]
            new_count = old_count + ingredient_count
            update_url = f"https://api.notion.com/v1/pages/{page_id}"
            update_payload = {
                "properties": {
                    "수량": {
                        "number": new_count
                    }
                }
            }
            update_response = requests.patch(search_url, headers=HEADERS, json=search_payload, timeout=10)
            update_response.raise_for_status()

            print("수량 업데이트 완료 !˘◡˘")

        else:
            # 노션 데이터베이스에 전송할 데이터
            payload = {
                "parent": {
                    "database_id" : DB_ID
                },
                "properties": {
                    "재료명": {
                        "title": [
                            {
                                "text": {
                                    "content": ingredient_name
                                }
                            }
                        ]
                    },
                    "수량": {
                        "number": ingredient_count
                    }
                },
                # 이모지 설정
                "icon": {
                    "type": "emoji",
                    "emoji": "🥩" # 해당하는 이모지
                }
            }
    
            create_response = requests.post(create_url, headers=HEADERS, create_json=payload, timeout=10)

            create_response.raise_for_status()

            print("새로운 재료가 추가되었습니다 ! ✦‿✦")

    # 에러 발생 알림
    except requests.exceptions.HTTPError as e:
        print(f" 노션 API 에러 : {e}")

    except ValueError:
        print("숫자로 입력 부탁드립니다 !")

    except Exception as e:
        print(f"에러 발생 : {e}")

# 함수 실행
add_imgredient()
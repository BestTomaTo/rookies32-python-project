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
    노션 데이터베이스에 추가"""

    # 재료명과 수량 입력 받기
    ingredient_name = input("재료명을 입력해주세요 : ")
    ingredient_count = int(input("수량을 입력해주세요 : "))

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
            "활성화 여부": {
                "checkbox": False
            },
            "수량": {
                "number": ingredient_count
            }
        }
        # 저희 아이콘 설정 부분도 배웠는데 넣는거 어떠신지 !!!!!
    }

    try:
        response = requests.post(
            notion_url,
            headers = additem_headers,
            json = payload,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        print("재료가 추가되었습니다 !")
        # print(data)

    # 에러 발생 알림 - 배운 부분이라 추가해봤습니다
    except requests.exceptions.HTTPError as e:
        print(f" 노션 API 에러 : {e}")

    except ValueError:
        print("숫자로 입력 부탁드립니다 !")

    except Exception as e:
        print(f"에러 발생 : {e}")

# 함수 실행
if __name__ == "__main__":
    add_imgredient()
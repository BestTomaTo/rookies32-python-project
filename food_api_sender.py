"""
[API 요청 계획]
1. 냉장고 처럼 남아 있는 음식 재료를 가지고 만들 수 있는 음식을 찾기
=> 'Search Recipes' API
- intolerance : 알레르기 파라미터
- includeIngredients : 음식 재료 파라미터

2. API에서 제공하는 알레르기 종류는 총 9가지.
=> 알레르기 데이터베이스에서 체크한 것을 가지고 api 호출의 intolerance 파라미터에 추가

[필요 기능]
- API 호출 기능
- 알레르기 조회 기능
- 재료 조회 기능


[순서도]

알레르기 DB(Notion) 조회     ->   냉장고 데이터베이스(Notion) 조회   ->   번역(Google Translator)   ->   파라미터화   ->   API 요청
allergic_checker.py              get_notion_refrigerator()                                                            food_api.py                
"""

import os
import requests
from dotenv import load_dotenv
from allergic_checker import get_allergic
from check_refrigerator import get_available_refrigerator
from food_checker import get_food

load_dotenv()

def send_food_api():
    while True:
        # 알레르기 DB 조회
        print("Notion에 가서 알레르기가 있는 재료에 체크하고 오세요!\n")
        v = input("완료하셨나요? y/n ")
        if v == 'y': intolerance_list = get_allergic() 
        else: continue

        # 냉장고 데이터베이스 조회
        print("Notion에 가서 사용하고자 하는 재료에 체크하고 오세요!\n")
        v = input("완료하셨나요? y/n ")
        if v == 'y': nangjango_list = get_food()
        else: continue

        # 파라미터화
        print("\n")
        print("=" * 60)
        print(f"알레르기 정보 : {intolerance_list}")
        print(f"음색 재료 정보 : {nangjango_list}")
        print("=" * 60)
        print("\n")

        print("위 정보가 맞나요? \n" \
        "1. 맞다 \n" \
        "2. Notion 재설정 \n" \
        "3. 메인메뉴 \n")
        v = input("메뉴를 선택해주세요 1/2/3 ")

        # 번역
        google_translator = []

        if v == '1': break
        elif v == '3': return
        else: continue
        

    # API 요청
    SPOON_API_KEY = os.getenv("SPOON_API_KEY")
    spoon_url = "https://api.spoonacular.com/recipes/complexSearch"
    spoon_headers = {
        'x-api-key': SPOON_API_KEY
    }
    
    params = {
        "intolerances": intolerance_list,
        "includeIngredients": nangjango_list,
        "number": 5,
        "fillIngredients": True
    }
    
    response = requests.get(spoon_url, headers=spoon_headers, params=params)
    recommend_food_data = response.json().get("results", [])
    
    print("=" * 60)
    print("현재 재료로 만들 수 있는 요리는 다음과 같습니다.")
    for i in range(len(recommend_food_data)):
        used_ingredients = recommend_food_data[i].get("usedIngredients", [])
        unused_ingredients = recommend_food_data[i].get("missedIngredients", [])
        
        print(f"{i+1}. {recommend_food_data[i].get("title", None)}")
        print("냉장고에서 사용되는 재료: ")
        for i in range(len(used_ingredients)):
            print(f"{i+1}. {used_ingredients[i].get("name", None)}")
        print("냉장고에 없는 재료: ")
        for i in range(len(unused_ingredients)):
            print(f"{i+1}. {unused_ingredients[i].get("name", None)}")
        print("-" * 60)

    # 사용한 음식 수량 재설정
    


if __name__ == "__main__":
    send_food_api()
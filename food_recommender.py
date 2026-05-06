import os, requests
from dotenv import load_dotenv
from intolerances_manage import Intolerance

load_dotenv()

# ------------ spoonacular api 관련 데이터 정의 ------------
# spoonacular api key 가져오기
SPOON_API_KEY = os.getenv("SPOON_API_KEY")
spoon_url = "https://api.spoonacular.com/recipes/complexSearch"
spoon_headers = {
    'x-api-key': SPOON_API_KEY
}

# 알레르기 관련 설정
# instance 생성
intolerances_instance = Intolerance()

# ---------------------------------------------------------

option_dict = {
    1 : {"option" : "1. 재료 넣기"},
    2 : {"option" : "2. 재료 조회"},
    3 : {"option" : "3. 재료 변경"}, # match-case문의 번호와 달라 수정하였습니다.
    4 : {"option" : "4. 재료 삭제"},
    5 : {"option" : "5. 알레르기 등록"},
    6 : {"option" : "6. 음식 추천"}
}

def show_option():
    print("="*60)
    for k, v in option_dict.items():
        print(f"{k} : {v["option"]}")
    print("="*60)

def input_option():
    try:
        option_num = int(input("원하는 기능을 선택하세요. 종료는 0번: "))
    except:
        raise ValueError("숫자만 입력 가능합니다.")
    # 입력 예외 처리
    if not option_num:
        return None
    elif option_num < 1 or option_num > 6:
        raise ValueError("요구하는 형식의 값이 아닙니다.")
    return option_num

def create_food():
    pass

def read_food():
    pass

def update_food():
    pass

def delete_food():
    pass

def intolerances_option():
    """알레르기 관련 설정으로 넘어가는 함수"""
    try:
        intolerances_instance.show_intolerances_option()
    
    except ValueError as e:
        print(e)

def recommend_food():
    ingredients_list = "egg,sugar,carrot,apple,jicama,lime"# read_food() # 재료를 불러옴 출력 예시? ([egg, sugar])
    # ingredients = ",".join(ingredients_list)
    intolerances_list = intolerances_instance.return_intolerances_list() # 알레르기 정보 조회?
    intolerances = ",".join(intolerances_list)

    print(ingredients_list, intolerances) # 디버깅용 평소에는 주석 처리

    params = {
        "intolerances": intolerances,
        "includeIngredients": ingredients_list,
        "number": 5,
        "fillIngredients": True
    }

    response = requests.get(spoon_url, headers=spoon_headers, params=params)
    # 확인용(json형태로 response 확인)
    with open("result.json", "w", encoding="utf-8") as f:
        f.write(response.text)
    recommend_food_data = response.json().get("results", [])
    print(recommend_food_data)

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

while True:
    # 단순 기능 출력
    show_option()
    
    while True:
        # 기능 입력받기
        try:
            selected_option = input_option()
            break
        except Exception as e:
            print(e)
            continue
    
    if selected_option == None:
        break

    
    # 옵션 수행
    match selected_option:
        case 1:
            create_food()
        case 2:
            read_food()
        case 3:
            update_food()
        case 4:
            delete_food()
        case 5:
            intolerances_option()
        case 6:
            recommend_food()
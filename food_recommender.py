import os, requests
from dotenv import load_dotenv
from intolerances_manage import Intolerance

load_dotenv()

# ------------ spoonacular api 관련 데이터 정의 ------------
# spoonacular api key 가져오기
SPOON_API_KEY = os.getenv("SPOON_API_KEY")
spoon_url = "https://api.spoonacular.com/recipes/complexSearch"
spoon_headers = {
    'Content-Type': 'application/json',
    'apiKey': SPOON_API_KEY
}

# 알레르기 관련 설정
# instance 생성
intolerances = Intolerance()

# ---------------------------------------------------------

option_dict = {
    1 : {"option" : "1. 재료 넣기"},
    2 : {"option" : "2. 재료 조회"},
    3 : {"option" : "3. 재료 삭제"},
    4 : {"option" : "4. 재료 변경"},
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
    while True:
        try:
            intolerances.show_intolerances_option()
            break
        
        except ValueError as e:
            print(e)
            continue


def recommend_food():
    ingredients_list = read_food() # 재료를 불러옴 출력 예시? ([egg, sugar])
    ingredients = ",".join(ingredients_list)
    intolerances_list = intolerances_list() # 알레르기 정보 조회?

    params = {
        "intolerances": intolerances_list,
        "includeIngredients": ingredients_list
    }

    response = requests.get(spoon_url, headers=spoon_headers, params=params)

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
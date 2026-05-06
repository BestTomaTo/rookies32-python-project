import os, requests
from dotenv import load_dotenv
from intolerances_manage import Intolerance
import json

load_dotenv()

# ------------ 재료 저장(임시) ------------
ingredients = ["egg","sugar","carrot","apple","jicama","lime"]
# 실행이 되는지 확인하기 위해 임시로 값 집어넣음
# 나중에 빈 리스트로 교체 필요 -> line 167의 load_ingredients() 주석 해제 
def save_ingredients(): # '현재 상태를 노션 DB에 반영'으로 변경 필요
    with open("foods.json", "w", encoding="utf-8") as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=4)
def load_ingredients(): # '노션 DB에 있는 데이터를 메모리로 가져오기'로 변경 필요
    global ingredients
    try:
        with open("foods.json", "r", encoding="utf-8") as f:
            ingredients = json.load(f)
    except FileNotFoundError:
        ingredients = []

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
    return ingredients

def update_food():
    ingredients_list = read_food()
    
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

# --------------- 프로그램 시작 ---------------
# load_ingredients()  프로그램 시작 시 재료 불러오기

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
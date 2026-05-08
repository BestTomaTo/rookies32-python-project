import os, requests
from dotenv import load_dotenv
from food_api_sender import send_food_api
from food_additem import add_imgredient
from check_refrigerator import print_available_refrigerator
from homework.delete_food import delete_food
from food_update import update_food

load_dotenv()

option_dict = {
    1 : {"option" : "1. 재료 넣기"},
    2 : {"option" : "2. 재료 조회"},
    3 : {"option" : "3. 재료 변경"},
    4 : {"option" : "4. 재료 삭제"},
    5 : {"option" : "5. 음식 추천"}
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
    add_imgredient()

def read_food():
    print_available_refrigerator()

def update_food_():
    update_food()

def delete_food_():
    name = input("제거할 음식 재료를 입력하세요: ")
    amount = float(input("제거할 수량을 입력하세요: "))
    delete_food(name, amount)

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
            update_food_()
        case 4:
            delete_food_()
        case 5:
            send_food_api()
           
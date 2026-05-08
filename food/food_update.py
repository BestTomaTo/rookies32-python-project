import os
import requests
from dotenv import load_dotenv
from food.check_refrigerator import get_notion_refrigerator

load_dotenv()

def update_notion_ingredient(id, new_title=None, new_quantity=None):
    """
    노션 DB의 특정 페이지(재료)를 수정하는 함수
    
    Parameters:
        id (str): 수정할 노션 페이지 고유 ID
        new_title (str): 변경할 재료명 (재료명 변경 시 사용, 기본값 None)
        new_quantity (int): 변경할 수량 (수량 변경 시 사용, 기본값 None)
    
    Returns:
        bool: 수정 성공 시 True, 실패 시 False
    """
    NOTION_TOKEN = os.getenv("NOTION_KEY")
    
    # 수정할 노션 페이지 URL (페이지 ID로 특정 항목 지정)
    url = f"https://api.notion.com/v1/pages/{id}"
    
    # 노션 API 요청 헤더 설정
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",  # 노션 인증 토큰
        "Notion-Version": "2022-06-28",              # 노션 API 버전
        "Content-Type": "application/json"           # 요청 데이터 형식
    }
    
    # 수정할 속성 딕셔너리 (변경 항목만 담음)
    properties = {}
    
    # 재료명 변경 시 노션 title 형식에 맞게 추가
    if new_title:
        properties["재료명"] = {"title": [{"text": {"content": new_title}}]}
    
    # 수량 변경 시 노션 number 형식에 맞게 추가
    if new_quantity is not None:
        properties["수량"] = {"number": new_quantity}
    
    try:
        # 노션 API에 PATCH 요청으로 해당 페이지 수정
        response = requests.patch(url, headers=headers, json={"properties": properties})
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
        return True
    except Exception as e:
        print(f"노션 업데이트 실패: {e}")
        return False


def update_food():
    """
    냉장고 재료를 수정하는 함수
    재료명 변경과 수량 변경 두 가지 기능을 제공
    """
    
    # 노션 DB에서 전체 재료 목록 불러오기
    # 반환 형태: [{"id": ..., "title": ..., "is_active": ..., "quantity": ...}, ...]
    ingredients_list = get_notion_refrigerator()

    # 노션 API 호출 실패 시 에러 딕셔너리 반환 → 에러 메시지 출력 후 종료
    if isinstance(ingredients_list, dict) and "error" in ingredients_list:
        print(f"재료 불러오기 실패: {ingredients_list['error']}")
        return

    # 재료 목록이 비어있을 경우 종료
    if not ingredients_list:
        print("수정할 재료가 없습니다.")
        return

    while True:
        # 현재 재료 목록 출력
        print("현재 재료 목록 : ")
        for i, ingredient in enumerate(ingredients_list):
            print(f"{i+1}. {ingredient['title']} : {ingredient['quantity']}개")

        # 수정할 재료 번호 입력 (b 입력 시 뒤로가기)
        user_input = input("수정할 재료 번호 (뒤로가기 : b): ").strip()
        if user_input.lower() == "b":
            return

        # 숫자가 아닌 문자열 입력 시 안내 메시지 출력
        try:
            idx = int(user_input) - 1
        except ValueError:
            print("유효한 번호를 입력해주세요.")
            continue

        # 범위 벗어난 번호 입력 시 안내 메시지 출력
        if idx < 0 or idx >= len(ingredients_list):
            print("유효한 번호를 입력해주세요.")
            continue

        # 선택한 재료 저장
        selected = ingredients_list[idx]

        # 잘못된 입력 시 수정할 항목 선택으로 돌아오도록 내부 while True로 감싸기
        while True:
            print("\n수정할 항목을 선택하세요.")
            print("1. 재료명 변경")
            print("2. 수량 변경")
            edit_choice = input("수정 항목 선택 (뒤로가기 : b): ").strip()

            if edit_choice.lower() == "b":
                # 재료 목록 선택으로 돌아가기
                break

            elif edit_choice == "1":
                # 재료명 변경
                while True:
                    new_title = input("새로운 재료명을 입력하세요: ").strip()
                    
                    # 빈 입력 방지
                    if not new_title:
                        print("재료 이름은 비어 있을 수 없습니다.")
                        continue
                    
                    # 기존 재료명과 중복 체크
                    existing_titles = [i["title"] for i in ingredients_list]
                    if new_title in existing_titles:
                        print("이미 있는 재료입니다.")
                        continue
                    break
                
                # 노션 DB에 재료명 수정 요청 후 결과 출력
                if update_notion_ingredient(selected["id"], new_title=new_title):
                    selected["title"] = new_title
                    print(f"'{selected['title']}' → '{new_title}'으로 변경되었습니다.")
                break  # 수정 완료 후 재료 목록으로 돌아가기

            elif edit_choice == "2":
                # 수량 변경
                new_quantity = input("새로운 수량을 입력하세요: ").strip()
                
                # 숫자가 아니거나 음수일 경우 다시 선택 화면으로
                if not new_quantity.isdigit() or int(new_quantity) < 0:
                    print("0 이상의 숫자를 입력해주세요.")
                    continue
                
                # 노션 DB에 수량 수정 요청 후 결과 출력
                if update_notion_ingredient(selected["id"], new_quantity=int(new_quantity)):
                    selected["quantity"] = int(new_quantity)
                    print(f"'{selected['title']}' 수량이 {int(new_quantity)}개로 변경되었습니다.")
                break  # 수정 완료 후 재료 목록으로 돌아가기

            else:
                # 1, 2, b 외의 값 입력 시 다시 선택 화면으로
                print("1 또는 2를 입력해주세요.")

if __name__ == "__main__":
    update_food()
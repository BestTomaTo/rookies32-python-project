import os, requests
from dotenv import load_dotenv

load_dotenv()

class Intolerance:
    def __init__(self):
        # .env 파일에서 민감한 정보 가져오기
        NOTION_KEY = os.getenv("NOTION_KEY")
        INTOLERANCES_DATABASE_ID = os.getenv("INTOLERANCES_DATABASE_ID")

        # 변수 정의(read와 patch를 위한 각각의 url 및 노션 api에 보낼 헤더 정의)
        self.intolerances_database_url_query = f"https://api.notion.com/v1/databases/{INTOLERANCES_DATABASE_ID}/query"
        self.intolerances_database_url_pages = f"https://api.notion.com/v1/pages/"
        self.intolerances_database_headers = {
            "Authorization": f"Bearer {NOTION_KEY}", 
            "Notion-Version": "2022-06-28", 
            "Content-Type": "application/json"
        }

        # 옵션을 정의한 딕셔너리 구조 show_intolerances_option() 함수에 사용
        self.intolerance_option = {
            0: "종료", 
            1: "알레르기 설정 조회", 
            2: "설정 변경", 
        }

    def show_intolerances_option(self):
        """알레르기 설정에 들어갔을 때 뜨는 옵션들"""
        while True: # 0이 나올 때 까지 반복
            print("="*60)
            for idx, v in self.intolerance_option.items():
                print(f"{idx} : {v}")
            
            choice_option = input("원하는 옵션을 적어주세요: ")
            # 입력된 값이 숫자가 아니거나 혹은 옵션 키값에 없으면 에러를 발생
            if not choice_option.isdigit() or int(choice_option) not in self.intolerance_option.keys():
                raise ValueError("옵션에 맞는 번호를 적어주세요.")
            
            match int(choice_option):
                case 1:
                    self.read_intolerances() # 알레르기 설정 조회 함수
                case 2:
                    self.change_check() # 알레르기 설정 변경 함수
                case 0:
                    break
    
    def read_intolerances(self, option="read"):
        """데이터베이스에 저장한 알레르기 정보에 대한 조회"""
        # post를 통해 알레르기 정보 데이터베이스를 요청
        response = requests.post(self.intolerances_database_url_query, headers=self.intolerances_database_headers, timeout=10)
        response.raise_for_status() # 에러 점검
        intolerance_dict = dict() # 훗날 필요할 경우를 대비한 딕셔너리 정의

        # json 확인(참고용)
        # a = response.text
        # with open("data.json", "w", encoding="utf-8") as f:
        #     f.write(a)
        data = response.json()
        page_list = data.get("results", [])

        print("=" * 50)
        print(f"알레르기 활성화여부 조회")
        for idx, page in enumerate(page_list, 1):
            # 알레르기 이름을 추출하는 과정
            props = page.get("properties", {})
            props_name = props.get("이름", {}).get("title", [])
            name = props_name[0].get("plain_text") if props_name else None

            # 알레르기 활성화 여부를 추출하는 과정
            check = props.get("체크박스", {}).get("checkbox", False)

            # 알레르기 페이지 ID를 추출하는 과정 => 활성화 여부를 변경할 때 사용됨
            page_id = page.get("id", "id 없음")

            # 만약 변경 시 사용될 딕셔너리 => intolerance_dict
            intolerance_dict[idx] = {"name": name, "check": check, "id": page_id}

            print(f"{idx}. {name} - {'1' if check else '0'}")

        if option == "return": # return이라는 인자가 들어오면 반환함 반면에 read면 그냥 출력만
            return intolerance_dict
        
    def change_check(self):
        """활성화 여부를 변경하기 위한 함수.\n
        notion에서는 활성화 여부가 checkbox로 되어있음.\n
        check시 True
        """

        # return이라는 인자를 보내 페이지 정보(딕셔너리 구조)를 가져옴
        intolerance_dict = self.read_intolerances("return")
        choice = input("활성화 및 비활성화를 원하는 번호를 적어주세요.: ")
        # 만약 값이 숫자가 아니거나 키값에 없을 경우 에러 발생
        if not choice.isdigit() or int(choice) not in intolerance_dict.keys():
            raise ValueError("올바른 값을 넣어주세요")
        
        # 체크 여부를 확인
        check_state = intolerance_dict.get(int(choice)).get("check")

        # body에 기존에 있던 체크 여부를 반대로 적용한 값을 담음
        payload = {
            "properties": {
                "체크박스": {
                    "checkbox": not check_state
                }
            }
        }

        # patch로 변경 사항을 보냄
        response = requests.patch(self.intolerances_database_url_pages + f"{intolerance_dict[int(choice)].get("id")}", 
                                  headers=self.intolerances_database_headers, json=payload)
        response.raise_for_status() # 에러 점검

        # 마지막 확인용 조회
        self.read_intolerances("read")

    def return_intolerances_list(self):
        intolerances_dict = self.read_intolerances("return")
        intolerances = list()

        for intolerance in intolerances_dict.items():
            if intolerance[1].get("check", False):
                intolerances.append(intolerance[1].get("name", None))
        return intolerances


if __name__ == "__main__":
    try:
        intolerance_manage = Intolerance()
        # intolerance_manage.show_intolerances_option()
        intolerance = intolerance_manage.return_intolerances_list()
        print(intolerance)
    except ValueError as e:
        print(e)
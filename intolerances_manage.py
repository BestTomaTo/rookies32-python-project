import os, requests
from dotenv import load_dotenv

load_dotenv()

class Intolerance:
    def __init__(self):
        NOTION_KEY = os.getenv("NOTION_KEY")
        INTOLERANCES_DATABASE_ID = os.getenv("INTOLERANCES_DATABASE_ID")

        self.intolerances_database_url = f"https://api.notion.com/v1/databases/{INTOLERANCES_DATABASE_ID}/query"
        self.intolerances_database_headers = {
            "Authorization": f"Bearer {NOTION_KEY}", 
            "Notion-Version": "2022-06-28", 
            "Content-Type": "application/json"
        }

        self.intolerance_option = {
            1: "알레르기 설정 조회", 
            2: "설정 추가", 
            3: "설정 삭제"
        }

    def show_intolerances_option(self):
        """알레르기 설정에 들어갔을 때 뜨는 옵션들"""
        print("="*60)
        for idx, v in self.intolerance_option.items():
            print(f"{idx} : {v}")
        
        choice_option = input("원하는 옵션을 적어주세요: ")
        if not choice_option.isdigit() or int(choice_option) not in self.intolerance_option.keys():
            raise ValueError("옵션에 맞는 번호를 적어주세요.")
        
        match int(choice_option):
            case 1:
                self.read_intolerances()
            case 2:
                self.add_intolerances()
            case 3:
                self.delete_intolerances()

    
    def read_intolerances(self, option="read"):
        """데이터베이스에 저장한 알레르기 정보에 대한 조회"""
        response = requests.post(self.intolerances_database_url, headers=self.intolerances_database_headers, timeout=10)
        response.raise_for_status()
        intolerance_dict = dict()

        # json 확인(참고용)
        # a = response.text
        # with open("data.json", "w", encoding="utf-8") as f:
        #     f.write(a)
        data = response.json()
        page_list = data.get("results", [])

        print("=" * 50)
        print(f"알레르기 활성화여부 조회")
        for idx, page in enumerate(page_list, 1):
            props = page.get("properties", {})
            props_name = props.get("이름", {}).get("title", [])
            name = props_name[0].get("plain_text") if props_name else None

            check = props.get("체크박스", {}).get("checkbox", False)

            intolerance_dict[idx] = {"name": name, "check": check}

            print(f"{idx}. {name} - {'1' if check else '0'}")

        if option == "return":
            return intolerance_dict
        
    def change_check(self):
        intolerance_dict = self.read_intolerances("return")
        choice = input("활성화 및 비활성화를 원하는 번호를 적어주세요.: ")
        if not choice.isdigit() or int(choice) not in intolerance_dict.keys():
            raise ValueError("올바른 값을 넣어주세요")
        response = requests.patch(url, headers=self.intolerances_database_headers)
        response.raise_for_status()

    def intolerances_list(self):
        pass

if __name__ == "__main__":
    try:
        intolerance_manage = Intolerance()
        intolerance_manage.show_intolerances_option()
        intolerance_manage.read_intolerances("read")
        intolerance_dict = intolerance_manage.read_intolerances("return")
        intolerance_manage.add_intolerances()
    except ValueError as e:
        print(e)
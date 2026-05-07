import os, requests
from dotenv import load_dotenv
from intolerances_manage import Intolerance


class FoodRecommended():
    def __init__(self, intolerances_instance):
        # spoonacular api key 가져오기
        self.SPOON_API_KEY = os.getenv("SPOON_API_KEY")
        self.spoon_url = "https://api.spoonacular.com/recipes/complexSearch"
        self.spoon_headers = {
            'x-api-key': self.SPOON_API_KEY
        }
        self.intolerances_instance = intolerances_instance


    def recommend_food(self):
        ingredients_list = "egg, potato, onion" # read_food() # 재료를 불러옴 출력 예시? ([egg, sugar])
        # ingredients = ",".join(ingredients_list)
        intolerances_list = self.intolerances_instance.return_intolerances_list() # 알레르기 정보 조회?
        intolerances = ",".join(intolerances_list)
        food_info = dict()

        # print(ingredients_list, intolerances) # 디버깅용 평소에는 주석 처리

        params = {
            "intolerances": intolerances, # 사용자가 가지고 있는 알레르기 정보
            "includeIngredients": ingredients_list, # 냉장고에 있는 재료
            "number": 5, # 나오는 결과 수
            "fillIngredients": True # 재료에 대한 정보 추가 및 냉장고에서 사용되는 재료와 냉장고에 없는 재료를 알려줌
        }

        response = requests.get(self.spoon_url, headers=self.spoon_headers, params=params)
        # 확인용(json형태로 response 확인) 평소에는 주석처리
        # with open("result.json", "w", encoding="utf-8") as f:
        #     f.write(response.text)
        recommend_food_data = response.json().get("results", [])
        # print(recommend_food_data) # 디버깅용 평소에는 주석처리

        print("=" * 60)
        print("현재 재료로 만들 수 있는 요리는 다음과 같습니다.")
        for i in range(len(recommend_food_data)):
            used_ingredients_list = list()
            unused_ingredients_list = list()

            used_ingredients = recommend_food_data[i].get("usedIngredients", [])
            unused_ingredients = recommend_food_data[i].get("missedIngredients", [])

            # 추천 요리 출력
            print(f"{i+1}. {recommend_food_data[i].get('title', None)}")
            
            print("냉장고에서 사용되는 재료: ")
            for j in range(len(used_ingredients)):
                used_ingredient = used_ingredients[j].get("name", None)
                used_ingredients_list.append(used_ingredient)
                print(f"{j+1}. {used_ingredient}")
            print("냉장고에 없는 재료: ")
            for k in range(len(unused_ingredients)):
                unused_ingredient = unused_ingredients[k].get("name", None)
                unused_ingredients_list.append(unused_ingredient)
                print(f"{k+1}. {unused_ingredient}")
            print("-" * 60)

            # 요리와 관련 재료 딕셔너리에 저장
            food_info[f"{recommend_food_data[i].get("title", None)}"] = {
                "used_ingredients" : used_ingredients_list, 
                "unused_ingredients" : unused_ingredients_list
            }
        return food_info


if __name__ == "__main__":
    intolerances = Intolerance()
    food_Recommended = FoodRecommended(intolerances)
    food_Recommended.recommend_food()
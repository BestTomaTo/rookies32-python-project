import requests

# 재료 번역 함수
def ingredients_translate(ingredients):
    """한국어 재료 리스트를 영어로 번역하는 함수"""

    translated_list = []

    # 입력된 재료 리스트를 하나씩 반복
    for ingredient in ingredients:
        ingredient = ingredient.strip()  # 공백 처리

        if not ingredient: # 빈 값 건너뜀
            continue

        # 번역 API 주소 - 무료 5000자?까지 가능
        mymemory_url = "https://api.mymemory.translated.net/get"

        # 파라미터 설정 (번역할 재료, 언어)
        parameters = {
            "q": ingredient,      # 번역할 재료
            "langpair": "ko|en"   # 한국어 -> 영어
        }

        try:
            response = requests.get(mymemory_url, params=parameters, timeout=5)
            data_result = response.json()

            # 번역 결과 출력
            translated = data_result["responseData"]["translatedText"]

        except Exception as e:
            # 실패하면 원래 단어 그대로 사용
            print(f"[번역 실패]: {ingredient} ({e})")
            translated = ingredient

        # 결과 리스트에 추가
        translated_list.append(translated)

    return translated_list



# 확인용
if __name__ == "__main__":
     # 실행이 되는지 확인하기 위해 임시로 값 넣음
    ingredients_list = ["밥", "치즈", "빵"]
    translated_result = ingredients_translate(ingredients_list)
    print(f"번역 확인: {ingredients_list} -> {translated_result}")
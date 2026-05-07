import os
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import schedule, time
from food_recommend_func import FoodRecommended
from intolerances_manage import Intolerance

load_dotenv()

def send_recommended_food(food_recommended):
    print("메일 보낼 준비 온")
    food_info = food_recommended.recommend_food()

    # smtp 접속 정보 로드
    user_email = os.getenv("EMAIL_USER")
    user_password = os.getenv("EMAIL_PASS")
    smtp_server = os.getenv("SMTP_SVR")
    smtp_port = os.getenv("SMTP_PORT")

    msg = MIMEMultipart()
    msg['Subject'] = "[식사 추천]"
    msg['From'] = user_email
    msg['To'] = user_email

    html_content = f"""
        <div style="font-family: Arial, sans-serif; background-color:#f4f6f8; padding:20px;">
            
            <h2 style="text-align:center; color:#333;">냉장고를 부탁해</h2>
            <p style="text-align:center; color:#777; font-size:14px;">
                오늘의 추천 메뉴입니다.
            </p>
            <img src="cid:image1" style="width:500px; border:1px solid pink">

            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:0 auto;">
                <tr>
                    <th width="33%" style="background:#fcf4d9; color:#000000; padding:10px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08); text-align:center">
                        <div style="font-size:12px; font-weight:bold; color:#222; margin-bottom:8px;">
                            오늘의 추천하는 음식
                        </div>
                    </th>
                    <th width="33%" style="background:#fcf4d9; color:#000000; padding:10px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08); text-align:center">
                        <div style="font-size:12px; font-weight:bold; color:#222; margin-bottom:8px;">
                            냉장고에 이 재료를 사용하세요
                        </div>
                    </th>
                    <th width="33%" style="background:#fcf4d9; color:#000000; padding:10px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08); text-align:center">
                        <div style="font-size:12px; font-weight:bold; color:#222; margin-bottom:8px;">
                            냉장고에 없어서 사야해요
                        </div>
                    </th>
                </tr>
                {''.join([
                    f"""
                    <tr>
                        <td style="background:#ffffff; padding:20px; margin-bottom:10px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08);">
                            <div style="font-size:16px; font-weight:bold; color:#222; margin-bottom:8px;">
                                {food}
                            </div>
                        </td>

                        <td style="background:#ffffff; padding:20px; margin-bottom:10px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08);">
                            <div style="font-size:13px; color:#888;">
                                ✍️ {", \n".join(ingredients['used_ingredients'])}
                            </div>
                        </td>

                        <td style="background:#ffffff; padding:20px; margin-bottom:10px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08);">
                            <div style="font-size:13px; color:#888;">
                                ✍️ {", \n".join(ingredients['unused_ingredients'])}
                            </div>
                        </td>
                    </tr>
                    <tr><td height="10"></td></tr>
                    """
                    for food, ingredients in food_info.items()
                ])}
            </table>

            <p style="text-align:center; font-size:12px; color:#aaa; margin-top:20px;">
                © 2026 Food Recommend
            </p>

        </div>
    """
    msg.attach(MIMEText(html_content, 'html', "utf-8"))

    # 서버 접속, 발송
    try:
        with SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(user_email, user_password)
            server.send_message(msg)
            print("메일 발송 성공")
    except Exception as e:
        print(f"오류 발생 : {e}")

def schedule_registeration(food_recommended):
    schedule.every(1).minutes.do(send_recommended_food, food_recommended)

if __name__ == '__main__':
    intolerances = Intolerance()
    food_recommended = FoodRecommended(intolerances)
    schedule_registeration(food_recommended)
    send_recommended_food(food_recommended)
    while True:
        schedule.run_pending()
        time.sleep(1)
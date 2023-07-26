from flask import Flask, request
import json
import mysql.connector
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, LocationMessage, TextSendMessage
from datetime import datetime
app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    now = datetime.now()
    body = request.get_data(as_text=True)
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    print("現在時間:", formatted_now)                   
    try:
        json_data = json.loads(body)                        
        access_token = 'UzV6hoOWEz0t8HfUos1jgM8jBBgh8fL0R2d7zDNbVDWrqBiskTcYQ+Nk5T+ESg2loCaDnzY0CBf4QM+75RAVM6NL1MbeVPxGdFY70f5msctPfEC9tCUBslFz9V/sdw+wTDDuzxHaFlX1M0aGI1dMxwdB04t89/1O/w1cDnyilFU='
        secret = 'c2fed2d1feb4e9d7641bc3e8cbc42558'
        line_bot_api = LineBotApi(access_token)             
        handler = WebhookHandler(secret)                    

        tk = json_data['events'][0]['replyToken']           
        user_id = json_data['events'][0]['source']['userId']
        profile = line_bot_api.get_profile(user_id)
        display_name = profile.display_name

        msg_type = json_data['events'][0]['message']['type']     
        if msg_type == 'location':
            address = json_data['events'][0]['message']['address']
            latitude = json_data['events'][0]['message']['latitude']
            longitude = json_data['events'][0]['message']['longitude']
            reply = "打卡成功"

            db = mysql.connector.connect(
                host="192.168.8.199",
                user="nick",
                password="951753",
                database="data"
            )
            cursor = db.cursor()
            sql = "INSERT INTO location (username, address, latitude, longitude, time) VALUES (%s, %s, %s, %s, %s)"
            val = (display_name, address, latitude, longitude, formatted_now)
            cursor.execute(sql, val)
            db.commit()

        else:
            reply = '請傳送座標打卡'
        
        line_bot_api.reply_message(tk, TextSendMessage(reply)) 
    except:
        print(body)                                          
    return 'OK'                                              

if __name__ == "__main__":
    app.run()

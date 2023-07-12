import requests
import subprocess
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
from linebot import LineBotApi
from linebot.models import ImageSendMessage, TextSendMessage
import random
import datetime

# Nature RemoのAPIキーとデバイスIDを設定
API_KEY = "【Nature RemoのAPI】"
DEVICE_ID = "【デバイスID】"
DEVICE_ID_SELECT_RASPI = "【HDMI分配器のラズパイのデバイスID】" // 必要であれば 

# LINEアクセストークン
ACCESS_TOKEN = "【LINEアクセストークン】"
# 画像とメッセージの送信先のユーザーID
USER_ID = "【送信先のユーザーID】"
line_bot_api = LineBotApi(ACCESS_TOKEN)


# アニメOPの動画ファイルのパスを設定
VIDEO_PATH_1 = "【動画ファイルのパス】"
VIDEO_PATH_2 = "【動画ファイルのパス】"
VIDEO_PATH_3 = "【動画ファイルのパス】"

# テレビの電源をオン
def turn_on_tv():
    headers = {
        'accept' : 'application/json',
        'Authorization' : 'Bearer ' + API_KEY ,
    }
    requests.post('https://api.nature.global/1/signals/' + DEVICE_ID + '/send', headers=headers, verify=False)
    requests.post('https://api.nature.global/1/signals/' + DEVICE_ID_SELECT_RASPI + '/send', headers=headers, verify=False)
   

# 動画再生
def play_video():
    # 現在の曜日を取得
    today = datetime.datetime.now().weekday()

    if today in [5, 6]:  # 土曜日と日曜日はVIDEO_PATH_3を再生
        subprocess.run(["omxplayer", VIDEO_PATH_3])
    else:  # 平日はVIDEO_PATH_1とVIDEO_PATH_2を順番に再生
        subprocess.run(["omxplayer", VIDEO_PATH_1])
        subprocess.run(["omxplayer", VIDEO_PATH_2])


# 目覚まし機能実行
def run_alarm():
    turn_on_tv()
    play_video()

# 画像とメッセージを送信する関数（動作確認用だったので別になくてもよい）
def send_image_and_message():
    # googleDriveに保存した画像のURL
     image_ids = ["【image1】","【image2】"]
     random_id = random.choice(image_ids)
     url_template = "https://drive.google.com/uc?export=view&id={}"
     random_url = url_template.format(random_id)

    # おはようのメッセージを設定
     morning_message = "【適当なメッセージ】"
     garbage_message = "【可燃ゴミの日通知メッセージ】"

     today = datetime.datetime.now().weekday()
     message = garbage_message if today in [2, 5] else morning_message
    # 画像とメッセージを含むメッセージオブジェクトを作成
    #image_message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
     text_message = TextSendMessage(text=message)

     image_message = ImageSendMessage(
     original_content_url=random_url,
     preview_image_url=random_url
    )
    # 画像とメッセージを送信
     line_bot_api.push_message(USER_ID, text_message)
     line_bot_api.push_message(USER_ID, image_message)


# アラーム起動
run_alarm()

send_image_and_message()

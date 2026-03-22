import requests

def send_line(msg):
    """
    LINE Notifyで通知を送る

    事前にトークン取得が必要
    """

    url = "https://notify-api.line.me/api/notify"
    token = "YOUR_TOKEN"

    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": msg}

    requests.post(url, headers=headers, data=data)

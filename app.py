from flask import Flask, redirect, request, session
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

OAUTH_URL = "https://discord.com/api/oauth2/authorize"
TOKEN_URL = "https://discord.com/api/oauth2/token"
USER_URL = "https://discord.com/api/users/@me"
JOIN_URL = "https://discord.com/api/guilds/{GUILD_ID}/members/{USER_ID}"  # 使用しないなら無視でOK

# ログインリンク
@app.route("/")
def home():
    return f'''
        <a href="{OAUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify">Discordでログイン</a>
    '''

# コールバック
@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    token = requests.post(TOKEN_URL, data=data, headers=headers).json()
    
    access_token = token["access_token"]

    # ユーザー情報取得
    user = requests.get(USER_URL, headers={"Authorization": f"Bearer {access_token}"}).json()
    session["user"] = user
    return f"ログイン完了！<br>ID: {user['id']}<br>名前: {user['username']}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

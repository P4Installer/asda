import requests
import os
import uuid
from flask import Flask, Response, render_template_string, request

app = Flask(__name__)

# Render выдает адрес автоматически, но нам нужен HTTPS для iOS
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>P4tweaks</title>
    <style>
        :root {
            --primary-color: #0071e3;
            --bg-color: #000000;
            --card-bg: rgba(28, 28, 30, 0.8);
            --text-main: #ffffff;
            --text-secondary: #a1a1a6;
            --divider: rgba(255, 255, 255, 0.1);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 0% 0%, #1d1d1f 0%, transparent 50%),
                radial-gradient(circle at 100% 100%, #002d5a 0%, transparent 50%);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            color: var(--text-main);
        }

        .container { 
            width: 100%; 
            max-width: 400px;
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header { text-align: left; margin-bottom: 30px; padding-left: 10px; }
        .header h1 { font-size: 34px; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
        .header p { color: var(--text-secondary); font-size: 15px; margin: 5px 0 0; }

        .section-title { 
            font-size: 13px; 
            text-transform: uppercase; 
            color: var(--text-secondary); 
            margin: 20px 0 8px 15px; 
            letter-spacing: 0.5px;
        }

        .card {
            background-color: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 20px;
            border: 1px solid var(--divider);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        .row {
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 0.5px solid var(--divider);
            text-decoration: none;
            color: var(--text-main);
            transition: background 0.2s;
        }
        .row:last-child { border-bottom: none; }
        .row:active { background-color: rgba(255,255,255,0.05); }

        .row-label { font-size: 17px; font-weight: 500; }
        .row-value { color: var(--primary-color); font-size: 17px; }

        .btn-install {
            background-color: var(--primary-color);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            border: none;
            cursor: pointer;
            transition: transform 0.1s;
        }
        .btn-install:active { transform: scale(0.95); }

        .icon {
            width: 29px;
            height: 29px;
            border-radius: 7px;
            margin-right: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>P4tweaks</h1>
            <p>Tweaks and apps</p>
        </div>

        <div class="section-title">Приложения и ipa</div>
        <div class="card">
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: linear-gradient(135deg, #5856d6, #3533a3);">E</div>
                    <span class="row-label">ESign Installer</span>
                </div>
                <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_esign">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: linear-gradient(135deg, #ff9500, #ff5e00);">K</div>
                    <span class="row-label">Ksign</span>
                </div>
                <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_ksign">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: linear-gradient(135deg, #340059, #200036);">P</div>
                    <span class="row-label">PureKFD(IPA)</span>
                </div>
                <a href="https://github.com/P4Installer/asda/raw/refs/heads/main/PureKFD.ipa">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: linear-gradient(135deg, #44bd48, #2d8a30);">G</div>
                    <span class="row-label">Gbox</span>
                </div>
                <a href="https://gbox.run/?id=01a1529a3237905cab97cd1034b6be16">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: linear-gradient(135deg, #602391, #401861);">S</div>
                    <span class="row-label">SideStore(IPA)</span>
                </div>
                <a href="https://github.com/SideStore/SideStore/releases/download/nightly/SideStore.ipa">
                    <button class="btn-install">Get</button>
                </a>
            </div>

            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: linear-gradient(135deg, #2c8a32, #096e0f);">M</div>
                    <span class="row-label">Minecraft(IPA)</span>
                </div>
                <a href="https://file.ipaomtk.com/Minecraft/Minecraft-v1.21.131-IPAOMTK.COM.ipa">
                    <button class="btn-install">Get</button>
                </a>
            </div>
        </div>

        <div class="section-title">Профили</div>
        <div class="card">
            <a href="https://P4Installer.github.io/P4Installer.mobileconfig" class="row">
                <span class="row-label">Приложение P4tweaks</span>
                <span class="row-value">Скачать</span>
            </a>
            <a href="https://raw.githubusercontent.com/P4Installer/asda/main/proxyapplejr.mobileconfig" class="row">
                <span class="row-label">proxy applejr.net</span>
                <span class="row-value">Скачать</span>
            </a>
            <a href="https://app.theappbox.ru/appbox_app.mobileconfig" class="row">
                <span class="row-label">AppBox</span>
                <span class="row-value">Скачать</span>
            </a>
        </div>

        <div class="section-title">Сертификаты</div>
        <div class="card">
            <a href="https://raw.githubusercontent.com/P4Installer/asda/main/PowerChinaInternationalGroupLimited.zip" class="row">
                <span class="row-label">PowerChina</span>
                <span class="row-value">Скачать</span>
            </a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Мы используем HTTPS версию URL для манифеста, это критично!
    current_url = request.url_root.replace('http://', 'https://')
    return render_template_string(HTML_TEMPLATE, base_url=current_url.strip('/'))

@app.route('/install-proxy_esign')
def install_proxy_esign():
    remote_manifest_url = "https://applejr.net/post/esignpwerchina.plist"
    try:
        response = requests.get(remote_manifest_url)
        content = response.text
        return Response(content, mimetype='text/xml')
    except Exception as e:
        return f"Ошибка загрузки манифеста: {e}"

@app.route('/install-proxy_ksign')
def install_proxy_ksign():
    remote_manifest_url = "https://applejr.net/post/ksignpower.plist"
    try:
        response = requests.get(remote_manifest_url)
        content = response.text
        return Response(content, mimetype='text/xml')
    except Exception as e:
        return f"Ошибка загрузки манифеста: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




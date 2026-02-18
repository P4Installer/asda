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
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>iOS 18 Control Hub</title>
    <style>
        :root {
            --ios-bg: #000000;
            --ios-card: #1c1c1e;
            --ios-blue: #0a84ff;
            --ios-green: #30d158;
            --ios-text: #ffffff;
            --ios-secondary: #8e8e93;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--ios-bg);
            color: var(--ios-text);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container { width: 100%; max-width: 400px; }
        .header { text-align: left; margin-bottom: 30px; padding-left: 10px; }
        .header h1 { font-size: 34px; font-weight: 700; margin: 0; }
        .header p { color: var(--ios-secondary); font-size: 15px; }

        .section-title { 
            font-size: 13px; 
            text-transform: uppercase; 
            color: var(--ios-secondary); 
            margin: 20px 0 8px 15px; 
        }

        .card {
            background-color: var(--ios-card);
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .row {
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 0.5px solid #38383a;
            text-decoration: none;
            color: var(--ios-text);
            transition: background 0.2s;
        }
        .row:last-child { border-bottom: none; }
        .row:active { background-color: #2c2c2e; }

        .row-label { font-size: 17px; }
        .row-value { color: var(--ios-blue); font-size: 17px; }

        .btn-install {
            background-color: var(--ios-blue);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            border: none;
            cursor: pointer;
        }

        .icon {
            width: 29px;
            height: 29px;
            border-radius: 7px;
            margin-right: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Утилиты</h1>
            <p>iOS 18 Developer Hub</p>
        </div>

        <div class="section-title">Магазины приложений (No PC)</div>
        <div class="card">
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: #5856d6;">E</div>
                    <span class="row-label">ESign Installer</span>
                </div>
                <a href="itms-services://?action=download-manifest&url={{ url }}/install-proxy">
                    <button class="btn-install">Установить</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: #ff9500;">S</div>
                    <span class="row-label">Scarlet</span>
                </div>
                <button class="btn-install">Загрузить</button>
            </div>
        </div>

        <div class="section-title">Системные твики (Профили)</div>
        <div class="card">
            <a href="/download-ota?ver=17.0" class="row">
                <span class="row-label">Откат на iOS 17 (Визуальный)</span>
                <span class="row-value">Скачать</span>
            </a>
            <a href="/download-ota?ver=block" class="row">
                <span class="row-label">Блокировка обновлений</span>
                <span class="row-value">tvOS</span>
            </a>
        </div>

        <div class="section-title">Устройство</div>
        <div class="card">
            <div class="row">
                <span class="row-label">Статус USB</span>
                <span class="row-value" style="color: var(--ios-green);">Подключено</span>
            </div>
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

@app.route('/install-proxy')
def install_proxy():
    # Ссылка на оригинальный манифест другого сайта
    remote_manifest_url = "https://applejr.net/post/Esign_Forevermark.plist"
    
    try:
        # 1. Скачиваем манифест с другого сайта
        response = requests.get(remote_manifest_url)
        content = response.text
        
        # 2. Если в чужом манифесте относительные пути, заменяем их на полные
        # (необязательно, если там уже прямая ссылка на .ipa)
        
        # 3. Отдаем его как свой
        return Response(content, mimetype='text/xml')
    except Exception as e:
        return f"Ошибка загрузки манифеста: {e}"

@app.route('/download-ota')
def download_ota():
    ver = request.args.get('ver', '17.0')
    
    # Генерируем уникальные ID для каждой установки
    root_uuid = str(uuid.uuid4())
    payload_uuid = str(uuid.uuid4())
    
    # Важно: PayloadIdentifier должен быть уникальным!
    profile = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>PayloadContent</key>
        <array>
            <dict>
                <key>PayloadDisplayName</key>
                <string>Tweak {ver}</string>
                <key>PayloadType</key>
                <string>com.apple.softwareupdate</string>
                <key>PayloadIdentifier</key>
                <string>com.p4.tweak.content.{payload_uuid}</string> 
                <key>PayloadUUID</key>
                <string>{payload_uuid}</string>
                <key>PayloadVersion</key>
                <integer>1</integer>
                <key>TargetVersion</key>
                <string>{ver}</string>
            </dict>
        </array>
        <key>PayloadDisplayName</key>
        <string>P4 Tweak Hub</string>
        <key>PayloadIdentifier</key>
        <string>com.p4.tweak.root.{root_uuid}</string> 
        <key>PayloadType</key>
        <string>Configuration</string>
        <key>PayloadUUID</key>
        <string>{root_uuid}</string>
        <key>PayloadVersion</key>
        <integer>1</integer>
    </dict>
    </plist>"""
    return Response(profile, mimetype='application/x-apple-aspen-config')
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)



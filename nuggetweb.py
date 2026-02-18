import uuid
from flask import Flask, Response, render_template_string, request

app = Flask(__name__)

# Настройки твоего сервера (замени на свой домен/IP с https)
BASE_URL = "https://your-domain.com" 

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
                <a href="itms-services://?action=download-manifest&amp;url=https://applejr.net/post/Esign_Forevermark.plist">
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
    return render_template_string(HTML_TEMPLATE, base_url=BASE_URL)

@app.route('/manifest.plist')
def manifest():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>items</key>
        <array>
            <dict>
                <key>assets</key>
                <array>
                    <dict>
                        <key>kind</key>
                        <string>software-package</string>
                        <key>url</key>
                        <string>{BASE_URL}/static/esign.ipa</string>
                    </dict>
                </array>
                <key>metadata</key>
                <dict>
                    <key>bundle-identifier</key>
                    <string>com.esign.client</string>
                    <key>bundle-version</key>
                    <string>1.0</string>
                    <key>kind</key>
                    <string>software</string>
                    <key>title</key>
                    <string>ESign</string>
                </dict>
            </dict>
        </array>
    </dict>
    </plist>"""
    return Response(xml, mimetype='application/xml')

@app.route('/download-ota')
def download_ota():
    ver = request.args.get('ver', '17.0')
    profile_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
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
                <key>PayloadUUID</key>
                <string>{str(uuid.uuid4())}</string>
                <key>PayloadVersion</key>
                <integer>1</integer>
                <key>TargetVersion</key>
                <string>{ver}</string>
            </dict>
        </array>
        <key>PayloadDisplayName</key>
        <string>iOS 18 Tweak Hub</string>
        <key>PayloadIdentifier</key>
        <string>com.tweak.hub</string>
        <key>PayloadType</key>
        <string>Configuration</string>
        <key>PayloadUUID</key>
        <string>{str(uuid.uuid4())}</string>
        <key>PayloadVersion</key>
        <integer>1</integer>
    </dict>
    </plist>"""
    return Response(profile_xml, mimetype='application/x-apple-aspen-config', 
                    headers={"Content-disposition": f"attachment; filename={ver}.mobileconfig"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
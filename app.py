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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>P4tweaks — Store</title>
    <style>
        :root {
            --primary-color: #007AFF;
            --bg-dark: #000000;
            --card-bg: rgba(28, 28, 30, 0.7);
            --text-main: #FFFFFF;
            --text-secondary: #8E8E93;
            --divider: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.15);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", sans-serif;
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 50% -10%, #1c1c1e 0%, transparent 60%),
                radial-gradient(circle at 0% 100%, #001d3d 0%, transparent 40%);
            margin: 0;
            padding: env(safe-area-inset-top) 16px env(safe-area-inset-bottom);
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            color: var(--text-main);
            -webkit-font-smoothing: antialiased;
        }

        .container { 
            width: 100%; 
            max-width: 414px;
            animation: slideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header { 
            text-align: left; 
            margin: 40px 0 20px 10px; 
        }
        .header h1 { 
            font-size: 34px; 
            font-weight: 800; 
            margin: 0; 
            letter-spacing: -1px; 
        }
        .header p { 
            color: var(--text-secondary); 
            font-size: 17px; 
            margin: 4px 0 0; 
            font-weight: 400;
        }

        .section-title { 
            font-size: 14px; 
            text-transform: uppercase; 
            color: var(--text-secondary); 
            margin: 25px 0 8px 16px; 
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        .card {
            background-color: var(--card-bg);
            backdrop-filter: blur(25px) saturate(180%);
            -webkit-backdrop-filter: blur(25px) saturate(180%);
            border-radius: 22px;
            overflow: hidden;
            border: 0.5px solid var(--glass-border);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }

        .row {
            padding: 14px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 0.5px solid var(--divider);
            text-decoration: none;
            color: var(--text-main);
            transition: background 0.2s;
        }
        .row:last-child { border-bottom: none; }
        .row:active { background-color: rgba(255,255,255,0.1); }

        .row-left {
            display: flex;
            align-items: center;
        }

        .row-label { 
            font-size: 17px; 
            font-weight: 500; 
            letter-spacing: -0.2px;
        }

        .row-value { 
            color: var(--primary-color); 
            font-size: 16px; 
            font-weight: 500;
        }

        .btn-install {
            background: rgba(255,255,255,0.1);
            color: var(--primary-color);
            padding: 6px 18px;
            border-radius: 100px;
            font-weight: 700;
            font-size: 14px;
            border: none;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.2s;
        }
        
        .row:active .btn-install {
            background-color: var(--primary-color);
            color: white;
        }

        .icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            margin-right: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 800;
            color: white;
            position: relative;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        /* Глянец на иконках */
        .icon::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
            border-radius: 8px;
        }

        .footer {
            margin: 40px 0 20px;
            font-size: 12px;
            color: #424245;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>P4tweaks</h1>
            <p>Библиотека приложений</p>
        </div>

        <div class="section-title">Приложения и ipa</div>
        <div class="card">
            <div class="row">
                <div class="row-left">
                    <div class="icon" style="background: linear-gradient(135deg, #5856d6, #3533a3);">E</div>
                    <span class="row-label">ESign Installer</span>
                </div>
                <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_esign">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div class="row-left">
                    <div class="icon" style="background: linear-gradient(135deg, #ff9500, #ff5e00);">K</div>
                    <span class="row-label">Ksign</span>
                </div>
                <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_ksign">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div class="row-left">
                    <div class="icon" style="background: linear-gradient(135deg, #340059, #200036);">P</div>
                    <span class="row-label">PureKFD</span>
                </div>
                <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_purekfd">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div class="row-left">
                    <div class="icon" style="background: linear-gradient(135deg, #44bd48, #2d8a30);">G</div>
                    <span class="row-label">Gbox</span>
                </div>
                <a href="https://gbox.run/?id=01a1529a3237905cab97cd1034b6be16">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div class="row-left">
                    <div class="icon" style="background: linear-gradient(135deg, #602391, #401861);">S</div>
                    <span class="row-label">SideStore (IPA)</span>
                </div>
                <a href="https://github.com/SideStore/SideStore/releases/download/nightly/SideStore.ipa">
                    <button class="btn-install">Get</button>
                </a>
            </div>
            <div class="row">
                <div class="row-left">
                    <div class="icon" style="background: linear-gradient(135deg, #2c8a32, #096e0f);">M</div>
                    <span class="row-label">Minecraft (IPA)</span>
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
                <span class="row-label">Proxy applejr.net</span>
                <span class="row-value">Скачать</span>
            </a>
            <a href="https://app.theappbox.ru/appbox_app.mobileconfig" class="row">
                <span class="row-label">AppBox Config</span>
                <span class="row-value">Скачать</span>
            </a>
        </div>

        <div class="section-title">Сертификаты</div>
        <div class="card">
            <a href="https://raw.githubusercontent.com/P4Installer/asda/main/PowerChinaInternationalGroupLimited.zip" class="row">
                <span class="row-label">PowerChina Group</span>
                <span class="row-value">Скачать</span>
            </a>
        </div>

        <div class="footer">© 2026 P4Installer. Design by SF Pro.</div>
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

@app.route('/install-proxy_purekfd')
def install_proxy_esign():
    remote_manifest_url = "https://raw.githubusercontent.com/P4Installer/asda/main/test.plist"
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







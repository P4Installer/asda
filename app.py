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
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
    <title>P4tweaks</title>
    <style>
        :root {
            --ios-bg: #000000;
            --ios-card: #1c1c1e;
            --ios-blue: #0a84ff;
            --ios-secondary: #8e8e93;
            --ios-divider: rgba(255, 255, 255, 0.12);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--ios-bg);
            color: white;
            margin: 0;
            padding: env(safe-area-inset-top) 16px 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            -webkit-font-smoothing: antialiased;
        }

        .container { 
            width: 100%; 
            max-width: 420px; 
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header { 
            margin: 40px 0 24px 8px; 
        }

        .header h1 { 
            font-size: 34px; 
            font-weight: 800; 
            margin: 0; 
            letter-spacing: -0.5px;
        }

        .header p { 
            color: var(--ios-secondary); 
            font-size: 17px; 
            margin: 4px 0 0;
        }

        .section-title { 
            font-size: 13px; 
            text-transform: uppercase; 
            color: var(--ios-secondary); 
            margin: 24px 0 8px 16px; 
            letter-spacing: 0.2px;
        }

        .card {
            background-color: var(--ios-card);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        .row {
            padding: 11px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 44px;
            text-decoration: none;
            color: white;
            border-bottom: 0.5px solid var(--ios-divider);
            transition: background 0.2s ease;
        }

        .row:last-child { border-bottom: none; }
        
        /* Эффект нажатия как в iOS */
        .row:active { background-color: #3a3a3c; }

        .row-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .row-label { 
            font-size: 17px; 
            font-weight: 400;
        }

        .row-value { 
            color: var(--ios-blue); 
            font-size: 17px;
            padding-right: 4px;
        }

        .btn-install {
            background-color: #2c2c2e;
            color: var(--ios-blue);
            padding: 6px 14px;
            border-radius: 18px;
            font-weight: 700;
            font-size: 13px;
            border: none;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.2s ease;
        }

        .btn-install:active {
            transform: scale(0.92);
            background-color: #3a3a3c;
        }

        .icon {
            width: 30px;
            height: 30px;
            border-radius: 7px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 600;
            color: white;
            flex-shrink: 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }

        /* Шеврон (стрелочка) для ссылок */
        .chevron::after {
            content: '›';
            color: #555558;
            font-size: 20px;
            margin-left: 8px;
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
                    <span class="row-label">PureKFD (IPA)</span>
                </div>
                <a href="https://github.com/P4Installer/asda/raw/refs/heads/main/PureKFD.ipa">
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
        </div>

        <div class="section-title">Профили конфигурации</div>
        <div class="card">
            <a href="https://P4Installer.github.io/P4Installer.mobileconfig" class="row">
                <span class="row-label">Приложение P4tweaks</span>
                <div style="display: flex; align-items: center;">
                    <span class="row-value">Скачать</span>
                    <span class="chevron"></span>
                </div>
            </a>
            <a href="https://raw.githubusercontent.com/P4Installer/asda/main/proxyapplejr.mobileconfig" class="row">
                <span class="row-label">Proxy applejr.net</span>
                <div style="display: flex; align-items: center;">
                    <span class="row-value">Скачать</span>
                    <span class="chevron"></span>
                </div>
            </a>
            <a href="https://app.theappbox.ru/appbox_app.mobileconfig" class="row">
                <span class="row-label">AppBox Profile</span>
                <div style="display: flex; align-items: center;">
                    <span class="row-value">Скачать</span>
                    <span class="chevron"></span>
                </div>
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

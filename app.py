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
    <title>P4tweaks</title>
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
            <h1>P4tweaks</h1>
            <p>Tweaks and apps</p>
        </div>

        <div class="section-title">Приложения и ipa</div>
        <div class="card">
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: #5856d6;">E</div>
                    <span class="row-label">ESign Installer</span>
                </div>
                <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_esign">
                    <button class="btn-install">Установить</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: #ff9500;">K</div>
                    <span class="row-label">Ksign</span>
                </div>
                <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_ksign">
                    <button class="btn-install">Установить</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: #340059;">P</div>
                    <span class="row-label">PureKFD(ios 15.0-17.0)</span>
                </div>
                <a href="https://ios-tweak-hub.onrender.com/install-proxy_PureKFD">
                    <button class="btn-install">IPA</button>
                </a>
            </div>
            <div class="row">
                <div style="display: flex; align-items: center;">
                    <div class="icon" style="background: #44bd48;">g</div>
                    <span class="row-label">Gbox</span>
                </div>
                <a href="https://gbox.run/?id=01a1529a3237905cab97cd1034b6be16">
                    <button class="btn-install">На сайт gbox</button>
                </a>
            </div>
        </div>



        <div class="section-title">Профили</div>
        <div class="card">
            <a href="https://ios-tweak-hub.onrender.com/install-proxy_p4installer" class="row">
                <span class="row-label">Приложение P4tweaks</span>
                <span class="row-value">Скачать</span>
            </a>
            <a href="https://ios-tweak-hub.onrender.com/install-proxy_applejr" class="row">
                <span class="row-label">proxy applejr.net</span>
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
    # Ссылка на оригинальный манифест другого сайта
    remote_manifest_url = "https://applejr.net/post/esignpwerchina.plist"
    
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

@app.route('/install-proxy_ksign')
def install_proxy_ksign():
    # Ссылка на оригинальный манифест другого сайта
    remote_manifest_url = "https://applejr.net/post/ksignpower.plist"
    
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

@app.route('/install-proxy_applejr')
def install_proxy_applejr():
    # Ссылка на оригинальный манифест другого сайта
    remote_manifest_url = "https://raw.githubusercontent.com/P4Installer/asda/main/proxyapplejr.mobileconfig"
    
    try:
        # 1. Скачиваем манифест с другого сайта
        response = requests.get(remote_manifest_url)
        content = response.text
        
        # 2. Если в чужом манифесте относительные пути, заменяем их на полные
        # (необязательно, если там уже прямая ссылка на .ipa)
        
        # 3. Отдаем его как свой
        return Response(content, mimetype='text/xml')
    except Exception as e:
        return f"Ошибка загрузки proxyapplejr: {e}"

@app.route('/install-proxy_p4installer')
def install_proxy_applejr():
    # Ссылка на оригинальный манифест другого сайта
    remote_manifest_url = "https://raw.githubusercontent.com/P4Installer/asda/main/P4installer.mobileconfig"
    
    try:
        # 1. Скачиваем манифест с другого сайта
        response = requests.get(remote_manifest_url)
        content = response.text
        
        # 2. Если в чужом манифесте относительные пути, заменяем их на полные
        # (необязательно, если там уже прямая ссылка на .ipa)
        
        # 3. Отдаем его как свой
        return Response(content, mimetype='text/xml')
    except Exception as e:
        return f"Ошибка загрузки P4installer: {e}"

@app.route('/install-proxy_purekfd')
def install_proxy_applejr():
    # Ссылка на оригинальный манифест другого сайта
    remote_manifest_url = "https://raw.githubusercontent.com/P4Installer/asda/main/PureKFD.ipa"
    
    try:
        # 1. Скачиваем манифест с другого сайта
        response = requests.get(remote_manifest_url)
        content = response.text
        
        # 2. Если в чужом манифесте относительные пути, заменяем их на полные
        # (необязательно, если там уже прямая ссылка на .ipa)
        
        # 3. Отдаем его как свой
        return Response(content, mimetype='text/xml')
    except Exception as e:
        return f"Ошибка загрузки PureKFD: {e}"



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)














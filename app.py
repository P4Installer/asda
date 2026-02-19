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
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 0% 0%, #1d1d1f 0%, transparent 50%),
                radial-gradient(circle at 100% 100%, #002d5a 0%, transparent 50%);
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: var(--text-main);
            overflow: hidden;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .container {
            text-align: center;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 40px 30px;
            border-radius: 32px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            max-width: 380px;
            width: 85%;
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeInUp 0.8s ease-out;
        }

        .app-icon {
            width: 90px;
            height: 90px;
            background: linear-gradient(135deg, #3a3a3c 0%, #000000 100%);
            border-radius: 20px;
            margin: 0 auto 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 36px;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }

        .app-icon::after {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            animation: shine 4s infinite;
        }

        @keyframes shine {
            0% { transform: translateX(-100%) rotate(45deg); }
            20%, 100% { transform: translateX(100%) rotate(45deg); }
        }

        h1 { 
            font-size: 28px; 
            margin: 0 0 10px; 
            font-weight: 700; 
            letter-spacing: -0.5px;
        }

        p { 
            color: var(--text-secondary); 
            margin-bottom: 32px; 
            line-height: 1.4; 
            font-size: 16px; 
            padding: 0 10px;
        }

        .btn-install {
            background-color: var(--primary-color);
            color: white;
            text-decoration: none;
            padding: 16px 0;
            width: 100%;
            border-radius: 16px;
            font-weight: 600;
            display: block;
            transition: all 0.2s ease;
            font-size: 17px;
            box-shadow: 0 4px 15px rgba(0, 113, 227, 0.3);
            border: none;
            cursor: pointer;
        }

        .btn-install:active {
            transform: scale(0.97);
            filter: brightness(1.1);
        }

        .instructions {
            margin-top: 32px;
            font-size: 14px;
            text-align: left;
            color: var(--text-secondary);
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 18px;
        }

        .instructions strong {
            display: block;
            margin-bottom: 12px;
            color: #fff;
            font-size: 15px;
        }

        .instructions ol { 
            padding-left: 18px; 
            margin: 0;
        }

        .instructions li { 
            margin-bottom: 10px; 
        }

        b { color: var(--primary-color); }
        
        a { text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="app-icon">P4</div>
        <h1>P4tweaks</h1>
        <p>Установите профиль конфигурации для доступа к приложениям.</p>
        
        <a href="https://P4Installer.github.io/P4Installer.mobileconfig" class="btn-install">Установить профиль</a>

        <div class="instructions">
            <strong>Инструкция:</strong>
            <ol>
                <li>Нажмите синюю кнопку</li>
                <li>Выберите <b>Разрешить</b> в Safari</li>
                <li>Откройте <b>Настройки</b> профиля</li>
                <li>Нажмите <b>Установить</b></li>
            </ol>
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


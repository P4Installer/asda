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
    <title>P4tweaks — Sileo Style</title>
    <style>
        :root {
            --sileo-accent: #2fb5d2;
            --sileo-gradient: linear-gradient(135deg, #32e1f3 0%, #2fb5d2 100%);
            --bg-dark: #0e0e0e;
            --card-bg: #1c1c1e;
            --text-main: #ffffff;
            --text-secondary: #8e8e93;
            --divider: #2c2c2e;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
            background-color: var(--bg-dark);
            margin: 0;
            padding: env(safe-area-inset-top) 0 env(safe-area-inset-bottom);
            color: var(--text-main);
            -webkit-tap-highlight-color: transparent;
        }

        /* Заголовок в стиле Sileo */
        .nav-header {
            padding: 20px 20px 10px;
            position: sticky;
            top: 0;
            background: rgba(14, 14, 14, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            z-index: 100;
        }

        .nav-header h1 {
            font-size: 34px;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .search-bar {
            background: #2c2c2e;
            border-radius: 10px;
            padding: 8px 12px;
            margin: 15px 0;
            color: var(--text-secondary);
            font-size: 17px;
            display: flex;
            align-items: center;
        }

        .container {
            padding: 0 16px;
            max-width: 500px;
            margin: 0 auto;
        }

        .section-title {
            font-size: 22px;
            font-weight: 700;
            margin: 25px 0 15px 4px;
        }

        /* Карточки приложений в стиле Sileo */
        .package-card {
            background: var(--card-bg);
            border-radius: 14px;
            padding: 12px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s, background 0.2s;
        }

        .package-card:active {
            transform: scale(0.97);
            background: #2c2c2e;
        }

        .icon {
            width: 58px;
            height: 58px;
            border-radius: 13px;
            margin-right: 15px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 700;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .package-info {
            flex-grow: 1;
            min-width: 0;
        }

        .package-name {
            font-size: 17px;
            font-weight: 600;
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .package-desc {
            font-size: 14px;
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Кнопка "GET" как в Sileo */
        .get-button {
            background: #2c2c2e;
            color: var(--sileo-accent);
            padding: 6px 20px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
            border: none;
            margin-left: 10px;
            min-width: 70px;
            text-align: center;
            transition: all 0.2s;
        }

        .package-card:active .get-button {
            background: var(--sileo-accent);
            color: white;
        }

        /* Список профилей (компактный вид) */
        .list-group {
            background: var(--card-bg);
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .list-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 16px;
            border-bottom: 0.5px solid var(--divider);
            text-decoration: none;
            color: inherit;
        }

        .list-item:last-child { border-bottom: none; }
        .list-item:active { background: #2c2c2e; }

        .list-label { font-size: 17px; font-weight: 400; }
        .list-action { color: var(--sileo-accent); font-weight: 500; }

        .footer {
            text-align: center;
            padding: 40px 0;
            color: var(--text-secondary);
            font-size: 13px;
        }

        .sileo-tab-bar {
            position: fixed;
            bottom: 0;
            width: 100%;
            height: 60px;
            background: rgba(28, 28, 30, 0.95);
            backdrop-filter: blur(10px);
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 0.5px solid var(--divider);
        }

        .tab-item { color: var(--sileo-accent); font-size: 11px; text-align: center; text-decoration: none; opacity: 0.6; }
        .tab-item.active { opacity: 1; }
    </style>
</head>
<body>

    <div class="nav-header">
        <h1>P4tweaks</h1>
        <div class="search-bar">🔍 Поиск пакетов...</div>
    </div>

    <div class="container">
        
        <div class="section-title">Новое</div>

        <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_esign" class="package-card">
            <div class="icon" style="background: linear-gradient(135deg, #5856d6, #3533a3);">E</div>
            <div class="package-info">
                <div class="package-name">ESign Installer</div>
                <div class="package-desc">Установщик с поддержкой прокси</div>
            </div>
            <div class="get-button">GET</div>
        </a>

        <a href="itms-services://?action=download-manifest&url=https://ios-tweak-hub.onrender.com/install-proxy_ksign" class="package-card">
            <div class="icon" style="background: linear-gradient(135deg, #ff9500, #ff5e00);">K</div>
            <div class="package-info">
                <div class="package-name">Ksign</div>
                <div class="package-desc">Подпись и установка приложений</div>
            </div>
            <div class="get-button">GET</div>
        </a>

        <a href="https://github.com/P4Installer/asda/raw/refs/heads/main/PureKFD.ipa" class="package-card">
            <div class="icon" style="background: linear-gradient(135deg, #340059, #200036);">P</div>
            <div class="package-info">
                <div class="package-name">PureKFD (IPA)</div>
                <div class="package-desc">Инструменты кастомизации</div>
            </div>
            <div class="get-button">GET</div>
        </a>

        <a href="https://file.ipaomtk.com/Minecraft/Minecraft-v1.21.131-IPAOMTK.COM.ipa" class="package-card">
            <div class="icon" style="background: linear-gradient(135deg, #2c8a32, #096e0f);">M</div>
            <div class="package-info">
                <div class="package-name">Minecraft</div>
                <div class="package-desc">Версия 1.21.131</div>
            </div>
            <div class="get-button">GET</div>
        </a>

        <div class="section-title">Конфигурации</div>
        <div class="list-group">
            <a href="https://P4Installer.github.io/P4Installer.mobileconfig" class="list-item">
                <span class="list-label">Приложение P4tweaks</span>
                <span class="list-action">Установить</span>
            </a>
            <a href="https://raw.githubusercontent.com/P4Installer/asda/main/proxyapplejr.mobileconfig" class="list-item">
                <span class="list-label">Proxy applejr.net</span>
                <span class="list-action">Добавить</span>
            </a>
            <a href="https://app.theappbox.ru/appbox_app.mobileconfig" class="list-item">
                <span class="list-label">AppBox Config</span>
                <span class="list-action">Скачать</span>
            </a>
        </div>

        <div class="section-title">Сертификаты</div>
        <div class="list-group">
            <a href="https://raw.githubusercontent.com/P4Installer/asda/main/PowerChinaInternationalGroupLimited.zip" class="list-item">
                <span class="list-label">PowerChina Group Limited</span>
                <span class="list-action">ZIP</span>
            </a>
        </div>

        <div class="footer">
            Обновлено: 2026<br>
            P4Installer Repo — Developed for Sileo
        </div>
    </div>

    <div class="sileo-tab-bar">
        <div class="tab-item active">Featured</div>
        <div class="tab-item">News</div>
        <div class="tab-item">Sources</div>
        <div class="tab-item">Packages</div>
        <div class="tab-item">Search</div>
    </div>

    <div style="height: 80px;"></div> </body>
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
def install_proxy_purekfd():
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










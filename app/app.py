from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from controllers.auth_controller import AuthController
from views.templates import render_main_page, render_template, render_message
import os


class AuthHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = AuthController()
        super().__init__(*args, **kwargs)

    def _send_response(self, content, status_code=200):
        """Отправка HTTP ответа"""
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def _serve_static(self, filepath):
        """Обработка статических файлов"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()

            if filepath.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif filepath.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')

            self.send_response(200)
            self.end_headers()
            self.wfile.write(content)
        except:
            self.send_error(404, "File not found")

    def do_GET(self):
        """Обработка GET запросов"""
        parsed_path = urlparse(self.path)

        # Статические файлы
        if parsed_path.path.startswith('/static/'):
            filepath = parsed_path.path[1:]
            if os.path.exists(filepath):
                self._serve_static(filepath)
            else:
                self.send_error(404, "File not found")
            return

        # Основные маршруты
        if parsed_path.path == '/':
            content = render_main_page()
            self._send_response(content)

        elif parsed_path.path == '/register':
            form = self.controller.get_register_form()
            nav_links = [
                {"url": "/", "text": "На главную"},
                {"url": "/login", "text": "Уже есть аккаунт? Войти"}
            ]
            content = render_template("Регистрация", form, nav_links)
            self._send_response(content)

        elif parsed_path.path == '/login':
            form = self.controller.get_login_form()
            nav_links = [
                {"url": "/", "text": "На главную"},
                {"url": "/register", "text": "Нет аккаунта? Зарегистрироваться"}
            ]
            content = render_template("Вход в систему", form, nav_links)
            self._send_response(content)

        elif parsed_path.path == '/change-password':
            form = self.controller.get_change_password_form()
            nav_links = [
                {"url": "/", "text": "На главную"}
            ]
            content = render_template("Смена пароля", form, nav_links)
            self._send_response(content)

        else:
            self.send_error(404, "Страница не найдена")

    def do_POST(self):
        """Обработка POST запросов"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(post_data)

        parsed_path = urlparse(self.path)

        if parsed_path.path == '/register':
            username = data.get('username', [''])[0]
            email = data.get('email', [''])[0]
            password = data.get('password', [''])[0]

            result = self.controller.handle_register(username, email, password)
            message = render_message(result["message"], result["success"])
            content = render_template(result["title"], message, result["nav_links"])
            self._send_response(content)

        elif parsed_path.path == '/login':
            email = data.get('email', [''])[0]
            password = data.get('password', [''])[0]

            result = self.controller.handle_login(email, password)
            message = render_message(result["message"], result["success"])
            content = render_template(result["title"], message, result["nav_links"])
            self._send_response(content)

        elif parsed_path.path == '/change-password':
            email = data.get('email', [''])[0]
            old_password = data.get('old_password', [''])[0]
            new_password = data.get('new_password', [''])[0]

            result = self.controller.handle_change_password(email, old_password, new_password)
            message = render_message(result["message"], result["success"])
            content = render_template(result["title"], message, result["nav_links"])
            self._send_response(content)

        else:
            self.send_error(404, "Страница не найдена")

    def log_message(self, format, *args):
        """Отключение логов в консоль"""
        pass


def run_server():
    """Запуск веб-сервера"""
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, AuthHandler)
    print("Сервер запущен")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
from models.database import Database
from views.templates import render_template, render_form


class AuthController:
    def __init__(self):
        self.db = Database()

    def handle_register(self, username: str, email: str, password: str) -> dict:
        """Обработка регистрации пользователя"""
        success, message = self.db.add_user(username, email, password)

        return {
            "success": success,
            "message": message,
            "title": "Регистрация",
            "nav_links": [
                {"url": "/login", "text": "Войти в аккаунт"} if success else
                {"url": "/register", "text": "Попробовать снова"},
                {"url": "/", "text": "На главную"}
            ]
        }

    def handle_login(self, email: str, password: str) -> dict:
        """Обработка входа пользователя"""
        success, username = self.db.authenticate_user(email, password)

        return {
            "success": success,
            "message": f"Вход выполнен успешно! Добро пожаловать, {username}!" if success else "Неверный email или пароль!",
            "title": "Вход в систему",
            "username": username if success else None,
            "nav_links": [
                {"url": "/change-password", "text": "Сменить пароль"} if success else
                {"url": "/login", "text": "Попробовать снова"},
                {"url": "/register", "text": "Зарегистрироваться"} if not success else
                {"url": "/", "text": "На главную"}
            ]
        }

    def handle_change_password(self, email: str, old_password: str, new_password: str) -> dict:
        """Обработка смены пароля"""
        result = self.db.change_password(email, old_password, new_password)
        success = "успешно" in result.lower()

        return {
            "success": success,
            "message": result,
            "title": "Смена пароля",
            "nav_links": [
                {"url": "/login", "text": "Войти с новым паролем"} if success else
                {"url": "/change-password", "text": "Попробовать снова"},
                {"url": "/", "text": "На главную"}
            ]
        }

    def get_register_form(self) -> str:
        """Получение формы регистрации"""
        return render_form(
            action="/register",
            fields=[
                {"type": "text", "name": "username", "placeholder": "Имя пользователя"},
                {"type": "email", "name": "email", "placeholder": "Email"},
                {"type": "password", "name": "password", "placeholder": "Пароль"}
            ],
            button_text="Зарегистрироваться",
            title="Создание нового аккаунта"
        )

    def get_login_form(self) -> str:
        """Получение формы входа"""
        return render_form(
            action="/login",
            fields=[
                {"type": "email", "name": "email", "placeholder": "Email"},
                {"type": "password", "name": "password", "placeholder": "Пароль"}
            ],
            button_text="Войти",
            title="Вход в аккаунт"
        )

    def get_change_password_form(self) -> str:
        """Получение формы смены пароля"""
        return render_form(
            action="/change-password",
            fields=[
                {"type": "email", "name": "email", "placeholder": "Email"},
                {"type": "password", "name": "old_password", "placeholder": "Старый пароль"},
                {"type": "password", "name": "new_password", "placeholder": "Новый пароль"}
            ],
            button_text="Сменить пароль",
            title="Изменение пароля"
        )


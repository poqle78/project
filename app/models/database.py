import sqlite3
from typing import Optional, Tuple


class Database:
    def __init__(self, db_path: str = "database.db"):
        """Инициализация подключения к базе данных"""
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        """Создание таблиц, если они не существуют"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Добавление нового пользователя"""
        try:
            self.cursor.execute('''
                INSERT INTO users (username, email, password) 
                VALUES (?, ?, ?)
            ''', (username, email, password))
            self.connection.commit()
            return True, "Регистрация успешна!"
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return False, "Пользователь с таким именем уже существует"
            elif "email" in str(e):
                return False, "Пользователь с таким email уже существует"
            return False, "Ошибка регистрации"

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """Аутентификация пользователя по email и паролю"""
        self.cursor.execute(
            'SELECT username, password FROM users WHERE email = ?',
            (email,)
        )
        result = self.cursor.fetchone()

        if not result:
            return False, None

        stored_username, stored_password = result
        if password == stored_password:
            return True, stored_username
        return False, None

    def change_password(self, email: str, old_password: str, new_password: str) -> str:
        """Смена пароля пользователя"""
        # Проверка, что пароли разные
        if old_password == new_password:
            return "Новый пароль должен отличаться от старого!"

        # Проверка существования пользователя
        self.cursor.execute(
            'SELECT password FROM users WHERE email = ?',
            (email,)
        )
        result = self.cursor.fetchone()

        if not result:
            return "Пользователь не найден"

        stored_password = result[0]

        # Проверка старого пароля
        if old_password != stored_password:
            return "Неверный старый пароль"

        # Обновление пароля
        try:
            self.cursor.execute(
                'UPDATE users SET password = ? WHERE email = ?',
                (new_password, email)
            )
            self.connection.commit()
            return "Пароль успешно изменен!"
        except Exception as e:
            return f"Ошибка при изменении пароля: {str(e)}"

    def user_exists(self, email: str) -> bool:
        """Проверка существования пользователя по email"""
        self.cursor.execute(
            'SELECT 1 FROM users WHERE email = ?',
            (email,)
        )
        return self.cursor.fetchone() is not None

    def get_all_users(self) -> list:
        """Получение списка всех пользователей (для отладки)"""
        self.cursor.execute('SELECT username, email FROM users')
        return self.cursor.fetchall()

    def close(self):
        """Закрытие соединения с базой данных"""
        self.connection.close()

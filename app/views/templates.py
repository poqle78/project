def render_template(title: str, content: str, nav_links: list = None) -> str:
    """Рендеринг HTML страницы"""
    if nav_links is None:
        nav_links = []

    nav_html = '<div class="nav">' + ' | '.join(
        f'<a href="{link["url"]}">{link["text"]}</a>'
        for link in nav_links
    ) + '</div>' if nav_links else ''

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>{title}</h1>
        {nav_html}
        {content}
    </body>
    </html>
    """


def render_form(action: str, fields: list, button_text: str, title: str = "") -> str:
    """Рендеринг HTML формы"""
    form_html = f'<h2>{title}</h2><div class="form"><form method="POST" action="{action}">'
    for field in fields:
        form_html += f'<input type="{field["type"]}" name="{field["name"]}" placeholder="{field["placeholder"]}" required><br>'
    form_html += f'<button type="submit">{button_text}</button></form></div>'
    return form_html


def render_message(message: str, is_success: bool = True) -> str:
    """Рендеринг сообщения"""
    css_class = "success" if is_success else "error"
    return f'<p class="{css_class}">{message}</p>'


def render_main_page() -> str:
    """Рендеринг главной страницы"""
    nav_links = [
        {"url": "/register", "text": "Регистрация"},
        {"url": "/login", "text": "Вход"},
        {"url": "/change-password", "text": "Смена пароля"}
    ]

    return render_template(
        title="Система авторизации",
        content="<p>Добро пожаловать в систему авторизации!</p>",
        nav_links=nav_links
    )
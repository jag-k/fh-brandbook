from lib import *


# MAIN

@route("/")
def main_page():
    headers = get_settings("headers")

    return template(
        "main",
        template_title=headers.get('main', "Молодёжный портал"),
        template_description=headers.get('description_main', ""),

        posts=get_json_list(Post),
        blocks=get_json_list(Block),
        categories=get_json_list(Category),
        news=get_json_list(News),

        about=get_settings("about"),
        main_settings=get_settings("main"),
    )


# NEWS

@route("/news")
def news_page():
    headers = get_settings("headers")

    return template(
        "news",
        template_title=headers.get('news', "Блог"),
        template_description=headers.get('description_news', ""),
        data=get_json_list(News),
    )


@route("/news/<id:int>")
def news_post_page(id: int):
    if exists(n for n in News if n.id == id):
        n = News[id]
        # category = n["category"]["id"]
        return template(
            "news_post",
            template_title=n.title + " | Блог",
            template_description=n.description,
            post=get_json(n),
            categories=get_json_list(Category),
        )
    else:
        redirect("/news", alert=Alert("Пост не найден."))


# ADMIN LOGIN

@route(ADMIN_LOGIN_ROUTE, method=GET_POST)
def login():
    alert = None
    if request.POST:
        h = hash_admin(request.forms.get("login"), request.forms.get("password"))
        if is_hash_admin(h):
            response.set_cookie(ADMIN_COOKIE_KEY, h, ADMIN_COOKIE_SECRET, max_age=604800, httponly=True)
            redirect_from = request.get_cookie("redirect", "/admin", ADMIN_COOKIE_SECRET)
            redirect(redirect_from)
        else:
            alert = Alert(
                "Вы ввели не правильный логин или пароль! Повторите снова",
                Alert.DANGER
            )
    if request.params.get("from"):
        response.set_cookie('redirect', request.params.get("from", ADMIN_LOGIN_ROUTE), ADMIN_COOKIE_SECRET)

    return template(join("admin", "login"),
                    template_title="Вход в админку",
                    alert=alert,
                    )


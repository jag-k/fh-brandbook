from html import unescape

from pony.converting import str2datetime

from lib import *


@admin_route("/")
def admin():
    return admin_temp(
        "create_user",
        awdad='awd',
        description="None",
    )


@admin_route("/main_page", GET_POST)
def admin_pages_main():
    if request.method == POST:
        par = dict(request.params)
        for filename in request.files:
            par[filename] = save_img(filename, "main_page", filename)

        for key, value in list(par.items()):
            if isinstance(value, bytes):
                del par[key]

        update_settings("main", par)
        redirect("/admin/main_page", alert=Alert("Главная страница успешно обновлена!"))

    data = get_settings("main")

    return admin_temp(
        "main",
        data=data
    )


@admin_route("/meta", GET_POST)
def admin_pages_meta():
    if request.method == POST:
        update_settings("meta", dict(request.params))
        redirect("/admin/meta", alert=Alert("Метатеги успешно сохранены!"))

    data = get_settings("meta")

    return admin_temp(
        "meta",
        data=data
    )


@admin_route("/socials", GET_POST)
def admin_pages_socials():
    if request.POST:
        with db_session:
            par = dict(request.params)
            for (key, value) in par.items():
                if PHONE_RE.match(value):
                    par[key] = '7' + ''.join(PHONE_RE.match(value).groups())
            update_settings("socials", par)
        return redirect("/admin/socials", alert=Alert("Социалки успешно сохранены!"))

    data = get_settings("socials")

    return admin_temp(
        "socials",
        data=data
    )


@admin_route("/about_me", GET_POST)
def admin_about_me():
    if request.method == POST:
        update_settings("about", dict(request.params))
        redirect("/admin/about_me", alert=Alert('Блок "Обо мне" изменен!'))

    data = get_settings("about")

    return admin_temp(
        "about_me",
        data=data
    )


# NEWS

@admin_route("/news")
def admin_new_news():
    return admin_temp(
        "news/index",
        data=get_json_list(News),
    )


@admin_route("/news/new", GET_POST)
def admin_new_news():
    if request.method == POST:
        params = dict(request.params)
        n = News(
            title=unescape(params["title"]),
            description=unescape(params["description"]),
            content=unescape(params["content"]),
            date=str2datetime(params["date"]),
            image="",
            hidden=bool(params.pop("published", False)),
        )
        commit()
        image = save_img("news_" + str(n.id), "news")
        n.image = image
        commit()

        redirect("/admin/news", alert=Alert("Вы создали новый пост в блоге!"))

    return admin_temp(
        "news/new",
        date=date.today().isoformat(),
        data={},
    )


@admin_route("/news/edit/<id:int>", GET_POST)
def admin_edit_news(id: int):
    n = News[id]
    if request.method == POST:
        params = dict(request.params)
        print("params", params)
        n.set(
            title=unescape(params["title"]),
            description=unescape(params["description"]),
            category=params.get("category"),
            content=unescape(params["content"]),
            date=str2datetime(params["date"]),
            hidden=bool(params.pop("published", False)),
        )

        commit()
        print(n.category)
        if request.files.get('image'):
            image = save_img("news_" + str(n.id), "news")
            n.image = image
            commit()

        redirect("/admin/news", alert=Alert("Вы отредактировали пост в блоге!"))

    return admin_temp(
        "news/new",
        date=date.today().isoformat(),
        data=get_json(n),
    )


@admin_route("/news/category", GET_POST)
def admin_new_news():
    if request.POST:
        c = Category(
            name=request.params.get('name'),
        )
        print(c)
        redirect(
            "/admin/news/category",
            alert=Alert("Вы успешно создали категорию!")
        )

    return admin_temp(
        "news/category",
        data=get_json_list(Category),
    )


@admin_route("/news/del/<id:int>")
def admin_new_news(id: int):
    News[id].delete()
    commit()
    redirect('/admin/news', alert=Alert("Пост успешно удалён!"))


@admin_route("/news/category/del/<id:int>")
def admin_new_news(id: int):
    Category[id].delete()
    commit()
    redirect('/admin/news/category', alert=Alert("Категория успешно удалена!"))


@admin_route("/news/category/edit/<id:int>", POST)
def admin_new_news(id: int):
    c = Category[id]
    c.set(
        name=request.params.get('name'),
    )
    print(c)
    redirect(
        "/admin/news/category",
        alert=Alert("Вы успешно отредактировали категорию!")
    )


@admin_route("/toggle_public_news/<id:int>")
def admin_edit_news(id):
    n = select(n for n in News if n.id == id).first()
    d = n.draft
    n.draft = not d
    redirect("/admin/news", alert=Alert("Вы %s новость!" % ('опубликовали' if d else 'скрыли')))


# HEADERS

@admin_route("/headers", GET_POST)
def admin_new_news():
    if request.POST:
        c = Header(
            name=request.params.get('name'),
            url=request.params.get('url'),
        )
        print(c)
        redirect(
            "/admin/headers",
            alert=Alert("Вы успешно создали ссылку в шапке!")
        )

    return admin_temp(
        "headers",
        data=get_json_list(Header),
    )


@admin_route("/headers/del/<id:int>")
def admin_new_news(id: int):
    Header[id].delete()
    commit()
    redirect('/admin/headers', alert=Alert("Ссылка успешно удалена из шапки!"))


@admin_route("/headers/edit/<id:int>", POST)
def admin_new_news(id: int):
    c = Header[id]
    c.set(
        name=request.params.get('name'),
        url=request.params.get('url'),
    )
    print(c)
    redirect(
        "/admin/headers",
        alert=Alert("Вы успешно отредактировали ссылку!")
    )


if os.getenv("DEVELOP") == "True":
    @route("/create_admin", GET_POST)
    def create_admin_page():
        if request.POST:
            create_admin(
                request.forms.get("login"),
                request.forms.get("password"),
                request.forms.get("name", ""),
            )

            redirect("/")

        return template(
            join("admin", "create_user")
        )


@admin_route("/ckeditor/upload_photo/<path:path>", POST)
def upload_photo(path):
    try:
        file = save_img(path=path, name_in_form="upload", overwrite=False)
        return {
            "url": file
        }
    except OSError:
        return {
            "error": {
                "message": "Изображение с таким именем существует. "
                           "Пожалуйста, переименуйте изображение и попробуйте снова."
            }
        }
    except Exception as err:
        return {
            "error": {
                "message": "Ошибка во время загрузки!\n(%s: %s)" % (type(err).__name__, err)
            }
        }

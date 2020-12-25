from enum import Enum
from typing import Iterable, Any, Tuple, Dict


class MenuItem:
    def __init__(self, name: str, url: str):
        self.name = name
        self._url = url.lstrip('/')
        self.group = None
        self.current = False

    @property
    def url(self):
        if isinstance(self.group, MenuGroup) and getattr(self.group, "url", False):
            return "%s/%s" % (self.group.name.lstrip('/'), self._url)
        return self._url

    def default(self):
        self.current = False


class MenuGroup:
    def __init__(self, name: str, *items: MenuItem, icon: str = None, expanded: bool = False):
        for i in items:
            i.group = self

        self.name = name
        self.items = tuple(items)
        self.icon = icon
        self._default_expanded = expanded
        self._expanded = expanded

    @property
    def expanded(self):
        return self._default_expanded or self._expanded

    @expanded.setter
    def expanded(self, value: bool):
        self._expanded = value

    def __iter__(self) -> Iterable[MenuItem]:
        return iter(self.items)

    def default(self):
        self._expanded = self._default_expanded
        for i in self.items:
            i.default()


class MenuTab:
    def __init__(self, name: str, *groups_or_items: MenuGroup or MenuItem):
        self.name = name
        self.goi = tuple(groups_or_items)  # type: Iterable[Any[MenuGroup, MenuItem]]
        self._enter = False

    @property
    def urls(self) -> Dict[str, Tuple[MenuGroup, MenuItem]]:
        urls = {}
        for g in self.goi:
            if isinstance(g, MenuItem):
                urls[g.url] = (None, g)
            elif isinstance(g, MenuGroup):
                for i in g:
                    urls[i.url] = (g, i)
        print(urls)
        return urls

    def __enter__(self):
        if not self._enter:
            raise BufferError("%s must be called!" % self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._enter = False
        for i in self.goi:
            i.default()

    def __call__(self, url: str):
        group, item = self.urls.get(url, (None, None))  # type: MenuGroup, MenuItem
        if group is not None:
            group.expanded = True
        if item is not None:
            item.current = True
        self._enter = True
        return self

    def __iter__(self) -> Iterable[MenuGroup or MenuItem]:
        return iter(self.goi)


ADMIN_TAB = MenuTab(
    "Админ-панель",
    MenuGroup(
        "Страницы",
        MenuItem(
            "Главная",
            "main_page"
        ),
        MenuItem(
            "Шапка сайта",
            "headers"
        ),
        # MenuItem(
        #     "Блоки",
        #     "blocks"
        # ),
        icon="file-alt",
        expanded=True,
    ),
    MenuGroup(
        "Новости",
        MenuItem(
            "Создать новость",
            "news/new"
        ),
        MenuItem(
            "Категории",
            "news/category"
        ),
        MenuItem(
            "Все новости",
            "news"
        ),
        icon="newspaper",
        expanded=True,
    ),
    MenuGroup(
        "Настройки",
        MenuItem(
            "Частые Вопросы",
            "faq"
        ),
        MenuItem(
            "Соц. сети",
            "socials"
        ),
        MenuItem(
            "SEO",
            "meta"
        ),
        icon="wrench",
    ),
)

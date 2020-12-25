from db.controller import *


def define_default():
    # db.drop_table(Header.__name__, True, True)
    # db.drop_table(Settings.__name__, True, True)
    # db.drop_table(Admin.__name__, True, True)
    #
    # migration()
    with db_session:
        a = [Header(
            name="Главная",
            url=""
        ), Header(
            name="Новости",
            url="news"
        ), Settings(
            key="main",
            value={"header": "Молодёжный портал", "subheader": "Пензенской области"}
        ), create_admin("jag-k", "1234")]
    print("Added all:", *a, sep='\n\n')


if __name__ == '__main__':
    define_default()

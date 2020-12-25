"""
docs: https://docs.ponyorm.org/
"""
from os import urandom

from db.models import *
from hashlib import pbkdf2_hmac
import binascii

SALT = b"QCIGSDwfnTOaoF1MFkzFZfFzbAhmlrnU"

# ==============================================================================
# ===== CONTROLLER =====

# ==============================================================================
# ADMIN FUNCS

def hash_admin(login, pwd):
    dk = pbkdf2_hmac(hash_name='sha256',
                     password=bytes("%s ---- %s" % (login, pwd), 'utf-8'),
                     salt=SALT,
                     iterations=100000)
    return str(binascii.hexlify(dk), encoding="utf-8")


def is_admin(login, pwd):
    return is_hash_admin(hash_admin(login, pwd))


@db_session
def is_hash_admin(h):
    return h and get(h == a.hash for a in Admin)


@db_session
def get_admin_by_login(login: str) -> Admin:
    return select(a for a in Admin if a.login == login).first()


@db_session
def get_admin_by_hash(hash: str) -> Admin:
    return select(a for a in Admin if a.hash == hash).first()


@db_session
def get_admin_by_id(id: int) -> Admin:
    return select(a for a in Admin if a.id == id).first()


@db_session
def get_admin(login_hash_id):
    return select(a for a in Admin if login_hash_id in (a.login, a.hash, a.id)).first()


@db_session
def create_admin(login: str, password: str, name: str = "") -> Admin or None:
    if not password:
        return None
    h = hash_admin(login, password)
    admin = get_admin_by_hash(h)

    if not admin and not select(a.login == login for a in Admin).first():
            return Admin(login=login, hash=h, name=name or login.split("@")[0])
    else:
        return admin


@db_session
def del_admin(login_hash_id):
    a = get_admin(login_hash_id)
    if a:
        a.delete()
        return True
    return False


@db_session
def edit_admin_password(login_hash_id, password: str):
    a = get_admin(login_hash_id)
    a.hash = hash_admin(a.login, password)
    return a


@db_session
def edit_admin_data(admin: Admin, name: str = None, login: str = None, password: str = None, **kwargs) -> Admin:
    if name:
        admin.name = name
    if login:
        admin.login = login
    if password:
        admin.hash = hash_admin(admin.login, password)
    return admin


@db_session
def get_settings(key, default={}):
    s = select(s for s in Settings if s.key == key).first()
    return s.value if s else default


@db_session
def get_all_settings():
    return dict(select((s.key, s.value) for s in Settings))


@db_session
def update_settings(key: str, value: dict):
    s = select(s for s in Settings if s.key == key).first()
    # print("GET", s)
    if s:
        s.value.update(value)
    else:
        with db_session:
            s = Settings(key=key, value=value)
        # print("ELSE", s)
    return s


# ===== END CONTROLLER =====


if __name__ == '__main__':

    print(hash_admin(None, None))
    print(hash_admin("jag-k", "1234"))
    print(hash_admin("", ""))
    print(hash_admin("jasdad", "asdawdw"))

    with db_session:
        Admin.select().show()
        create_admin("1234", "1234")
        """
        print(create_admin("jag-k58@ya.ru", "PASSWORD"))
        print()
        Admin.select().show()
        print(edit_admin_password("jag-k58@ya.ru", "PASSwORD"))
        print()
        Admin.select().show()
        print()
        Admin.select().show()
        """

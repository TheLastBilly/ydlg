from wol_control import *
from wol_control.models import User
from werkzeug.security import generate_password_hash, check_password_hash

default_admin_pass="admin"
default_admin_user="admin"

app = create_app()

with app.app_context():
    db.create_all()

    hash_passwd = generate_password_hash(default_admin_pass, method='sha256')
    new_user = User(name=default_admin_user, password=hash_passwd , admin=True)

    db.session.add(new_user)
    db.session.commit()
    
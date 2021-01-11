from ydlg import *
from wol_control.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os

admin_user = os.environ("YDLG_USERNAME")
if admin_user == "":
    admin_user = "admin"
admin_password = os.environ("YDLG_PASSWORD")
if admin_password == "":
    admin_password = "admin"

app = create_app()

with app.app_context():
    db.create_all()

    hash_passwd = generate_password_hash(admin_password, method='sha256')
    new_user = User(name=admin_user, password=hash_passwd , admin=True)

    db.session.add(new_user)
    db.session.commit()
    
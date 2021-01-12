from ydlg import *
from ydlg.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os

admin_user = ""
try:
    admin_user = os.environ["YDLG_USERNAME"]
except Exception as e:
    pass
if admin_user == "":
    admin_user = "admin"

admin_password = ""
try:
    admin_password = os.environ["YDLG_PASSWORD"]
except Exception as e:
    pass
if admin_password == "":
    admin_password = "admin"

secret_key = uuid.uuid4().hex
if not os.path.exists("/tmp/flask.key"):
    with open("/tmp/flask.key", "a") as fp:
        fp.write(secret_key)
    
app = create_app()

with app.app_context():
    db.create_all()

    hash_passwd = generate_password_hash(admin_password, method='sha256')
    new_user = User(name=admin_user, password=hash_passwd , admin=True)

    db.session.add(new_user)
    db.session.commit()
    
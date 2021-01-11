from wol_control import *
from wol_control.models import User
from werkzeug.security import generate_password_hash, check_password_hash

app = create_app()

with app.app_context():
    def display_users():
        users = User.query.all()
        if users is None:
            print("No users found")
            return None
        print("\nUser List:")
        number = 0
        for user in users:
            number+=1
            print("{}: {}{}".format(number, user.name, "" if not user.admin else " [ADMIN]" ))
        print("")
        return users
    def create_user():
        username = input("Username: ")
        raw_password = input("Password: ")
        is_admin = True
        admin_in = input("Is admin [Y/n]")

        if(admin_in == "N" or admin_in == "n"):
            is_admin = False

        if raw_password is None or len(raw_password) >= 100 or username is None or len(username) >= 100:
            print("Username/Password not valid")
            quit()

        hash_passwd = generate_password_hash(raw_password, method='sha256')
        new_user = User(name=username, password=hash_passwd , admin=is_admin)

        print("New user {} created succesfuly".format(username))

        db.session.add(new_user)
        db.session.commit()
    def delete_user(user):
        print("Deleting user {}".format(user.name))
        db.session.delete(user)
        db.session.commit()
    while True:
        users = display_users()
        response = input("What would you like to do? [create/delete/exit]: ")
        if response == "create":
            create_user()
            input("Press enter to continue")
            continue
        elif response == "delete":
            response = input("Which user would you like to delete: ")
            deleted_user = False
            for user in users:
                if response == user.name:
                    delete_user(user)
                    deleted_user = True
            if not deleted_user:
                print("User {} not found".format(response))
            input("Press enter to continue")
            continue
        elif response == "exit":
            print("Exiting...")
            break
        else:
            print("Command {} not recognized".format(response))
            continue
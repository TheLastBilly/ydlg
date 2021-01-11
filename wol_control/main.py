from flask import Blueprint, render_template, request, Response,redirect,url_for
import os
from flask_login import login_user, login_required, current_user
from .models import Mac

main = Blueprint('main', __name__)

remote_user = "wol_control"

log_filename = "../wol_control_access.log"

def get_controls( ):
    controls = []
    if current_user.admin:
        controls = Mac.query.all()
    else:
        controls = Mac.query.filter_by(admin=False)
    return controls

@main.route('/')
@login_required
def index():
    controls=get_controls()
    if controls is None:
        return render_template('control.html', message="No controllers have been regystered")
    return render_template( 'control.html', controls=controls)

@main.route('/control/<string:public_id>/<string:command>')
@login_required
def toggle_control(public_id, command):
    control = Mac.query.filter_by(public_id=public_id).first()
    def return_message(msg):
        return render_template('control.html', message=msg, redirect_home=True)
    def log_access( command ):
        with open(log_filename, "a") as log_file:
            log_file.write("User {} turned {} {}".format(current_user.name, control.name, command))

    if control is None:
        return_message("No such device found.")        
    elif control.admin is True and current_user.admin is False:
        return_message("Access denied.")    
    
    if command == "on":
        log_access(command)
        os.system("/usr/local/bin/wol {}".format(control.mac))
        return_message("Turning {} on".format(control.name))
    if command == "off":
        log_access(command)
        os.system("ssh {}@{} ~/.wol_control/remote_shutdown.sh".format(remote_user, control.ip))
        return_message("Turning {} off".format(control.name))
    else:
        return_message("Invalid command")

from flask import Blueprint, render_template, request, Response,redirect,url_for
import os
from flask_login import login_user, login_required, current_user
from .utils import *
import youtube_dl

main = Blueprint('main', __name__)

default_download_directory = ""

try:
    default_download_directory = os.environ["YDLG_DOWNLOAD_FOLDER"]
except Exception as e:
    pass
if default_download_directory == "":
    default_download_directory = "./Downloads"

@main.route('/')
@login_required
def index():
    return render_template( 'download.html')

@main.route('/download', methods=['POST'])
@login_required
def downloadYoutubeLink():
    url = request.form.get("URL")
    if not validateYoutubeURL(url):
       return render_template('download.html', message="Link it's not valid") 

    ydl_opts = {
        'outtmpl': default_download_directory + '/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return render_template('download.html', message="Done downloading")
from ydlg import create_app

application = create_app()

if __name__ == "__main__":
    application.run(host='http://0.0.0.0')

import re

def validateYoutubeURL( input ):
    return re.match("^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$", input.lower())
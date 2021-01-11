import re

def validate_mac_input( input ):
    return re.match("[0-9a-f]{2}([:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", input.lower())

def validate_ip_input( input ):
    return re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", input.lower())
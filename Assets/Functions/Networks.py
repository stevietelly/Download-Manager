import requests
import Assets.Functions.Parser as p
import validators
import importlib


def internet():
    try:
        requests.head('http://www.google.com/', timeout=1)
        return True
    except Exception as s:
        str(s.args)
        return False


def check_network_connection(use="internal"):
    importlib.reload(p)
    p.KeyMatch().reload()
    if use == "internal":
        return internet()
    elif use == "external":
        if p.KeyMatch().match("internet_validation"):
            return internet()
        elif not p.KeyMatch().match("internet_validation"):
            return True


def validate_url(url):
    perf = validators.url(url)
    if perf:
        return True
    elif not perf:
        return False


def check_link_validity(url, use="internal"):
    importlib.reload(p)
    """Telly App internal functions
     for validating the url being passed which is either user controlled dor the external and the internal which is
     a must requirement"""
    if use == 'internal':
        return validate_url(url)
    elif use == "external":
        if not p.KeyMatch().match("link_validation"):
            return True
        elif p.KeyMatch().match("link_validation"):
            return validate_url(url)

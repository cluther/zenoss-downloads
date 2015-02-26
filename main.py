# Python Standard Library
import cookielib
import os.path
import urllib
import urllib2

# Google App Engine
import cloudstorage
from google.appengine.api import app_identity

# Third Party
from flask import Flask, abort, send_file
from flask.ext.httpauth import HTTPBasicAuth


app = Flask("zenoss-downloads")
app.config['DEBUG'] = True

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """Return True if username and password are valid.

    Validity is checked by attempting to login to Zendesk with the
    provided credentials.

    """
    return_to = "https://support.zenoss.com/hc/en-us/requests"

    payload = {
        "user[email]": username,
        "user[password]": password,
        "return_to": return_to,
        }

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    r = opener.open(
        "https://zenoss.zendesk.com/access/login",
        urllib.urlencode(payload))

    if "unauthenticated" in r.url:
        return False

    if r.url.startswith(return_to):
        return True

    return False


@app.route("/<filename>")
@auth.login_required
def download(filename):
    bucket = app_identity.get_default_gcs_bucket_name()
    path = os.path.join('/', bucket, filename)

    try:
        fp = cloudstorage.open(path, 'r')
    except Exception:
        abort(404)

    # add_etags not compatible with Google Cloud Storage.
    return send_file(fp, add_etags=False)


if __name__ == "__main__":
    app.run()

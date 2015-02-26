#!/usr/bin/env python
import cookielib
import sys
import urllib
import urllib2


def main():
    return_to = "https://support.zenoss.com/hc/en-us/requests"

    payload = {
        "user[email]": sys.argv[1],
        "user[password]": sys.argv[2],
        "return_to": return_to,
        }

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    r = opener.open(
        "https://zenoss.zendesk.com/access/login",
        urllib.urlencode(payload))

    import pdb; pdb.set_trace()
    print r


if __name__ == "__main__":
    main()

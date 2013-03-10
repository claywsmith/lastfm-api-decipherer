import requests
import yaml
from sys import exit

rootURL = "http://ws.audioscrobbler.com/2.0/"
apikey = ''
apisecret = ''
user = ''
sk = ''
sig = ''
token = ''
format = '&format=json'

def main():
    global apikey
    global apisecret
    global sk
    global user

    try:
        fh = open('config.yaml')
    except IOError:
        print """
        Failed to open "config.yaml" for reading.  We have created this file for you.  You must now edit it,
        and its format is:

        apikey: xxxxxxx
        apisecret: yyyyyyy

        """
        exit(1)

    config = yaml.load(fh.read())
    apikey = config['apikey']
    apisecret = config['apisecret']
    fh.close()

    getSig()
    authCheck()
    fh = open('config.yaml')
    config = yaml.load(fh.read())
    sk = config['sk']
    fh.close()
    print "line43, sig:", sig

    user = raw_input("What is your Last.FM user name? >> ")

    menu()

def menu():
    print """
	Welcome to the Last.FM XML Deciphering Thing
		1. Top artists
		2. Top songs
		3. Top albums
		4. Most recent songs
		5. Upcoming releases you may be interested in
		6. Recommended artists
		7. Auth checkUpcoming shows you might want to attend
		Q. Exit

		"""
    projectRunner()


def projectRunner():
    go = raw_input("What info would you like? >> ").strip()
    if not go.isdigit() and go not in range(7) and go.lower() != "q":
        print "Invalid input"
        projectRunner()
    elif go == "1":
        getTop("user.getTopArtists", "topartists", "artist")
    elif go == "2":
        getTop("user.getTopTracks", "toptracks", "track")
    elif go == "3":
        getTop("user.getTopAlbums", "topalbums", "album")
    elif go == "4":
        getRecent("user.getRecentTracks", "recenttracks", "track")
    elif go == "5":
        getRecent("user.getNewReleases", "albums", "album")
    elif go == "6":
        getRecArtists("user.getRecommendedArtists", "artists", "artist")
    elif go == "7":
        authCheck()
    elif go.lower() == "q":
        exit(0)
    # elif go = "8":
    # 	recEvents(): #"user.getRecommendedEvents"
    else:
        print "Invalid input"
        projectRunner()

def buildURL(method):
    if method not in 'user.getRecommendedArtists':
        url = '%s?method=%s&user=%s&api_key=%s&limit=20%s' % (rootURL, method, user, apikey, format)
    elif method == 'user.getRecommendedArtists':
        url = '%s?method=%s&user=%s&api_key=%s&api_sig=%s&sk=%s&limit=20%s' % (rootURL, method, user, apikey, sig, sk, format)
    elif method == 'auth.getToken':
        url = '%s?method=%s&api_key=%s&%s' % (rootURL, method, apikey, format)
    return url

def queryAPI(url):
    response = requests.get(url)
    data = response.json()
    return data


def getTop(method, var2, var3):
    print "\n"
    url = buildURL(method)
    data = queryAPI(url)
    l = []
    p = []
    a = []

    for item in data[var2][var3]:
        l.append(item["name"])
        p.append(item["playcount"])
        if var2 == "topalbums":
            a.append(item["artist"]["name"])

    if var2 == "topalbums":
        for index, name in enumerate(l):
            print '%d. %s, "%s" - %s plays' % ((index + 1), a[index], name, p[index])
    else:
        for index, name in enumerate(l):
            print "%d. %s - %s plays" % ((index + 1), name, p[index])

    menu()

def getRecent(method, var2, var3):
    print "\n"
    url = buildURL(method)
    data = queryAPI(url)

    for item in data[var2][var3]:
        if var3 == "track":
            print "%s - %s" % (item["artist"]["#text"], item["name"])
        else:
            print "%s - %s" % (item["artist"]["name"], item["name"])

    menu()

def getRecArtists(method, var2, var3):
    print '\n'
    url = buildURL(method)
    print url
    data = queryAPI(url)
    print data
    for item in data[var2][var3]:
        print "%s" % (item["name"])

def getSig():
    global sig
    global token
    import hashlib
    url = buildURL("auth.getToken")
    data = queryAPI(url)
    token = data["token"]
    sig = hashlib.md5("api_key" + apikey + "methodauth.getSessionToken" + token + apisecret).hexdigest()


def authenticate():
    import webbrowser
    url = "http://www.last.fm/api/auth/?api_key=%s+&token=%s" % (apikey, token)
    webbrowser.open(url, new=2)
    raw_input("Press ENTER when authentication is passed.")
    url = rootURL + '?method=auth.getSession&api_key=%s&token=%s&api_sig=%s&format=json' % (apikey, token, sig)
    response = requests.get(url)
    data = response.json()
    key = data["session"]["key"].encode('ascii', 'ignore')
    print "line 171, key: " + key
    fh = open('config.yaml', 'a')
    fh.write(('\nsk: ' + key))
    fh.close()

def authCheck():
    fh = open('config.yaml', 'r')
    checker = []
    
    for word in fh:
        checker.append(word)
    fh.close()
    if len(checker) == 3:
        pass
    else:
        authenticate()

if __name__ == '__main__':
    main()
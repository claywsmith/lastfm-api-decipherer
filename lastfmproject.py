import requests
import yaml
from sys import exit

rootURL = "http://ws.audioscrobbler.com/2.0/"
apikey = ""
apisecret = ""
user = ''

def main():
    global apikey
    global apisecret
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
		7. Upcoming shows you might want to attend
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
    elif go.lower() == "q":
        exit(0)
    # elif go = "8":
    # 	recEvents(): #"user.getRecommendedEvents"
    else:
        print "Invalid input"
        projectRunner()


def queryAPI(method):
    url = '%s?method=%s&user=%s&api_key=%s&format=json' % (rootURL, method, user, apikey)
    response = requests.get(url)
    data = response.json()
    return data


def getTop(method, var2, var3):
    print "\n"
    data = queryAPI(method)
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
    data = queryAPI(method)
    for item in data[var2][var3]:
        if var3 == "track":
            print "%s - %s" % (item["artist"]["#text"], item["name"])
        else:
            print "%s - %s" % (item["artist"]["name"], item["name"])
    menu()


def authenticate():
    pass

if __name__ == '__main__':
    main()
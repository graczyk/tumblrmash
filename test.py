import pytumblr
import json
import random

credentials = json.loads(open('tumblr_credentials.json', 'r').read())
client = pytumblr.TumblrRestClient(credentials["consumer_key"], credentials["consumer_secret"], credentials["oauth_token"], credentials["oauth_token_secret"])

following = client.following()

#create list of blogs, put in list
blogs = following["blogs"]
tosearch = []
for blog in blogs:
    tosearch.append(blog["url"])

#create dictionary with original picture URLs and set the count to 0
pics = {}
for blog in tosearch:
    resp = client.posts(blog[7:].rstrip('/'), type='photo', tag='me')
    for post in resp["posts"]:
        for orig in post["photos"]:
            pics[orig["original_size"]["url"]] = 0
            
running = True        
def total():
    #print out all sorted dictionary elements with a value of 1 or greater
    print "todo"
    running = False
    
while running:
    pic1 = random.choice(pics.keys())
    print pic1
    pic2 = random.choice(pics.keys())
    print pic2
    s = raw_input("Please enter 1 or 2 to choose the more interesting picture or 0 to total and exit.")
    if s == "0":
        total()
        break;
    elif s == "1":
        pics[pic1] += 1
        print pics.get(pic1)
    elif s == "2":
        pics[pic2] += 1
        print pics.get(pic2)
    else:
        print "Enter 1, 2 or 0"
    
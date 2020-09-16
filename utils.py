import json 
from datetime import date

def addPost(post):
  data = open("posts.json")
  raw_date = str(date.today()).split("-")
  posts = json.load(data)
  data.close()
  if post["author"] == None:
    post["author"] = "Admin"
  data = open("posts.json", "w")
  posts.append({"#": len(posts) + 1,
  "title": post["title"],
  "subtitle": post["subtitle"],
  "author": post["author"],
  "date": "|".join(raw_date),
  "slug": post["slug"],
  "content": post["content"],
  "edited": False
  })
  datastr = json.dumps(posts)
  data.write(datastr)
  data.close()

def editPost(post):
  data = open("posts.json")
  raw_date = str(date.today()).split("-")
  posts = json.load(data)
  data.close()
  data = open("posts.json", "w")
  post["date"] = "|".join(raw_date)
  post["edited"] = True
  posts[(post["#"]-1)] = post
  datastr = json.dumps(posts)
  data.write(datastr)
  data.close()

def delPost(index):
  data = open("posts.json")
  posts = json.load(data)
  data.close()
  data = open("posts.json", "w")
  posts.pop(index)
  for i in posts:
    if i["#"]-1 != 0:
      i["#"] = i["#"] - 1
    else:
      pass
  datastr = json.dumps(posts)
  print(datastr)
  data.write(datastr)
  data.close()
  
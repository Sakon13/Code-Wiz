from flask import request, Flask, render_template, session, redirect
import json
import utils as ut
import math

def loadParams():
  with open("config.json") as c:
    return json.load(c)

def loadPosts():
  with open("posts.json") as data:
    return json.load(data)[::-1]
  
app = Flask(__name__)
app.secret_key = "Ki3#sh4"

@app.route("/")
def home():
  params = loadParams()
  posts = loadPosts()
  page = request.args.get("page")
  last = math.ceil(len(posts)/int(params["posts_limit"]))
  if not str(page).isnumeric():
    page = 1

  posts = posts[(int(page)-1)*int(params["posts_limit"]):(int(page)-1)*int(params["posts_limit"])+int(params["posts_limit"])]
  if last == 1:
    new = "#"
    old = "#"
  elif int(page) == 1:
    new = "#"
    old = "/?page=" + str(int(page) + 1)
  elif int(page) == last:
    new = "/?page=" + str(int(page) - 1)
    old = "#"
  else:
    new = "/?page=" + str(int(page) - 1)
    old = "/?page=" + str(int(page) + 1)
    print(new, old)
  return render_template("index.html", params=params, posts=posts, old=old, new=new)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/posts/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
  params = loadParams()
  posts = loadPosts()
  post = list(filter(lambda x: x["slug"] == post_slug , posts))
  return render_template("post.html", post=post[0])

@app.route("/dashboard", methods=["POST", "GET"])
def login():
  params = loadParams()
  posts = loadPosts()
  if "user" in session and session["user"] == params["admin_user"]:
    return render_template("dashboard.html", posts=posts)
  
  if request.method=="POST":
    user = request.form.get("uname")
    password = request.form.get("upass")
    if user == params["admin_user"] and password == params["admin_pass"]:
      session["user"] = user
      return render_template("dashboard.html", posts=posts)
    else:
      return render_template("login.html")
  else:
    return render_template("login.html")

@app.route("/edit/<string:no>", methods=["GET", "POST"])
def edit(no):
  params = loadParams()
  posts = loadPosts()
  post = list(filter(lambda x: str(x["#"]) == no, posts))
  if len(post)==0:
    post = [{"#": 0}]
  else:
    pass
  if request.method == "GET":
    if "user" in session and session["user"] == params["admin_user"]:
      return render_template("edit.html", post=post[0])
    else:
      return render_template("unauthorized.html", params=params)
  elif request.method=="POST":
    if "user" in session and session["user"] == params["admin_user"]:
      post[0]["title"] = request.form.get("title")
      post[0]["subtitle"] = request.form.get("subtitle")
      post[0]["slug"] = request.form.get("slug")
      post[0]["author"] = request.form.get("author")
      post[0]["content"] = request.form.get("content")
      if int(no) > 0:
        ut.editPost(post[0])
      else:
        ut.addPost(post[0])
      return redirect("/dashboard")
    else:
      return render_template("unauthorized", params=params)

@app.route("/logout")
def logout():
  params = loadParams()
  if "user" in session and session["user"] == params["admin_user"]:
    session.pop("user")
    return redirect("/dashboard")
  else:
    return render_template("logout.html", params=params)

@app.route("/delete/<string:index>")
def delete(index):
  params = loadParams()
  if "user" in session and session["user"] == params["admin_user"]:
    ut.delPost(int(index)-1)
    posts = loadPosts()
    return redirect("/dashboard")
  else:
    return render_template("unauthorized.html")

@app.route("/test")
def test():
  params = loadParams()
  if "user" in session and session["user"] == params["admin_user"]:
    if params["testenv"] == True:
      return render_template(params["testTemplate"], params=params["testParams"])
    else:
      return render_template("test.html", params=params["testParams"])
  else:
    return render_template("unauthorized.html", params=params)
app.run(debug=True)
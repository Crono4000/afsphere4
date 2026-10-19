
import flask
from AfsphereDB import AfsphereDB
from datetime import datetime, timedelta, timezone


app = flask.Flask(__name__)
db = AfsphereDB()
blacklist: set[str] = set()
acesses: dict[str, int] = dict()
acess_limit: int = 25


def my_split(text: str) -> list[str]:
    if text == "":
        return []
    return text.split(" ")


def check_login(session: str) -> bool:
    if session is None:
        return False
    return db.OneExecute("SELECT check_login_session(%s);", [session])


@app.before_request
def check_auth():
    print(acesses)
    remote_addr = flask.request.headers.get("X-Real-IP")
    print(remote_addr)
    if remote_addr in blacklist:
        flask.abort(401)
    login_session = flask.request.cookies.get("login_key")
    if flask.request.path == "/login_page" or flask.request.path == "/login":
        if remote_addr in acesses:
            acesses[remote_addr] += 1
        else:
            acesses[remote_addr] = 1
        if acesses[remote_addr] >= acess_limit:
            blacklist.add(remote_addr)
        return
    if not check_login(login_session):
        if remote_addr in acesses:
            acesses[remote_addr] += 1
        else:
            acesses[remote_addr] = 1
        if acesses[remote_addr] >= acess_limit:
            blacklist.add(remote_addr)
        return flask.redirect("/login_page")


@app.route("/")
def index():
    return flask.render_template("home.html")


@app.route("/create_info")
def create_info():
    return flask.render_template("create_info.html")


@app.route("/login_page", methods=["GET"])
def login_page():
    return flask.render_template("login.html")


@app.route("/info/<int:id>")
def info(id: int):
    info = db.Execute("SELECT * FROM get_info(%s)", [id])
    tags = db.Execute("SELECT * FROM get_info_tags(%s)", [id])
    return flask.render_template("info.html", tags=tags, title=info[0][0], content=info[0][1], info_id=id)


@app.route("/edit_info/<int:id>")
def edit_info(id: int):
    info = db.Execute("SELECT * FROM get_info(%s)", [id])
    tags = db.Execute("SELECT * FROM get_info_tags(%s)", [id])
    return flask.render_template("edit_info.html", tags=tags, title=info[0][0], content=info[0][1], info_id=id)


@app.route("/search_infos/<int:page>")
def search_infos(page: int) -> None:
    search: str = flask.request.args.get("search")
    if search is None:
        return flask.redirect(flask.url_for("search_infos", page=0, search=""))
    result = db.Execute("SELECT * FROM search_infos_by_tags_webpage(%s::text[], %s)", [my_split(search), page])
    return flask.render_template("search_infos.html", infos=result, page=page)


@app.route("/add_info", methods=["POST"])
def post_add_info():
    title = flask.request.form.get("title")
    info = flask.request.form.get("info")
    tags = flask.request.form.get("tags")
    if title is None or info is None or tags is None:
        return flask.redirect(flask.url_for("create_info", page=0, search=""))
    id = db.OneExecute("CALL insert_info(%s, %s, NULL);", [title, info])
    if id is None:
        return flask.redirect(flask.url_for("create_info", page=0, search=""))
    db.Execute("CALL insert_info_tags(%s, %s);", [tags.split(" "), id])
    return flask.redirect(flask.url_for("search_infos", page=0, search=""))


@app.route("/edit_title_info", methods=["POST"])
def post_edit_title_info():
    title = flask.request.form.get("title")
    info_id = flask.request.form.get("info_id")
    if title is None or info_id is None:
        return flask.redirect("/")
    db.Execute("UPDATE info SET title = %s WHERE info_id = %s", [title, info_id])
    return flask.redirect(flask.url_for("edit_info", id=info_id))


@app.route("/edit_content_info", methods=["POST"])
def post_edit_content_info():
    content = flask.request.form.get("content")
    info_id = flask.request.form.get("info_id")
    if content is None or info_id is None:
        return flask.redirect("/")
    db.Execute("UPDATE info SET info_content = %s WHERE info_id = %s", [content, info_id])
    return flask.redirect(flask.url_for("edit_info", id=info_id))


@app.route("/add_tag_info", methods=["POST"])
def post_add_tag_info():
    tag = flask.request.form.get("tag")
    info_id = flask.request.form.get("info_id")
    if tag is None or info_id is None:
        return flask.redirect("/")
    db.Execute("CALL insert_info_tag(%s, %s);", [tag, info_id])
    return flask.redirect(flask.url_for("edit_info", id=info_id))


@app.route("/delete_tag_info", methods=["POST"])
def post_delete_tag_info():
    tag = flask.request.form.get("tag")
    info_id = flask.request.form.get("info_id")
    if tag is None or info_id is None:
        return flask.redirect("/")
    db.Execute("CALL delete_info_tag(%s, %s);", [tag, info_id])
    return flask.redirect(flask.url_for("edit_info", id=info_id))
                          

@app.route("/login", methods=["POST"])
def login():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    key = db.OneExecute("SELECT login_user(%s, %s);", [username, password])
    if key is None:
        return flask.redirect(flask.url_for("login_page"))
    response = flask.redirect("/")
    response.set_cookie("login_key", key, expires=datetime.now(timezone.utc) + timedelta(days=7))
    return response


if __name__ == "__main__":
    app.run(debug=True)

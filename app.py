
import flask
from AfsphereDB import AfsphereDB


app = flask.Flask(__name__)
db = AfsphereDB()


def my_split(text: str) -> None:
    if text == "":
        return []
    return text.split(" ")


@app.route("/")
def index():
    return flask.render_template("home.html")


@app.route("/create_info")
def create_info():
    return flask.render_template("create_info.html")


@app.route("/info/<int:id>")
def info(id):
    info = db.Execute("SELECT * FROM get_info(%s)", [id])
    tags = db.Execute("SELECT * FROM get_info_tags(%s)", [id])
    print(tags)
    return flask.render_template("info.html", tags=tags, title=info[0][0], content=info[0][1])


@app.route("/search_infos/<int:page>")
def search_infos(page: int) -> None:
    search: str = flask.request.args.get("search")
    if search is None:
        return flask.redirect(flask.url_for("search_infos", page=0, search=""))
    result = db.Execute("SELECT * FROM search_infos_by_tags_webpage(%s::text[], %s)", [my_split(search), page])
    return flask.render_template("search_infos.html", infos=result)


@app.route("/post/add_info", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True)

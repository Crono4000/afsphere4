
import flask
from AfsphereDB import AfsphereDB


app = flask.Flask(__name__)
db = AfsphereDB()


@app.route("/")
def index():
    return flask.render_template("home.html")


@app.route("/create_info")
def create_info():
    return flask.render_template("create_info.html")


@app.route("/search_infos/<page>")
def search_infos(page) -> None:
    search: str = flask.request.args.get("search")
    if search is None or not page.isnumeric:
        return flask.redirect(flask.url_for("/search_infos/0?search="))
    page = int(page)
    result = db.Execute("SELECT * FROM search_infos_by_tags_webpage(%s::text[], %s::int)", [search.split(" "), page])
    print(result)
    return flask.render_template("search_infos.html", infos=result)


@app.route("/post/add_info", methods=["POST"])
def post_add_info():
    title = flask.request.form.get("title")
    info = flask.request.form.get("info")
    tags = flask.request.form.get("tags")
    if title is None or info is None or tags is None:
        return flask.redirect(flask.url_for("/create_info"))
    id = db.OneExecute("CALL insert_info(%s, %s, NULL);", [title, info])
    if id is None:
        return flask.redirect(flask.url_for("/create_info"))
    db.Execute("CALL insert_info_tags(%s, %s);", [tags.split(" "), id])
    return flask.redirect(flask.url_for("/search_infos/0?search="))


if __name__ == "__main__":
    app.run(debug=True)

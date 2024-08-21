from flask import Blueprint

from flask import Blueprint

bookmarks = Blueprint('bookmarks', __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route("/bookmarks", methods=['POST', 'GET'])
def index():
    return {"BOOKMARKS":[]}
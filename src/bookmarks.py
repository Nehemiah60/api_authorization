
from flask import Blueprint, request, jsonify, abort
from src.models import Bookmarks, db
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required

bookmarks = Blueprint('bookmarks', __name__, url_prefix="/api/v1")

@bookmarks.route("/bookmarks", methods=['POST', 'GET'])
@jwt_required()
def create_bookmarks():
    current_user = get_jwt_identity()

    if request.method == 'POST':
        data = request.get_json()

        body = data.get('body')
        url = data.get('url')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            })
        
        # Check if URL exists

        existing_url = Bookmarks.query.filter_by(url=url).first()

        if existing_url:
            return jsonify({
                'error': 'That url exists'
            })
        bookmark = Bookmarks(
            body = body,
            url = url,
            user_id = current_user
        )

        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'url':bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at': bookmark.updated_at
        })
    
    else:
        page = request.args.get('page', 1 , type=int)
        start = (page-1)*20
        end = start + 5
        bookmarks = Bookmarks.query.filter_by(user_id=current_user)

        data = []

        for bookmark in bookmarks:
            data.append({
                'id': bookmark.id,
                'url':bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'body': bookmark.body,
                'created_at':bookmark.created_at,
                'updated_at': bookmark.updated_at
            })
       

        return jsonify({
            'data': data[start:end]
        })

        #Retrieve a single Item

@bookmarks.route('/bookmarks/<int:bookmark_id>', methods=['GET'])
@jwt_required()
def get_single_bookmark(bookmark_id):
    bookmark = Bookmarks.query.filter(Bookmarks.id == bookmark_id).one_or_none()

    if bookmark is None:
        abort(404)
    
    else:
        return jsonify({
            "bookmark": bookmark.body,
            "id": bookmark.id,
            "visits": bookmark.visits
        })

@bookmarks.route('/bookmarks/update/<int:bookmark_id>' , methods=['POST', 'PUT', 'PATCH'])
@jwt_required()
def update_book(bookmark_id):
    bookmark = Bookmarks.query.filter(Bookmarks.id==bookmark_id).one_or_none() 

    data = request.get_json()
    bookmark.url = data.get("url")
    bookmark.body = data.get("body")
    db.session.commit()

    return jsonify({
            "updated": bookmark.id,
            "updated_bookmark_body": bookmark.body
        })

#delete bookmark
@bookmarks.route('/bookmarks/delete/<int:bookmark_id>' , methods=['DELETE'])
@jwt_required()
def delete_book(bookmark_id):
    bookmark = Bookmarks.query.filter(Bookmarks.id==bookmark_id).one_or_none() 
   
    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({
            "message": "Bookmark deleted successfully",
            "deleted": bookmark.id,
            "deleted_bookmark_body": bookmark.body
        })

#get visits stats
@bookmarks.route('/bookmarks/stats', methods=['GET'])
@jwt_required()
def get_stats():
    current_user = get_jwt_identity()
    bookmarks = Bookmarks.query.filter_by(user_id=current_user).all()
    data = []

    for bookmark in bookmarks:
        new_link = {
            "id": bookmark.id,
            "visits": bookmark.visits,
            "short_url": bookmark.short_url

        }
        data.append(new_link)

    return jsonify({"data": data})
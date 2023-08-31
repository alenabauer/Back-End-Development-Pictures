from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """ return all pictures """
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """ return the picture with the given ID"""
    picture = next((p for p in data if p["id"] == id), None)

    if picture is not None:
        return jsonify(picture), 200
    else:
        return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """ create a new picture object """
    picture_exists = next((True for p in data if p["id"] == request.json["id"]), False)

    if picture_exists:
        return jsonify({"Message": "picture with id {} already present".format(request.json["id"])}), 302

    data.append(request.json)
    return jsonify(request.json), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """ update a picture object """
    picture = next((p for p in data if p["id"] == id), None)

    if picture is not None:
        picture.update(request.json)
        return jsonify(picture), 200
    else:
        return jsonify({"error": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """ delete a picture object """
    picture = next((p for p in data if p["id"] == id), None)

    if picture is not None:
        data.remove(picture)
        return jsonify({}), 204
    else:
        return jsonify({"error": "Picture not found"}), 404

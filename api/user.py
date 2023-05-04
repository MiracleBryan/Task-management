from flask_restx import reqparse, Resource, Namespace
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    unset_jwt_cookies,
    get_jwt_identity,
)
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os

from database.models import User
from database.db import db
from config import get_config

api = Namespace("user", desc="User endpoints")


@api.route("")
class UserResource(Resource):
    # Get User - Obtain Information
    get_user_parser = reqparse.RequestParser()
    get_user_parser.add_argument("user_id", type=int, required=False)

    @api.expect(get_user_parser)
    @api.doc(
        responses={
            200: "User profile.",
            401: "Unauthorized.",
            404: "{error: 'Not found.', user: Object}",
            404: "{error: 'Not connected.'}",
        },
        description="Get user profile.",
    )
    @jwt_required()
    def get(self):
        """
        Get the current logged in user profile
        """
        args = self.get_user_parser.parse_args()
        query_user_id = args["user_id"]  # The query user id

        # This user
        email = get_jwt_identity()
        query_user = this_user = User.query.filter_by(email=email).first()

        # The queried user
        if query_user_id is not None:
            query_user = User.query.filter_by(id=query_user_id).first()

            # Query user is not found.
            if query_user is None:
                return {"error": "Not found."}, 404
            else:
                # Query user not connected to this user.
                if (this_user != query_user) and not this_user.is_connected_to(
                    query_user
                ):
                    return {
                        "error": "Not connected.",
                        "user": query_user.parse_private(),
                    }, 404

        return query_user.parse()

    # Create User - Sign Up
    create_user_parser = reqparse.RequestParser()
    create_user_parser.add_argument("name", required=True, default="test")
    create_user_parser.add_argument("email", required=True, default="test@google.com")
    create_user_parser.add_argument("password", required=True, default="test")
    create_user_parser.add_argument("mobile", required=False, default="")
    create_user_parser.add_argument("linkedin", required=False, default="")

    @api.expect(create_user_parser)
    @api.doc(
        responses={201: "Created.", 409: "Account with email already exists."},
        description="Signs up a user account.",
    )
    def post(self):
        """
        User sign up or register
        """
        args = self.create_user_parser.parse_args(strict=True)

        # Checks if email already ties to an account. If so return 409 conflict.
        if User.query.filter_by(email=args.email).first():
            return "Account with email already exists.", 409

        # Hash and Salt Password
        hashed_password = generate_password_hash(
            args.password, method="pbkdf2:sha256", salt_length=16
        )

        # Create the account.
        user = User(
            name=args.name,
            email=args.email,
            password=hashed_password,
            mobile=args.mobile,
            linkedin=args.linkedin,
        )
        db.session.add(user)
        db.session.commit()

        # Success.
        return "Created.", 201

    # Update User - Edit User Information
    edit_user_parser = reqparse.RequestParser()
    edit_user_parser.add_argument("email", required=False)
    edit_user_parser.add_argument("password", required=False)
    edit_user_parser.add_argument("name", required=False)
    edit_user_parser.add_argument("mobile", required=False)
    edit_user_parser.add_argument("linkedin", required=False)
    edit_user_parser.add_argument("picture", required=False)

    @api.expect(edit_user_parser)
    @api.doc(
        responses={200: "Edit Success.", 401: "Unauthorized."},
        description="Edits a user account.",
    )
    @jwt_required()
    def put(self):
        """
        Update or edit user profile
        """
        args = self.edit_user_parser.parse_args(strict=True)

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()
        if not user:
            response = {"message": "User does not Exist!"}
            return response

        if args.name:
            user.name = args.name
        if args.email:
            user.email = args.email
        if args.password:
            hashed_password = generate_password_hash(
                args.password, method="pbkdf2:sha256", salt_length=16
            )
            user.password = hashed_password
        if args.mobile:
            user.mobile = args.mobile
        if args.linkedin:
            user.linkedin = args.linkedin

        db.session.commit()
        response = {"message": "User info updated successfully!"}
        return response


@api.route("/picture")
class UserProfilePicture(Resource):
    # Upload user profile picture
    user_picture_parser = reqparse.RequestParser()
    user_picture_parser.add_argument(
        "file",
        required=True,
        type=FileStorage,
        location="files",
    )

    @api.expect(user_picture_parser)
    @api.doc(
        responses={200: "{ 'filename': url }", 400: "Bad file format."},
        description="Uploads a user profile picture.",
    )
    @jwt_required()
    def post(self):
        """
        Profile Picture Upload
        """
        args = self.user_picture_parser.parse_args(strict=True)

        # This user
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        # Allowed format of picture.
        allowed_formats = {"png", "jpg", "jpeg"}
        file = args["file"]

        # Empty filename.
        if file.filename == "":
            return "Bad file format.", 400

        # Image format.
        picture_file_format = file.filename.rsplit(".", 1)[1].lower()
        if picture_file_format not in allowed_formats:
            return "Bad file format.", 400

        # Save uploaded image.
        filename = f"profilepic-{uuid.uuid4().hex}.{picture_file_format}"
        config = get_config()
        file.save(os.path.join(config["static_folder"], filename))

        # Update user profile picture
        user.picture = filename
        db.session.commit()

        return {"filename": filename}, 200


@api.route("/login")
class Login(Resource):
    # Login User
    login_user_parser = reqparse.RequestParser()
    login_user_parser.add_argument("email", required=True, default="test@google.com")
    login_user_parser.add_argument("password", required=True, default="test")

    @api.expect(login_user_parser)
    @api.doc(
        responses={200: "Log In Success.", 401: "Unauthorized."},
        description="Logs in a user with an email and password.",
    )
    def post(self):
        """
        User login
        """
        args = self.login_user_parser.parse_args(strict=True)

        # Tries to log user in. 401 if unauthorized.
        user = User.query.filter_by(email=args.email).first()

        if user and check_password_hash(user.password, args.password):
            access_token = create_access_token(identity=args.email)
            return {"message": "Log In Success.", "access_token": access_token}, 200
        else:
            return "Unauthorized.", 401


@api.route("/logout")
class Logout(Resource):
    @api.doc(
        responses={200: "Log Out Success.", 422: "Unprocessable Entity."},
        description="Logs a user out.",
    )
    @jwt_required()
    def post(self):
        """
        User logout
        """
        response = jsonify({"message": "Log Out Success."})
        unset_jwt_cookies(response)
        return response

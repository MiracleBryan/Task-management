from flask_restx import reqparse, Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import User, Connection, ConnectionStatusEnum
from database.db import db

import api.socket_events as socket

api = Namespace("connectionrequest", desc="Connection Request endpoints")


@api.route("")
class ConnectionRequestResource(Resource):
    # Gets all incoming or outgoing connection request of a user
    query_connection_parser = reqparse.RequestParser()

    @api.expect(query_connection_parser)
    @api.doc(
        responses={
            200: "Connection accepted.",
            304: "Connection already established.",
            400: "Connection request not found.",
            400: "Requested user not found.",
            401: "Unauthorized.",
        },
        description="Shows all connections for the email.",
    )
    @jwt_required()
    def get(self):
        """
        Get incoming / outgoing connection requests
        """
        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        return {
            "IncomingConnection": [
                conn.user_1.parse_private()
                for conn in this_user.incoming_connection_requests
            ],
            "OutgoingConnection": [
                conn.user_2.parse_private()
                for conn in this_user.outgoing_connection_requests
            ],
        }, 200

    # Creates a connection request
    request_connection_parser = reqparse.RequestParser()
    request_connection_parser.add_argument("email", required=True)

    @api.expect(request_connection_parser)
    @api.doc(
        responses={
            201: "Created.",
            400: "Connection request already created.",
            400: "Connection request already created by the other user.",
            400: "Connection already established.",
            400: "Cannot connect to yourself.",
            400: "Requested user not found.",
            401: "Unauthorized.",
        },
        description="Request for a connection to the email specified.",
    )
    @jwt_required()
    def post(self):
        """
        Creates a connection request from current user to the email passed
        """
        args = self.request_connection_parser.parse_args(strict=True)

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()
        other_user = User.query.filter_by(email=args.email).first()

        # Checks if the requested user is found.
        if other_user is None:
            return "Requested user not found.", 400

        # Checks if connecting to yourself.
        if this_user.id == other_user.id:
            return "Cannot connect to yourself.", 400

        # Checks if connection request has already been made or established.
        conn = Connection.query.filter_by(
            user_1_id=this_user.id, user_2_id=other_user.id
        ).first()
        if conn:
            if conn.status == ConnectionStatusEnum.pending:
                return "Connection request already created.", 400
            else:
                return "Connection already established.", 400

        # Checks if connection request has already been made from other_user to this_user.
        conn = Connection.query.filter_by(
            user_1_id=other_user.id, user_2_id=this_user.id
        ).first()
        if conn:
            if conn.status == ConnectionStatusEnum.pending:
                return "Connection request already created by the other user.", 400
            else:
                return "Connection already established.", 400

        # Creates a connection request.
        connection_request = Connection(
            user_1_id=this_user.id,
            user_2_id=other_user.id,
            status=ConnectionStatusEnum.pending,
        )
        db.session.add(connection_request)
        db.session.commit()

        # Push to client connection request created.
        socket.emit_conn_request(this_user)
        socket.emit_conn_request(other_user)

        return "Created.", 201

    # Elevates a connection request status to an accepted established connection
    update_connection_parser = reqparse.RequestParser()
    update_connection_parser.add_argument("email", required=True)

    @api.expect(update_connection_parser)
    @api.doc(
        responses={
            200: "Connection accepted.",
            304: "Connection already established.",
            400: "Connection request not found.",
            400: "Requested user not found.",
            401: "Unauthorized.",
        },
        description="Accepts the incoming connection request made by the email.",
    )
    @jwt_required()
    def put(self):
        """
        Accept an incoming connection request made by the email specified
        """
        args = self.request_connection_parser.parse_args(strict=True)

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()
        other_user = User.query.filter_by(email=args.email).first()

        # Checks if the requested user is found.
        if other_user is None:
            return "Requested user not found.", 400

        # Checks if connection request exists.
        connection_request = Connection.query.filter_by(
            user_1_id=other_user.id, user_2_id=this_user.id
        ).first()
        print(f"from {other_user.name} to {this_user.name}")
        if connection_request is None:
            return "Connection request not found.", 400

        # Checks if connection already established.
        if connection_request.status == ConnectionStatusEnum.accepted:
            return "Connection already established.", 400

        # Accept the incoming connection request.
        connection_request.status = ConnectionStatusEnum.accepted
        db.session.commit()

        # Push to client connection request accepted.
        socket.emit_conn(this_user)
        socket.emit_conn(other_user)

        return "Connection accepted.", 200

    delete_connection_parser = reqparse.RequestParser()
    delete_connection_parser.add_argument("email", required=True)

    @api.expect(delete_connection_parser)
    @api.doc(
        responses={
            200: "Successful Deletion!",
            400: "Connection request not found.",
            400: "Requested user not found.",
            401: "Unauthorized.",
        },
        description="Deletes an incoming or outgoing connection request by the email specified.",
    )
    @jwt_required()
    def delete(self):
        """
        Deletes an incoming or outgoing connection request
        """
        args = self.delete_connection_parser.parse_args()

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()
        other_user = User.query.filter_by(email=args.email).first()

        if other_user is None:
            return "Requested user not found.", 400

        user_id = this_user.id
        other_id = other_user.id
        # Filter for both users assuming duplicate entries AND connection is pending.

        connection_request = None
        for request_list in [
            this_user.incoming_connection_requests,
            this_user.outgoing_connection_requests,
        ]:
            for request in request_list:
                if (request.user_1_id == user_id and request.user_2_id == other_id) or (
                    request.user_1_id == other_id and request.user_2_id == user_id
                ):
                    connection_request = request
                    break

        if not connection_request:
            return "Connection request not found.", 400

        db.session.delete(connection_request)
        db.session.commit()

        return "Successful Deletion!", 200

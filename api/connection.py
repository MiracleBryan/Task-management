from flask_restx import reqparse, Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import User, Connection
from database.db import db
from sqlalchemy import or_

import api.socket_events as socket

api = Namespace("connection", desc="Connection endpoints")


@api.route("")
class ConnectionResource(Resource):
    # Gets all established connections of a user
    @api.doc(
        responses={
            200: "Connection List.",
            401: "Unauthorized.",
        },
        description="Get established connections.",
    )
    @jwt_required()
    def get(self):
        """
        Get established connections
        """
        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        return {
            "Connections": [
                c.user_1.parse() if c.user_2.email == email else c.user_2.parse()
                for c in this_user.connected
            ]
        }, 200

    # Deletes a connection
    # TODO: Delete established user connection.
    delete_connection_parser = reqparse.RequestParser()
    delete_connection_parser.add_argument("email", required=True)

    @api.expect(delete_connection_parser)
    @api.doc(
        responses={
            200: "Connection deleted.",
            400: "Connection request not found.",
            400: "Requested user not found.",
            401: "Unauthorized.",
        },
        description="Accepts the incoming connection request made by the email.",
    )
    @jwt_required()
    def delete(self):
        """
        Deletes an established connection
        """
        args = self.delete_connection_parser.parse_args(strict=True)
        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()
        other_user = User.query.filter_by(email=args.email).first()

        if other_user is None:
            return "Requested user not found.", 400

        other_id = other_user.id
        # Filter for both users assuming duplicate entries AND connection is accepted.
        connection = this_user.connected.filter(
            or_(Connection.user_1_id == other_id, Connection.user_2_id == other_id)
        ).first()

        if not connection:
            return "Connection not found.", 400

        db.session.delete(connection)
        db.session.commit()

        # Push to client established connection deleted.
        socket.emit_conn(this_user)
        socket.emit_conn(other_user)

        return "Successful Deletion!", 200

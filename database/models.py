from .db import db

from sqlalchemy import and_, or_
import enum


class TaskStatusEnum(enum.Enum):
    not_started = 0
    in_progress = 1
    blocked = 2
    completed = 3


class ConnectionStatusEnum(enum.Enum):
    pending = 0
    accepted = 1


class Connection(db.Model):
    __tablename__ = "Connection"
    user_1_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    user_2_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    status = db.Column(
        db.Enum(ConnectionStatusEnum), default=ConnectionStatusEnum.pending
    )
    user_1 = db.relationship("User", foreign_keys=user_1_id, lazy=True)
    user_2 = db.relationship("User", foreign_keys=user_2_id, lazy=True)


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(50), nullable=True)
    linkedin = db.Column(db.String(50), nullable=True)
    picture = db.Column(db.String(50), nullable=True)
    tasks = db.relationship(
        "Task",
        primaryjoin="or_(Task.owner==User.id, " "Task.creator==User.id)",
        lazy=True,
    )
    connected = db.relationship(
        Connection,
        primaryjoin=lambda: and_(
            Connection.status == ConnectionStatusEnum.accepted,
            or_(User.id == Connection.user_1_id, User.id == Connection.user_2_id),
        ),
        viewonly=True,
        lazy="dynamic",
    )
    incoming_connection_requests = db.relationship(
        Connection,
        primaryjoin=lambda: and_(
            Connection.status == ConnectionStatusEnum.pending,
            User.id == Connection.user_2_id,
        ),
        viewonly=True,
        lazy=True,
    )
    outgoing_connection_requests = db.relationship(
        Connection,
        primaryjoin=lambda: and_(
            Connection.status == ConnectionStatusEnum.pending,
            User.id == Connection.user_1_id,
        ),
        viewonly=True,
        lazy=True,
    )

    # Check if is connected to the other_user. Return true if connected, false otherwise.
    def is_connected_to(self, other_user):
        # If connected return True.
        for c in self.connected:
            if c.user_1.email == other_user.email or c.user_2.email == other_user.email:
                return True

        return False

    # Parse public profile
    def parse(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "mobile": self.mobile,
            "linkedin": self.linkedin,
            "picture": self.picture,
        }

    # Parse private profile
    def parse_private(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "picture": self.picture,
        }


class Task(db.Model):
    __tablename__ = "Task"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    title = db.Column(db.String(50))
    description = db.Column(db.String)
    deadline = db.Column(db.Date)
    date_completed = db.Column(db.Date)
    estimated_time = db.Column(db.Integer)
    status = db.Column(db.Enum(TaskStatusEnum), default=TaskStatusEnum.not_started)
    owner_user = db.relationship(
        "User", foreign_keys=owner, back_populates="tasks", lazy=True
    )
    creator_user = db.relationship(
        "User", foreign_keys=creator, back_populates="tasks", lazy=True
    )


# Initialize database's application.
# Create database from Model defined above if needed.
def init_app_database(app, create_db_from_model=False):
    db.init_app(app)
    if create_db_from_model:
        with app.app_context():
            db.create_all()

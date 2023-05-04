from flask_restx import reqparse, Resource, Namespace
from flask_jwt_extended import get_jwt_identity, jwt_required
import datetime
from flask import jsonify

from database.models import Task, User, TaskStatusEnum
from database.db import db

api = Namespace("task", desc="Task endpoints")

date_format = "%d %b %Y"


# A list of tasks resource.
@api.route("")
class TaskListResource(Resource):
    # Gets a list of tasks of a user.
    get_tasks_parser = reqparse.RequestParser()
    get_tasks_parser.add_argument("user_id", type=int, required=False)

    @api.expect(get_tasks_parser)
    @api.doc(
        responses={200: "Success.", 404: "Not connected to user."},
        description="Gets a list of tasks.",
    )
    @jwt_required()
    def get(self):
        """
        Gets a list of tasks
        """
        args = self.get_tasks_parser.parse_args()
        query_user_id = args["user_id"]  # The query user id

        # This user
        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        # The queried user
        query_user = None
        if query_user_id is not None:
            query_user = User.query.filter_by(id=query_user_id).first()

            # Query user is found and is not connected to the current user.
            if (
                query_user is not None
                and (this_user != query_user)
                and not this_user.is_connected_to(query_user)
            ):
                return "Not connected to user.", 404

        if query_user is None:
            query_user = this_user

        task_list = []
        for task in query_user.tasks:
            # Do not return task if user is already disconnected.
            if query_user != task.owner_user and not query_user.is_connected_to(
                task.owner_user
            ):
                continue
            task_list.append(
                {
                    "id": task.id,
                    "owner": task.owner,
                    "owner_name": task.owner_user.name,
                    "owner_email": task.owner_user.email,
                    "creator": task.creator,
                    "creator_name": task.creator_user.name,
                    "creator_email": task.creator_user.email,
                    "title": task.title,
                    "description": task.description,
                    "date_completed": (
                        task.date_completed.strftime(date_format)
                        if task.date_completed
                        else ""
                    ),
                    "deadline": (
                        task.deadline.strftime(date_format) if task.deadline else ""
                    ),
                    "estimated_time": task.estimated_time,
                    "status": task.status.name,
                }
            )

        return {"TaskList": task_list}, 200

    # Creates a Task and add it to this task list.
    create_task_parser = reqparse.RequestParser()
    create_task_parser.add_argument("title", required=True)
    create_task_parser.add_argument("owner", required=False)
    create_task_parser.add_argument("description", required=False)
    create_task_parser.add_argument("deadline", required=False)
    create_task_parser.add_argument("date_completed", required=False)
    create_task_parser.add_argument("estimated_time", required=False)
    create_task_parser.add_argument("status", required=False)

    @api.expect(create_task_parser)
    @api.doc(
        responses={
            201: "Task ID",
            401: "Unauthorized.",
        },
        description="Creates a new task.",
    )
    @jwt_required()
    def post(self):
        """
        Creates a new task
        """
        args = self.create_task_parser.parse_args(strict=True)

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        if args.owner:
            owner_user = User.query.filter_by(email=args.owner).first()
            if owner_user is None:  # Fallback to this user.
                owner_user = this_user
        else:
            owner_user = this_user

        if not args.status:
            args.status = TaskStatusEnum.not_started

        deadline = (
            datetime.datetime.strptime(args.deadline, date_format).date()
            if args.deadline
            else None
        )

        date_completed = (
            datetime.datetime.strptime(args.date_completed, date_format).date()
            if args.date_completed
            else None
        )

        task = Task(
            owner=owner_user.id,
            creator=this_user.id,
            title=args.title,
            description=args.description,
            deadline=deadline,
            date_completed=date_completed,
            estimated_time=args.estimated_time,
            status=args.status,
        )
        db.session.add(task)
        db.session.commit()
        return {
            "Task": {
                "id": task.id,
                "owner": task.owner,
                "creator": task.creator,
                "creator_email": task.creator_user.email,
                "owner_name": task.owner_user.name,
                "owner_email": task.owner_user.email,
                "creator": task.creator,
                "creator_name": task.creator_user.name,
                "title": task.title,
                "description": task.description,
                "deadline": (
                    task.deadline.strftime(date_format) if task.deadline else ""
                ),
                "date_completed": (
                    task.date_completed.strftime(date_format)
                    if task.date_completed
                    else ""
                ),
                "estimated_time": task.estimated_time,
                "status": task.status.name,
            }
        }, 201

    # Deletes a list of selected tasks given its ID.
    delete_tasks_parser = reqparse.RequestParser()
    delete_tasks_parser.add_argument("id", type=int, action="append", required=True)

    @api.expect(delete_tasks_parser)
    @api.doc(
        responses={200: "Deleted.", 404: "Task not found."},
        description="Deletes multiple tasks in the task list ID.",
    )
    @jwt_required()
    def delete(self):
        """
        Deletes multiple tasks from the task list
        """

        args = self.delete_tasks_parser.parse_args(strict=True)
        task_ids = args["id"]

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        # Do not allow delete more than 500.
        if len(task_ids) > 500:
            return "Task not found", 404

        tasks = [Task.query.filter_by(id=id).first() for id in task_ids]

        # Do not allow other users to delete my task!
        for task in tasks:
            if task is None:
                continue
            if task.owner != this_user.id and task.creator != this_user.id:
                return "Task not found", 404
            else:
                db.session.delete(task)

        db.session.commit()

        return "Deleted.", 200


# A task resource.
@api.route("/<int:id>")
class TaskResource(Resource):
    # Gets a Task based on its ID.
    @api.doc(
        responses={200: "Success.", 404: "Task not found."},
        description="Gets task information based on ID.",
    )
    @jwt_required()
    def get(self, id):
        """
        Gets task information based on ID
        """
        task = Task.query.filter_by(id=id).first()
        if task:
            return {
                "Task": {
                    "id": task.id,
                    "owner": task.owner,
                    "creator": task.creator,
                    "title": task.title,
                    "description": task.description,
                    "deadline": (
                        task.deadline.strftime(date_format) if task.deadline else ""
                    ),
                    "date_completed": (
                        task.date_completed.strftime(date_format)
                        if task.date_completed
                        else ""
                    ),
                    "estimated_time": task.estimated_time,
                    "status": task.status.name,
                }
            }
        else:
            return "Task not found", 404

    # Updates a Task details based on its ID.
    update_task_parser = reqparse.RequestParser()
    update_task_parser.add_argument("title", required=True)
    update_task_parser.add_argument("owner_email", required=True)
    update_task_parser.add_argument("description", required=True)
    update_task_parser.add_argument("deadline", required=True)
    update_task_parser.add_argument("date_completed", required=True)
    update_task_parser.add_argument("estimated_time", required=True)
    update_task_parser.add_argument("status", required=True)

    @api.expect(update_task_parser)
    @api.doc(
        responses={
            200: "Updated.",
            400: "Not connected to the assigned owner.",
            404: "Owner not found.",
            404: "Task not found.",
        },
        description="Updates a task.",
    )
    @jwt_required()
    # TODO: Check if the owner assigned is assigned by a legitimate connection.
    def put(self, id):
        """
        Updates a task
        """
        args = self.update_task_parser.parse_args()
        task = Task.query.filter_by(id=id).first()

        if task is None:
            return "Task not found.", 404

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        owner_user = User.query.filter_by(email=args.owner_email).first()

        if owner_user is None:
            return "Owner not found.", 404

        # If trying to assign owner to another user, ensure the other user is in this user's established connection.
        if owner_user != this_user:
            if not this_user.is_connected_to(owner_user):
                return f"Already not connected with {owner_user.name}", 400

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        # Do not allow other users to update my task!
        if task.owner != this_user.id and task.creator != this_user.id:
            return "Task not found", 404

        task.title = args.title
        task.owner = owner_user.id
        task.description = args.description
        deadline = (
            datetime.datetime.strptime(args.deadline, date_format).date()
            if args.deadline
            else None
        )
        task.deadline = deadline
        date_completed = (
            datetime.datetime.strptime(args.date_completed, date_format).date()
            if args.date_completed
            else None
        )
        task.date_completed = date_completed
        task.estimated_time = args.estimated_time
        task.status = args.status

        db.session.commit()

        return "Updated.", 200

    # Deletes a Task given its ID.
    @api.doc(
        responses={200: "Deleted.", 404: "Task not found."},
        description="Deletes a task.",
    )
    def delete(self, id):
        """
        Deletes a task
        """

        email = get_jwt_identity()
        this_user = User.query.filter_by(email=email).first()

        task = Task.query.filter_by(id=id).first()

        if not task:
            return "Task not found", 404

        # Do not allow other users to delete my task!
        if task.owner != this_user.id and task.creator != this_user.id:
            return "Task not found", 404

        db.session.delete(task)
        db.session.commit()

        return "Deleted.", 200

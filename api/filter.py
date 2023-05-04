from flask_restx import reqparse, Resource, Namespace
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, get_jwt_identity

from database.models import User, Task
from database.db import db
import datetime 

date_format = '%d %b %Y'
api = Namespace("filter", desc="Filter endpoints")
        
@api.route("")
class FilterResource(Resource):
    # Filter Information
    filter_user_parser = reqparse.RequestParser()
    filter_user_parser.add_argument("status", type=str, required=False)
    filter_user_parser.add_argument("deadline", type=str, required=False)
    filter_user_parser.add_argument("title", type=str, required=False)
    filter_user_parser.add_argument("description", type=str, required=False)
    filter_user_parser.add_argument("id", type=int, required=False)
    filter_user_parser.add_argument("estimated_time", type=int, required=False)
    @api.expect(filter_user_parser)
    @api.doc(responses={
        200: "Successful Return.",
        401: "Unauthorized."
    }, description="Filter based on Get request")
    @jwt_required()
    def get(self):
        """
        Filter
        """
        args = self.filter_user_parser.parse_args()

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        #Get all tasks from user
        task_query = Task.query.filter(Task.owner == user.id)

        task_filter = args.get('title')
        if task_filter is not None: 
            task_query = task_query.filter(Task.title.ilike(f'%{task_filter}%'))

        deadline_filter = args.get('deadline')
        if deadline_filter is not None: 
            deadline = datetime.datetime.strptime(deadline_filter, '%Y-%m-%d').date()
            task_query = task_query.filter(Task.deadline == deadline)


        status_filter = args.get('status')
        if status_filter is not None: 
            task_query = task_query.filter(Task.status == status_filter)

        
        description_filter = args.get('description')
        if description_filter is not None: 
            task_query = task_query.filter(Task.description.ilike(f'%{description_filter}%'))

        id_filter = args.get('id')
        if id_filter is not None: 
            task_query = task_query.filter(Task.id == id_filter)

        estimated_time_filter = args.get('estimated_time')
        if estimated_time_filter is not None: 
            task_query = task_query.filter(Task.estimated_time == estimated_time_filter)
        

        tasks = task_query.all()

        return  {
                "FilteredList" :  [{
                    "id" : task.id,
                    "owner": task.owner,
                    "owner_name": task.owner_user.name,
                    "owner_email": task.owner_user.email,
                    "creator" : task.creator,
                    "creator_name": task.creator_user.name,
                    "creator_email" : task.creator_user.email,
                    "title" : task.title,
                    "description" : task.description,
                    "deadline" : (task.deadline.strftime(date_format) if task.deadline else ""),
                    "status" : task.status.name,
                    "estimated_time" : task.estimated_time
                } for task in tasks]
            }, 200
    

# if name_filter:
        #     user_tasks = user.tasks
        #     for task in user_tasks:
        #         #Assume what is queried is same as title.
        #         if task.title == name_filter:
        #             if name_filter in return_object:
        #                 return_object[name_filter].append(task)
        #             else:
        #                 return_object[name_filter] = [task]
        
        # if deadline_filter: 
        #     user_tasks = user.tasks
        #     for task in user_tasks: 
        #         #Assume what is queried is same as deadline 
        #         if task.deadline.strftime(date_format) == deadline_filter:
        #             if deadline_filter in return_object:
        #                 return_object[deadline_filter].append(task)
        #             else:
        #                 return_object[deadline_filter] = [task]

        # if status_filter:
        #     user_tasks = user.tasks
        #     for task in user_tasks: 
        #         #Follow task.py formate 
        #         if task.status.name == status_filter:
        #             if status_filter in return_object:
        #                 return_object[status_filter].append(task)
        #             else:
        #                 return_object[status_filter] = [task]
        
        # if description_filter:
        #     user_tasks = user.tasks
        #     for task in user_tasks: 
        #         #Follow task.py formate 
        #         if task.id == id_filter:
        #             if id_filter in return_object:
        #                 return_object[id_filter].append(task)
        #             else:
        #                 return_object[id_filter] = [task]

        # if id_filter:
        #     user_tasks = user.tasks
        #     for task in user_tasks: 
        #         #Follow task.py formate 
        #         if task.id == id_filter:
        #             if id_filter in return_object:
        #                 return_object[id_filter].append(task)
        #             else:
        #                 return_object[id_filter] = [task]
    
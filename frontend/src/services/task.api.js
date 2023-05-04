import { BaseAPI } from './base.api'

class TaskAPI extends BaseAPI {
    async get_tasks(user_id) {
        const params = {}
        if (user_id !== undefined) {
            params['user_id'] = user_id
        }
        return this.api.get('/task', { params })
    }

    async update_task(task) {
        return this.api.put(`/task/${task.id}`, task)
    }

    async add_task(task) {
        return this.api.post(`/task`, task)
    }

    async delete_tasks(task_ids) {
        let s = task_ids.reduce((p, c) => {
            p += `id=${c}&`
            return p
        }, "").slice(0, -1)
        return this.api.delete(`/task?${s}`)
    }
};

export default new TaskAPI();
import { BaseAPI } from './base.api'

class UserAPI extends BaseAPI {
    async login(email, password) {
        return this.api.post('/user/login', { email: email, password: password })
    }

    async get_user(user_id) {
        const params = {}
        if (user_id !== undefined) {
            params['user_id'] = user_id
        }
        return this.api.get('/user', { params })
    }

    async update_user(user) {
        return this.api.put('/user', user)
    }

    async register(name, email, password) {
        return this.api.post('/user', { name: name, email: email, password: password })
    }

    async update_user_image(image_filename) {
        const form_data = new FormData()
        form_data.append("file", image_filename)
        return this.api.post('/user/picture', form_data, { headers: { 'accept': 'application/json', 'Content-Type': 'multipart/form-data' } })
    }

    async logout() {
        return this.api.post('/user/logout')
    }
};

export default new UserAPI();
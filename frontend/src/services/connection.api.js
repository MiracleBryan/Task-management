import { BaseAPI } from './base.api'

class ConnectionAPI extends BaseAPI {
    async get_connection() {
        return this.api.get('/connection')
    }

    async delete_connection(email) {
        return this.api.delete(`/connection?email=${encodeURIComponent(email)}`)
    }
};

export default new ConnectionAPI();
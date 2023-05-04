import { BaseAPI } from './base.api'

class ConnectionRequestAPI extends BaseAPI {
    async get_connection_requests() {
        return this.api.get('/connectionrequest')
    }

    async send_connection_request(email) {
        return this.api.post('/connectionrequest', { email: email })
    }

    async accept_connection_request(email) {
        return this.api.put('/connectionrequest', { email: email })
    }

    async delete_connection_request(email) {
        return this.api.delete(`/connectionrequest?email=${encodeURIComponent(email)}`)
    }
};

export default new ConnectionRequestAPI();
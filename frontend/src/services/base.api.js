import axios from 'axios'
import { get_api_url } from './utils'
import { get_access_token_attr_key } from 'src/utils/local_storage_utils'

// raw data deal with api
export class BaseAPI {
    constructor() {
        this.api = axios.create({
            baseURL: get_api_url(),
            withCredentials: true,
            headers: this.get_auth_headers()
        })
    }

    refresh_auth_headers() {
        this.api.defaults.headers = this.get_auth_headers()
    }

    get_auth_headers() {
        return { Authorization: `Bearer ${localStorage.getItem(get_access_token_attr_key())}` }
    }
}
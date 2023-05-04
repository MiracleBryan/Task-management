import io from 'socket.io-client'
import { useAppStore } from 'src/stores/AppStore'
import { get_access_token_attr_key, is_authenticated } from 'src/utils/local_storage_utils'

// Creates socket and ties to store
class SocketFactory {
    create_socket(store) {
        if (is_authenticated()) {
            const socket = io.connect(process.env.SOCKET_API, {
                extraHeaders: {
                    "Authentication": `Bearer ${localStorage.getItem(get_access_token_attr_key())}`
                }
            })
            this.bind(socket, store)
            return socket
        }
        return null
    }

    bind(socket, store) {
        socket.on("message", m => {
            console.log(`Received: ${m} `)
        })

        socket.on("connection requests", m => store.set_connection_requests(m))
        socket.on("connection", m => store.set_connection(m))
    }
}

function initialize_socket() {
    const factory = new SocketFactory()
    const store = useAppStore()
    factory.create_socket(store)
}

export { initialize_socket }
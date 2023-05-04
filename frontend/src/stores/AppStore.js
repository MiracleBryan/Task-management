import { defineStore } from 'pinia';
import { toRaw } from 'vue';

export const useAppStore = defineStore('app', {
  state: () => ({
    connection_requests: {
      "IncomingConnection": [],
      "OutgoingConnection": []
    },
    connections: {
      "Connections": []
    },
    user: {},
    viewing_user: null,
    tasks_dirty: false,
  }),

  getters: {
    incoming_connection(state) {
      return state.connection_requests["IncomingConnection"]
    },
    connection(state) {
      return state.connections["Connections"]
    },
    user_readonly(state) {
      if (state.user && state.viewing_user) {
        return state.user["id"] != state.viewing_user["id"]
      }
      return true
    },
  },

  actions: {
    set_connection_requests(v) {
      this.connection_requests = v
    },
    set_connection(v) {
      this.connections = v
    },
    delete_connection(v) {
      const conn = toRaw(this.connections["Connections"])
      const idx = conn.findIndex(c => c.email == v)
      if (idx == -1) return
      conn.splice(idx, 1)
      this.connections = { "Connections": conn }
    },
    delete_connection_request(i) {
      this.connection_requests["IncomingConnection"].splice(i, 1)
    },
    set_user(v) {
      this.user = v
    },
    set_viewing_user(v) {
      this.viewing_user = v
    },
    reset_viewing_user() {
      this.viewing_user = null
    },
    invalidate_tasks() {
      this.tasks_dirty = true
    }
  },
})

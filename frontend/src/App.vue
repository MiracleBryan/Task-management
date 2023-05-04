<template>
  <router-view />
</template>

<script>
import { initialize_socket } from 'src/services/socket/socket'
import AuthAPI from 'src/services/user.api.js';
import { useAppStore } from 'src/stores/AppStore'
import { defineComponent } from 'vue'
import { is_authenticated } from 'src/utils/local_storage_utils'

export default defineComponent({
  name: 'App',
  created() {
    // Initialize socket
    initialize_socket()

    // Initialize user
    if (is_authenticated()) {
      AuthAPI.get_user()
        .then(res => {
          const store = useAppStore()
          store.set_user(res.data)
        })
    }
  }
})
</script>

<template>
    <q-page>
        <div class="task_page outside bg-indigo-1 row" style="min-height: inherit">
            <div class="task_page_list_container outside bg-white"
                style="display:flex; flex-direction: column; justify-content:left; align-items: start; width:99%; border-top-right-radius:11px; overflow:auto">

                <!-- If viewing user, view the user's task list. -->
                <template v-if="viewing_user">
                    <h5 class="task_list_name text-grey-9">Task List 📖</h5>

                    <hr class="separator" style="border: 0px; margin-bottom: 1em">

                    <TaskList :user_id="viewing_user['id']" :readonly="task_list_readonly"></TaskList>
                </template>

                <!-- Error Messages if user not found etc. -->
                <div v-else class="error_message text-grey-8 text-h6 q-pt-xl">
                    <span>{{ error_message }}</span>
                    <div v-if="add_user" class="q-mt-md">
                        <span class="q-mr-lg">Send add request?</span>
                        <q-btn @click="send_request" class="bg-indigo-5 text-white" no-caps><q-icon name="person_add"
                                class="q-pr-sm" />Send
                            Request</q-btn>
                    </div>
                </div>
            </div>
        </div>
    </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useAppStore } from 'src/stores/AppStore'
import AuthAPI from 'src/services/user.api.js'
import ConnReqAPI from 'src/services/connection_request.api.js'
import TaskList from 'src/components/task/TaskList.vue'

export default defineComponent({
    components: {
        TaskList,
    },
    data() {
        return {
            error_message: "",
            add_user: null,
        }
    },
    created() {
        // Replace the path to include the user's id if not included.
        if (this.$route.query.user == undefined) {
            this.$router.replace({ path: this.$route.path, query: { user: this.user.id } })
        }

        this.update_query_user()
    },
    watch: {
        // Set current user from the route query.
        "$route.query": {
            immediate: true,
            handler(new_value, old_value) {
                if (old_value == undefined) return
                this.update_query_user()
            }
        },
    },
    computed: {
        task_list_readonly() {
            return useAppStore().user_readonly
        },

        viewing_user() {
            return useAppStore().viewing_user
        },

        user() {
            return useAppStore().user
        }
    },
    methods: {
        // The current viewing user of the task list.
        update_query_user() {
            const user_id = this.$route.query.user
            AuthAPI.get_user(user_id)
                .then(res => {
                    const store = useAppStore()
                    store.set_viewing_user(res.data)

                    // Clear errors
                    this.clear_errors()
                })
                .catch(e => {
                    const err_msg = e.response.data.error
                    const store = useAppStore()
                    if (err_msg == "Not connected.") { // Not connected to the user.
                        const stranger_user = e.response.data.user
                        this.error_message = `Not connected to ${stranger_user.name}.`
                        this.add_user = stranger_user

                        const store = useAppStore()
                        store.set_viewing_user(stranger_user)
                    } else { // User is not found or bad request.
                        this.error_message = "User not found. 😥"
                        this.add_user = null
                    }
                    // Reset the viewing user.
                    store.reset_viewing_user()
                })
        },

        // Clear errors
        clear_errors() {
            this.error_message = ""
            this.add_user = null
        },

        // Add stranger user
        send_request() {
            ConnReqAPI.send_connection_request(this.add_user.email)
                .then(() => {
                    this.$q.notify({
                        message: `Sent request to ${this.add_user.email}`,
                        icon: 'o_person_add',
                        position: 'bottom-right',
                        color: 'primary'
                    })
                    this.email = ''
                })
                .catch(e => {
                    const error_msg = e.response.data
                    this.$q.notify({
                        message: error_msg,
                        icon: 'o_person_add_disabled',
                        position: 'bottom-right',
                        color: 'pink-5'
                    })
                })
        }
    }
})
</script>

<style scoped lang="scss">
.task_page {
    transition: background-color 0.35s ease;
}

.task_page_list_container {
    padding: 0 40px;
    transition: background-color 0.35s ease;
}

.task_list_name {
    margin-bottom: 0;
}


// Dark Mode
.body--dark {
    .task_page {
        background-color: $dark !important;
    }

    .task_list_name {
        color: $blue-2 !important;
    }

    .task_page_list_container {
        background-color: $dark-2 !important;
        border: 1px solid $dark-bg-fill-2;
        border-bottom: none;
        border-left: none;
    }

    // .separator {
    //     border: 1px solid $grey-5 !important;
    // }

    .error_message {
        color: $grey-5 !important;
    }
}

// Responsive
@media (max-width: 600px) {
    .task_page_list_container {
        width: 100% !important;
        border-top-right-radius: 0 !important;
        padding: 0 10px;
    }

    .task_list_name {
        margin-top: 1em;
    }

    // .separator {
    //     min-width: 0 !important;
    //     width: 9vw !important;
    // }
}
</style>
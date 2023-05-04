<template>
    <div class="q-mt-xs" v-if="connection.length > 0">
        <div v-for="user in connection" :key="user.id"
            class="connection flex items-center cursor-pointer q-pl-md q-pt-sm relative-position" v-ripple
            @click="show_profile(user)">

            <!-- Profile Picture -->
            <q-avatar size="43px" color="grey-2" class="q-mb-sm">
                <img v-if="user.picture" :src="image_path(user.picture)" />
                <q-icon v-else color="grey-8" size="43px" name="face" />
            </q-avatar>

            <div class="q-ml-md q-pb-xs text-bold relative-position">{{ user.name }}</div>
        </div>
        <q-separator class="q-mx-md q-mt-sm"></q-separator>

        <!-- Readonly Profile Details -->
        <ProfileDetails :user_prop="user" :readonly="true" ref="profile">
            <!-- Extra Actions -->
            <q-card-actions class="row justify-between">
                <!-- View Profile -->
                <q-btn color="indigo-5" no-caps @click="view_profile">
                    <q-icon name="assignment" class="q-pr-sm" />
                    View Profile
                </q-btn>

                <!-- Unfriend -->
                <q-btn outline dense color="red-8" no-caps icon="person_remove" @click="disconnect_confirmation">
                    <q-tooltip class="bg-red" anchor="top middle" self="center middle">
                        unfriend
                    </q-tooltip>
                </q-btn>
            </q-card-actions>
        </ProfileDetails>

        <!-- Disconnect Confirmation Dialog -->
        <q-dialog v-model="show_disconnect_confirmation">
            <q-card class="column justify-between" style="width: 450px; min-height: 200px">
                <q-card-section>
                    <div class="text-h6 text-red-7 row items-center">
                        <span class="q-mr-sm">Unfriend {{ user.name }}</span>
                    </div>
                </q-card-section>

                <q-card-section class="q-pt-none" style="min-width: 400px">
                    Are you sure you want to remove {{ user.name }} as your friend?
                </q-card-section>

                <!-- Confirm Delete Button -->
                <q-card-actions align="right">
                    <q-btn no-caps flat label="Unfriend" color="red-6" @click="disconnect" v-close-popup />
                </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
</template>

<script>
import ConnAPI from 'src/services/connection.api.js'
import { useAppStore } from 'src/stores/AppStore'
import ProfileDetails from '../profile/ProfileDetails.vue'
import { get_base_url } from 'src/services/utils.js'

export default ({
    components: {
        ProfileDetails
    },
    data() {
        return {
            user: null,
            show_disconnect_confirmation: false,
        }
    },
    computed: {
        connection() {
            return useAppStore().connection
        },
    },
    created() {
        // Initialize store
        ConnAPI.get_connection()
            .then(res => {
                useAppStore().set_connection(res.data)
            })
            .catch(e => {
                console.log(e)
            })
    },
    methods: {
        // Show Profile Details
        show_profile(user) {
            this.user = user
            this.$nextTick(_ => this.$refs.profile.show_profile())
        },

        // Disconnect confirmation dialog
        disconnect_confirmation() {
            this.show_disconnect_confirmation = true
        },

        // Disconnect user
        disconnect() {
            const email = this.user.email
            ConnAPI.delete_connection(email)
                .then(() => {
                    // Deletes the connection off.
                    useAppStore().delete_connection(email)
                    // Notify user is unfriended.
                    this.$q.notify({
                        message: `Unfriended ${this.user.name}`,
                        icon: 'person_remove',
                        position: 'bottom-right',
                        color: 'red-7'
                    })

                    // // This is kinda annoying...... Refresh the entire list just after disconnection? :(
                    // // Task list is now dirty, invalidate.
                    // useAppStore().invalidate_tasks()
                })
            this.display = false
            this.show_disconnect_confirmation = false
        },

        // View tasks and profile of the user
        view_profile() {
            this.$router.push({ path: this.$route.path, query: { user: this.user.id } })
        },

        // Image path
        image_path(path) {
            return `${get_base_url()}/${path}`
        }
    }
})
</script>

<style scoped lang="scss">
// Dark Mode
.body--dark {
    .connection {
        &:hover {
            background-color: $dark-bg-fill-2;
        }
    }
}

// Light Mode
.body--light {
    .connection {
        &:hover {
            background-color: hsl(230, 15%, 95%);
        }
    }
}

.connection {
    border-radius: 6px;
}
</style>
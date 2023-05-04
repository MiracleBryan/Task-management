<template>
    <q-img style="height: 100px; border-top-left-radius: 11px; margin-bottom: 0.7em">
        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
            <!-- Profile Component Container -->
            <div class="bg-transparent text-grey-8 q-my-md full-width">
                <div class="flex row justify-between">

                    <!-- Profile Section -->
                    <div class="profile_section flex row cursor-pointer items-center"
                        @click="this.$refs.prof_details.show_profile()">
                        <!-- Profile Picture -->
                        <q-btn round color="grey-2" class="profile_avatar q-mr-md q-ml-sm">
                            <q-avatar size="50px" color="none">
                                <img v-if="user.picture" :src="image_url" />
                                <q-icon v-else color="grey-8" size="50px" name="face" />
                            </q-avatar>
                        </q-btn>

                        <!-- Name -->
                        <div class="profile_name text-grey-10 text-weight-bold">{{ user.name }}</div>
                        <ProfileDetails :user_prop="user" :readonly="readonly" @update_user="update_user"
                            ref="prof_details" />
                    </div>

                    <!-- Notification Section -->
                    <div class="self-end q-pb-xs">
                        <!-- Notifications Button -->
                        <q-btn round flat icon="o_notifications" class="noti_button" @click="not_seen_notification = false">
                            <div v-show="request_count > 0 && not_seen_notification" class="absolute noti_count"
                                style="right: 0; top: 25px; opacity: 0.4">
                                <q-badge color="red" floating transparent>
                                    {{ request_count }}
                                </q-badge>
                            </div>
                            <!-- Connection Request Notifications -->
                            <q-menu fit :offset="[10, 20]" style="width: 225px" transition-show="jump-down"
                                transition-hide="jump-up">
                                <div class="flex column q-pt-md">
                                    <div v-if="request_count > 0">
                                        <span class="q-ml-md q-mb-md text-bold">Connection Requests</span>
                                        <div v-for="(request, index) in incoming_requests" :key="request.name"
                                            class="flex column items-center justify-center q-mb-lg q-mt-md">

                                            <!-- Profile Picture -->
                                            <q-avatar v-if="request.picture" size="43px" color="none">
                                                <img :src="image_path(request.picture)" />
                                            </q-avatar>
                                            <q-avatar v-else size="43px" color="grey-2">
                                                <q-icon color="grey-8" size="xl" name="face"></q-icon>
                                            </q-avatar>

                                            <!-- Requester's UserName -->
                                            <div class="q-mt-xs">
                                                <span>
                                                    {{ request.name }}
                                                </span>
                                                <span class="text-weight-light">
                                                    wants to connect.
                                                </span>
                                            </div>

                                            <!-- Accept / Decline Request -->
                                            <div class="flex justify-between no-wrap q-mt-sm">
                                                <q-btn flat class="text-white bg-blue-8 q-mr-md" no-caps
                                                    @click="accept_connection_request(request.email, request.name, index)">Confirm</q-btn>
                                                <q-btn filled flat class="text-black bg-grey-2" no-caps
                                                    @click="delete_connection_request(request.email, index)">Delete</q-btn>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else class="flex row justify-center items-center q-mb-md text-grey-7">
                                        <span class="q-mr-sm q-pt-xs">No Notifications</span>
                                        <q-icon name="o_mood" size="1.5em"></q-icon>
                                    </div>
                                </div>
                            </q-menu>
                        </q-btn>
                    </div>
                </div>
            </div>
        </transition>
    </q-img>
</template>

<script>
import ConnReqAPI from 'src/services/connection_request.api.js'
import { useAppStore } from 'src/stores/AppStore'
import ProfileDetails from 'src/components/profile/ProfileDetails.vue'
import { get_base_url } from 'src/services/utils.js'

export default ({
    components: {
        ProfileDetails
    },
    data() {
        return {
            not_seen_notification: true,
        }
    },
    computed: {
        request_count() {
            return this.incoming_requests.length
        },
        incoming_requests() {
            return useAppStore().incoming_connection
        },
        user() {
            return useAppStore().viewing_user
        },
        readonly() {
            return useAppStore().user_readonly
        },
        image_url() {
            return `${get_base_url()}/${this.user.picture}`
        }
    },
    watch: {
        request_count() {
            this.not_seen_notification = true
        }
    },
    created() {
        // Initialize store
        ConnReqAPI.get_connection_requests()
            .then(res => useAppStore().set_connection_requests(res.data))
    },
    methods: {
        // Accepts an incoming connection request.
        accept_connection_request(email, name, index) {
            ConnReqAPI.accept_connection_request(email)
                .then(() => {
                    this.$q.notify({
                        message: `Added ${name}!`,
                        icon: 'check',
                        position: 'bottom-right',
                        color: 'blue-7'
                    })
                })
                .finally(() => {
                    useAppStore().delete_connection_request(index)
                })
        },

        // Deletes an incoming connection request.
        delete_connection_request(email, index) {
            ConnReqAPI.delete_connection_request(email)
                .finally(() => {
                    useAppStore().delete_connection_request(index)
                })
        },

        // Update user information.
        update_user(v) {
            useAppStore().set_user(v)
            useAppStore().set_viewing_user(v)
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
    .profile_name {
        color: $dark-primary !important;
    }

    .noti_button {
        color: $grey-5 !important;
    }
}

// .profile_avatar {
//     transition: transform 0.3s ease;
// }

// .profile_name {
//     transition: transform 0.3s ease;
// }

// .profile_section {
//     &:hover {
//         .profile_avatar {
//             transform: scale(1.055);
//         }

//         .profile_name {
//             transform: scale(1.03);
//         }
//     }
// }

.noti_count {
    transition: all 0.9s;
}

.noti_button {
    &:hover {
        .noti_count {
            opacity: 0.95 !important;
        }
    }
}
</style>
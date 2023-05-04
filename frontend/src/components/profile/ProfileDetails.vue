<template>
    <!-- Profile Details -->
    <q-dialog v-model="show">
        <q-card class="flex column q-px-lg q-py-lg" style="min-width: 550px; min-height: 200px" @keyup.enter="edit_save">

            <q-card-section class="q-py-xs">
                <div class="personal_details_label text-h6 text-indigo-5">Personal Details</div>
            </q-card-section>

            <q-card-section class="flex row q-py-sm">
                <!-- Profile Image -->
                <div class="q-pt-sm q-mr-lg">
                    <label for="profile-image-file" class="profile_picture_avatar flex column"
                        :class="[edit ? 'profile_picture_hoverable' : '']">
                        <q-avatar size="60px" color="grey-2">
                            <img v-if="new_image_data" :src="new_image_data" />
                            <img v-else-if="user.picture" :src="image_url" />
                            <q-icon v-else color="grey-8" size="60px" name="face" />
                        </q-avatar>
                        <span class="profile_picture_hint text-center q-mt-xs"
                            style="font-size:0.8em; opacity:0">change</span>
                    </label>
                    <input :disabled="!edit" id="profile-image-file" type="file" accept="image/png, image/jpeg"
                        @change="edit_image" style="display: none" ref="input_image">
                </div>

                <!-- Profile Information -->
                <div class="flex column q-pt-none col-grow">
                    <!-- Name -->
                    <div class="flex column q-mb-md">
                        <span class="user_info_title text-grey-8">
                            Name
                        </span>
                        <q-input autofocus :readonly="!edit" outlined dense class="user_info text-grey-8" hide-bottom-space
                            v-model="user.name" :rules="name_rules" ref="name_input" type="text" maxlength="50" />
                    </div>

                    <!-- Email -->
                    <div class="flex column q-mb-md">
                        <span class="user_info_title text-grey-8">
                            Email Address
                        </span>
                        <q-input readonly outlined dense class="user_info text-grey-8" v-model="user.email" type="text"
                            maxlength="50">
                        </q-input>
                    </div>

                    <!-- Mobile Number -->
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut"
                        mode="out-in">
                        <div v-if="edit || user.mobile" class="q-mb-md">
                            <span class="user_info_title text-grey-8">
                                Contact Number
                            </span>
                            <q-input :readonly="!edit" outlined dense class="user_info text-grey-8" v-model="user.mobile"
                                type="tel" maxlength="15">
                            </q-input>
                        </div>
                    </transition>

                    <!-- Linkedin -->
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut"
                        mode="out-in">
                        <div v-if="edit || user.linkedin" class="q-mb-md">
                            <span class="user_info_title text-grey-8">
                                Linkedin
                            </span>
                            <q-input :readonly="!edit" outlined dense class="user_info text-grey-8 q-mb-md"
                                v-model="user.linkedin" type="text" maxlength="50">
                            </q-input>
                        </div>
                    </transition>
                </div>
            </q-card-section>

            <!-- Editable buttons -->
            <q-card-section v-if="!readonly" align="right" class="text-primary">
                <template v-if="!edit">
                    <q-btn outline label="Edit" class="text-indigo-5" @click="edit_start" />
                </template>
                <template v-else>
                    <q-btn outline flat label="Cancel" class="text-grey-7 q-mr-lg" @click="edit_cancel" />
                    <q-btn :loading="saving" outline label="Save Changes" class="text-green-7" @click="edit_save" />
                </template>
            </q-card-section>

            <!-- Extra Actions Slot -->
            <slot></slot>
        </q-card>
    </q-dialog>
</template>

<script>
import UserAPI from 'src/services/user.api.js'
import { get_base_url } from 'src/services/utils.js'

export default {
    props: {
        readonly: Boolean,
        user_prop: Object,
    },
    emits: ['update_user'],
    data() {
        return {
            show: false,
            edit: false, // Editing state
            user: {},
            picture: null,
            saving: false,
            new_image_data: null,
            new_image_file: null,

            // Input Rules
            name_rules: [
                v => (v && v.length > 0) || 'Name cannot be empty.',
            ],
        }
    },
    watch: {
        show(new_value, old_value) {
            if (!new_value) {
                this.edit = false
            }
        }
    },
    computed: {
        image_url() {
            return `${get_base_url()}/${this.user.picture}`
        },
    },
    methods: {
        show_profile() {
            this.show = true
            this.reset_edit()
        },
        reset_edit() {
            this.user = Object.assign({}, this.user_prop)
            this.new_image_data = null
            this.new_image_file = null

            // Reset the input image file.
            const input_image = this.$refs.input_image
            if (input_image) {
                input_image.value = ""
            }
        },
        edit_image(e) {
            const image = e.target.files[0]
            this.new_image_file = image
            const rdr = new FileReader()
            rdr.readAsDataURL(image)
            rdr.onload = e => { this.new_image_data = e.target.result }
        },
        edit_start() {
            this.edit = true
        },
        edit_cancel() {
            this.edit = false
            this.reset_edit()
        },
        edit_save() {
            // Ensure in edit state before saving.
            if (!this.edit) return

            // If error, return.
            if (!this.$refs.name_input.validate(this.user.name)) {
                // Notify error.
                this.$q.notify({
                    message: 'Name is invalid.',
                    position: 'bottom-right',
                    color: 'red-5'
                })
                return
            }

            this.edit = false

            // Only notify once is enough, either on profile picture update or user information update.
            let notified_update = false

            // Post update picture.
            if (this.new_image_file) {
                notified_update = true
                UserAPI.update_user_image(this.new_image_file)
                    .then(res => {
                        // Notify update success.
                        this.$q.notify({
                            message: 'Saved profile',
                            icon: 'check_circle',
                            position: 'bottom-right',
                            color: 'green-6'
                        })

                        this.user.picture = res.data.filename

                        // Emit update success.
                        this.$emit('update_user', Object.assign({}, this.user))
                    })
            }

            // Post user API call to update.
            const updated_user_api_param = Object.assign({}, this.user)
            // User information unchanged, update not required.
            if (JSON.stringify(updated_user_api_param) == JSON.stringify(this.user_prop)) {
                return
            }
            delete updated_user_api_param.id
            UserAPI.update_user(updated_user_api_param)
                .then(_ => {
                    if (!notified_update) {
                        // Notify update success.
                        this.$q.notify({
                            message: 'Saved profile',
                            icon: 'check_circle',
                            position: 'bottom-right',
                            color: 'green-6'
                        })
                    }

                    // Emit update success.
                    this.$emit('update_user', Object.assign({}, this.user))
                })
                .catch(e => { // Update failed.
                    // Notify update failure.
                    this.$q.notify({
                        message: 'Failed to save profile',
                        icon: 'highlight_off',
                        position: 'bottom-right',
                        color: 'red-5'
                    })
                    console.log(e)

                    this.reset_user()
                })
        },
    }
}
</script>

<style lang="scss" scoped>
// Dark Mode
.body--dark {
    .personal_details_label {
        color: $blue-6 !important;
    }

    .user_info_title {
        color: $blue-3 !important;
    }

    .user_info {
        color: $grey-6 !important;
    }
}

// Profile Picture
.profile_picture_hoverable {
    &:hover {
        filter: brightness(75%);

        .profile_picture_hint {
            opacity: 1 !important;
        }
    }

    .profile_picture_avatar {
        cursor: pointer;
    }

    cursor: pointer;
    transition: all 0.4s ease;
}

.profile_picture_hint {
    transition: all 0.4s ease;
}
</style>
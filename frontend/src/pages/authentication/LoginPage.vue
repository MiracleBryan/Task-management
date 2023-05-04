<template>
    <div class="login_page flex items-center fullscreen">
        <q-card rounded class='text-grey-8 q-mx-auto shadow-7' style="margin-bottom: 8em; width: 370px; height: 535px;">
            <div class="flex column items-center full-height q-pt-xl q-pb-lg q-px-md" @keyup.enter="login">
                <div class='text-h6 text-bold text-grey-10 no-pointer-events'>Welcome</div>

                <q-avatar class="q-mt-lg q-mb-md" style="opacity: 0.775">
                    <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-black.svg">
                </q-avatar>

                <div class="flex column col-grow" style="width: 85%">
                    <q-input dense autofocus v-model='email' label='Email' type='email' style="margin-top: 1.95em;" />
                    <q-input dense v-model='password' label='Password' type='password' style="margin-top: 1.95em;" />

                    <div style="flex: 1 1 auto">
                        <q-btn flat rounded :disabled='logging_in' :loading='logging_in'
                            class='full-width text-white bg-indigo-8 q-py-sm' label='LOGIN' @click='login' color='primary'
                            style="z-index: 1; margin-top: 5.6em">
                            <template v-slot:loading>
                                <q-spinner-hourglass class="on-left" />
                            </template>
                        </q-btn>
                        <Transition appear enter-active-class="animated slideInDown" leave-active-class="animated fadeOut">
                            <p v-if="message" class="text-red-8" style="pointer-events: none">{{ message }}</p>
                        </Transition>
                    </div>

                    <div class="flex row justify-center">
                        <span style="pointer-events: none">Don't have an account?</span>
                        <span>&nbsp;&nbsp;</span>
                        <span style="cursor: pointer; text-decoration: underline;" @click="register">Sign Up</span>
                    </div>
                </div>
            </div>
        </q-card>
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import AuthAPI from 'src/services/user.api.js';
import { useAppStore } from 'src/stores/AppStore'
import { initialize_socket } from 'src/services/socket/socket'
import { get_access_token_attr_key } from 'src/utils/local_storage_utils'

export default defineComponent({
    data() {
        return {
            email: '',
            password: '',
            logging_in: false,
            message: '',
        }
    },
    methods: {
        login() {
            this.logging_in = true
            this.message = ''
            AuthAPI.login(this.email, this.password)
                .then(r => {
                    localStorage.setItem(get_access_token_attr_key(), r.data.access_token)
                    AuthAPI.refresh_auth_headers()

                    // Initialize socket
                    initialize_socket()

                    // Initialize user
                    AuthAPI.get_user()
                        .then(res => {
                            const store = useAppStore()
                            store.set_user(res.data)

                            // Redirect to the tasks list page.
                            this.$router.push({ path: '/tasks' })
                        })
                })
                .catch(() => {
                    console.log('Login failed!')
                    this.logging_in = false
                    this.message = 'Invalid username or password.'
                })
        },
        register() {
            this.$router.push({ name: 'register' })
        }
    }
})
</script>

<style scoped lang="scss">
.login_page {
    background-image: linear-gradient(30deg, $indigo-8, $purple-7, $indigo-13);
    background-size: 400%;
    animation: bg-anim 85s infinite alternate;
}

@keyframes bg-anim {
    0% {
        background-position: left;
    }

    100% {
        background-position: right;
    }
}
</style>
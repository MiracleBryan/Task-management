<template>
    <div class="register_page flex items-center fullscreen">
        <q-card rounded class='text-grey-8 q-mx-auto shadow-7' style="margin-bottom: 8em; width: 370px; height: 535px;">
            <div class="flex column items-center full-height q-pt-xl q-pb-lg q-px-md">
                <div class='text-h6 text-bold text-grey-10 no-pointer-events'>Register</div>

                <q-avatar class="q-mt-lg q-mb-md" style="opacity: 0.775">
                    <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-black.svg">
                </q-avatar>
                <!-- Register Input  -->
                <div class="flex column col-grow" style="width: 85%">
                    <q-input dense autofocus ref="input" lazy-rules :rules="[
                        val => (!!val) || `Name is required`,
                    ]" v-model='name' label='Name' type='text' style="margin-top: 0.3em;" />
                    <q-input dense ref="input" lazy-rules :rules="[
                        (val, rules) => rules.email(val) && (!!val) || 'Please enter a valid email address'
                    ]" v-model='email' label='Email' type='email' style="margin-top: 0.5em;" />
                    <q-input dense ref="input" lazy-rules :rules="[
                        val => (!!val) || `Password is required`,
                    ]" v-model='password' label='Password' type='password' style="margin-top: 0.5em;" />
                    <!-- Form Submit -->
                    <div style="flex: 1 1 auto">
                        <q-btn flat rounded :disabled='logging_in' :loading='logging_in'
                            class='full-width text-white bg-indigo-8 q-py-sm' label='Done' @click='register' color='primary'
                            style="z-index: 1; margin-top: 3em">
                            <template v-slot:loading>
                                <q-spinner-hourglass class="on-left" />
                            </template>
                        </q-btn>
                        <Transition appear enter-active-class="animated slideInDown" leave-active-class="animated fadeOut">
                            <p v-if="message" class="text-red-8" style="pointer-events: none">{{ message }}</p>
                        </Transition>
                    </div>
                    <!-- Return -->
                    <div class="flex row justify-center">
                        <span style="cursor: pointer; text-decoration: underline;" @click="BacktoLogin">Back to login</span>
                    </div>
                </div>
            </div>
        </q-card>
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import AuthAPI from 'src/services/user.api.js';
import { useQuasar } from 'quasar';


export default defineComponent({
    data() {
        return {
            name: '',
            email: '',
            password: '',
            mobile: '',
            linkedin: '',
            registering: false,
            logging_in: false,
            message: '',
        }
    },
    // Popup message
    setup() {
        const $q = useQuasar()
        return {
            showNotif(msg, clr) {
                $q.notify({
                    message: msg,
                    color: clr
                })
            }
        }
    },

    methods: {

        register() {
            this.logging_in = true
            this.message = ''
            // Check submit items
            if (this.name == '' || !this.email.includes('@' && '.com') || this.password == '' || this.email == '') {
                console.log('Invaild: Empty colum')
                this.logging_in = false
                this.message = 'Must filled in required Info'
                this.showNotif('Must filled in required Info', 'red')
            }
            else {
                AuthAPI.register(this.name, this.email, this.password, this.mobile, this.linkedin)
                    .then(() => {
                        this.showNotif('Register success!', 'green')
                        console.log('Register success! Redirecting..')
                        this.$router.push({ name: 'login' })
                    })
                    .catch((err) => {
                        this.showNotif(err.response.data, 'red')
                        console.log('Register failed!')
                        this.logging_in = false
                        this.message = err.response.data
                        console.log(err.response.data)
                    })
            }

        },

        BacktoLogin() {
            this.$router.push({ name: 'login' })
        }
    }

})

</script>

<style scoped lang="scss">
.register_page {
    background-image: linear-gradient(30deg, $indigo-8, $purple-7, $indigo-13);
    background-size: 400%;
    animation: bg-anim 85s infinite alternate;
}


.login_container {
    width: 380px;
    height: 430px;

}

.input {
    margin-top: 2em;
}

.register_button {
    margin-top: 4em;
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
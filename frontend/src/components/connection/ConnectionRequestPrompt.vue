
<template>
    <q-dialog v-model="show">
        <q-card class="q-px-md q-py-md" style="min-width: 400px">
            <q-card-section>
                <div class="send_connection_label text-h6 text-grey-9">Send Connection Request</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
                <q-input dense v-model="email" autofocus label="Email" type="email" @keyup.enter="send_request" />
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn outline label="Add" class="text-indigo-8" v-close-popup @click="send_request" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import ConnReqAPI from 'src/services/connection_request.api.js'

export default {
    data() {
        return {
            show: false,
            email: ''
        }
    },
    methods: {
        show_add_dialog() {
            this.show = true
        },
        send_request() {
            this.show = false

            if (this.email == '') return

            ConnReqAPI.send_connection_request(this.email)
                .then(() => {
                    this.$q.notify({
                        message: `Sent request to ${this.email}`,
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
}
</script>

<style lang="scss">
// Dark Mode
.body--dark {
    .send_connection_label {
        color: $grey-4 !important;
    }
}
</style>
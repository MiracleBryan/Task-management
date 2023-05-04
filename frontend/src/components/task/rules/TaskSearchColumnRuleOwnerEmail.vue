<template>
    <q-select dense options-dense outlined :options="conditions" v-model="condition" style="width: 160px" class="q-mr-sm">
        <template v-if="!condition" v-slot:prepend>
            <div style="font-size:0.6em">Condition</div>
        </template>
    </q-select>
    <q-select dense options-dense outlined :options="owner_emails" v-model="email" style="min-width: 280px" class="q-mr-sm">
        <template v-if="!email" v-slot:prepend>
            <div style="font-size:0.6em">Select an email</div>
        </template>
    </q-select>
</template>
<script>
import { useAppStore } from 'src/stores/AppStore'

export default {
    data() {
        return {
            condition: "",
            email: "",
        }
    },
    emits: ["changed"],
    created() {
        this.condition = this.conditions[0]
    },
    watch: {
        condition() {
            this.$emit("changed")
        },
        email() {
            this.$emit("changed")
        }
    },
    computed: {
        conditions() {
            return ["is", "is not"]
        },
        owner_emails() {
            const emails = useAppStore().connection.map(conn => conn.email)
            emails.push(useAppStore().user.email)
            return emails
        },
    },
    methods: {
        match(task) {
            if (this.condition == "is") {
                return task.owner_email == this.email
            } else if (this.condition == "is not") {
                return task.owner_email != this.email
            }
            return false
        }
    }
}
</script>
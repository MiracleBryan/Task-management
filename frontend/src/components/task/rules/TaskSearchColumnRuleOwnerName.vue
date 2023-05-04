<template>
    <q-select dense options-dense outlined :options="conditions" v-model="condition" style="width: 160px" class="q-mr-sm">
        <template v-if="!condition" v-slot:prepend>
            <div style="font-size:0.6em">Condition</div>
        </template>
    </q-select>
    <q-select dense options-dense outlined :options="owner_names" v-model="name" style="min-width: 280px" class="q-mr-sm">
        <template v-if="!name" v-slot:prepend>
            <div style="font-size:0.6em">Select a name</div>
        </template>
    </q-select>
</template>
<script>
import { useAppStore } from 'src/stores/AppStore'

export default {
    data() {
        return {
            condition: "",
            name: "",
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
        name() {
            this.$emit("changed")
        }
    },
    computed: {
        conditions() {
            return ["is", "is not"]
        },
        owner_names() {
            const names = useAppStore().connection.map(conn => conn.name)
            names.push(useAppStore().user.name)
            return names
        },
    },
    methods: {
        match(task) {
            if (this.condition == "is") {
                return task.owner_name == this.name
            } else if (this.condition == "is not") {
                return task.owner_name != this.name
            }
            return false
        }
    }
}
</script>
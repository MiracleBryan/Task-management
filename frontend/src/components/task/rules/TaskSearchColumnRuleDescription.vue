<template>
    <q-select dense options-dense outlined :options="conditions" v-model="condition" style="width: 160px" class="q-mr-sm">
        <template v-if="!condition" v-slot:prepend>
            <div style="font-size:0.6em">Condition</div>
        </template>
    </q-select>
    <q-input dense outlined v-model="description" style="min-width: 280px" class="q-mr-sm">
    </q-input>
</template>
<script>

export default {
    data() {
        return {
            condition: "",
            description: "",
        }
    },
    emits: ["changed"],
    created() {
        this.condition = this.conditions[2]
    },
    watch: {
        condition() {
            this.$emit("changed")
        },
        description() {
            this.$emit("changed")
        }
    },
    computed: {
        conditions() {
            return ["is", "is not", "contains", "doesn't contain"]
        }
    },
    methods: {
        match(task) {
            if (this.condition == "is") {
                if (task.description == null) {
                    return this.description == ""
                }
                return task.description == this.description
            } else if (this.condition == "is not") {
                if (task.description == null) {
                    return this.description != ""
                }
                return task.description != this.description
            } else if (this.condition == "contains") {
                if (task.description == null) {
                    return false
                }
                if (task.description.match(new RegExp(this.description, "i"))) {
                    return true
                }
            } else if (this.condition == "doesn't contain") {
                if (task.description == null) {
                    return true
                }
                if (task.description.match(new RegExp(this.description, "i"))) {
                    return true
                }
            }
            return false
        }
    }
}
</script>
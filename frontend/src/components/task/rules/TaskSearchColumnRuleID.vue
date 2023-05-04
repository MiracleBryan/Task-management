<template>
    <q-select dense options-dense outlined :options="conditions" v-model="condition" style="width: 160px" class="q-mr-sm">
        <template v-if="!condition" v-slot:prepend>
            <div style="font-size:0.6em">Condition</div>
        </template>
    </q-select>
    <q-input dense outlined v-model="id" style="min-width: 280px" class="q-mr-sm">
    </q-input>
</template>
<script>

export default {
    data() {
        return {
            condition: "",
            id: "",
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
        id() {
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
            let task_id_str = task.id.toString()
            if (this.condition == "is") {
                return task_id_str == this.id
            } else if (this.condition == "is not") {
                return task_id_str != this.id
            } else if (this.condition == "contains") {
                if (task_id_str.match(new RegExp(this.id, "i"))) {
                    return true
                }
            } else if (this.condition == "doesn't contain") {
                if (task_id_str.match(new RegExp(this.id, "i"))) {
                    return true
                }
            }
            return false
        }
    }
}
</script>
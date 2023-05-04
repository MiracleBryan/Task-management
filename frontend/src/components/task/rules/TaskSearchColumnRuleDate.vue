<template>
    <q-select dense options-dense outlined :options="conditions" v-model="condition" style="width: 160px" class="q-mr-sm">
        <template v-if="!condition" v-slot:prepend>
            <div style="font-size:0.6em">Condition</div>
        </template>
    </q-select>

    <!-- Calendar - Date 1 -->
    <div style="border: 1px solid grey; border-radius: 3px"
        class="date_picker q-mr-sm row items-center justify-center cursor-pointer"
        :style="{ 'min-width': (condition == 'between') ? '127px' : '280px' }">
        <div class="text-grey-7">{{ date1 }}</div>

        <!-- Calendar -->
        <q-menu anchor="bottom middle" self="top middle" :offset="[0, 1]" v-model="show_calendar_1"
            style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
            <q-date minimal v-model="date1"
                style="box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)"
                mask="DD MMM YYYY" />
        </q-menu>
    </div>

    <!-- Between two dates, Creates another date field -->
    <template v-if="condition == 'between'">
        <div class="text-grey-9 q-mr-sm row items-center">
            to
        </div>

        <!-- Calendar - Date 2 -->
        <div style="min-width: 127px; border: 1px solid grey; border-radius: 3px"
            class="date_picker q-mr-sm row items-center justify-center cursor-pointer">
            <div class="text-grey-7">{{ date2 }}</div>

            <!-- Calendar -->
            <q-menu anchor="bottom middle" self="top middle" :offset="[0, 1]" v-model="show_calendar_2"
                style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
                <q-date minimal v-model="date2"
                    style="box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)"
                    mask="DD MMM YYYY" />
            </q-menu>
        </div>
    </template>
</template>
<script>
export default {
    data() {
        return {
            condition: "",
            date1: "",
            date2: "",

            // UI Calendar
            show_calendar_1: false,
            show_calendar_2: false
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
        date1() {
            this.$emit("changed")
            this.show_calendar_1 = false
            this.show_calendar_2 = false
        },
        date2() {
            this.$emit("changed")
            this.show_calendar_1 = false
            this.show_calendar_2 = false
        }
    },
    computed: {
        conditions() {
            return ["is", "is not", "before", "after", "between"]
        }
    },
    methods: {
        match(task) {
            if (this.date1 == "") return true
            if (this.condition == "is") {
                return task.deadline == this.date1
            } else if (this.condition == "is not") {
                return task.deadline != this.date1
            } else if (this.condition == "before") {
                return Date.parse(task.deadline) < Date.parse(this.date1)
            } else if (this.condition == "after") {
                return Date.parse(task.deadline) > Date.parse(this.date1)
            } else if (this.condition == "between") {
                return Date.parse(this.date1) <= Date.parse(task.deadline) && Date.parse(task.deadline) <= Date.parse(this.date2)
            }
            return false
        }
    }
}
</script>

<style scoped lang="scss">
.date_picker {
    &:hover {
        border-color: black !important;
    }

    transition: all 0.4s;
}
</style>
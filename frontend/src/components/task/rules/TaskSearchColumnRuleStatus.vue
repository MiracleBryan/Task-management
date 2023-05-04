<template>
    <q-select dense options-dense outlined :options="conditions" v-model="condition" style="width: 160px" class="q-mr-sm">
        <template v-if="!condition" v-slot:prepend>
            <div style="font-size:0.6em">Condition</div>
        </template>
    </q-select>
    <q-select dense options-dense outlined multiple use-chips :options="Object.keys(status_display)" v-model="status"
        style="min-width: 280px" class="q-mr-sm">
        <template v-if="!status.length" v-slot:prepend>
            <div style="font-size:0.6em">Select a status</div>
        </template>
        <template v-slot:option="scope">
            <div v-if="!scope.selected" v-bind="scope.itemProps"
                class="status_option q-px-md q-py-sm cursor-pointer text-white text-center"
                :style="{ 'background-color': getPaletteColor(status_color[scope.opt]) }">
                {{ status_display[scope.opt] }}
            </div>
        </template>
        <template v-slot:selected-item="scope">
            <q-chip removable dense :color="status_color[scope.opt]" text-color="white"
                @remove="scope.removeAtIndex(scope.index)" :tabindex="scope.tabindex">
                {{ status_display[scope.opt] }}
            </q-chip>
        </template>
        <template v-slot:no-option>
            <div class="q-py-sm q-px-sm no-pointer-events text-grey-6">Select a column</div>
        </template>
    </q-select>
</template>
<script>
import { Status_Display, Status_Color } from 'src/utils/data/status.js'
import { colors } from 'quasar'

export default {
    data() {
        return {
            condition: "",
            status: [],

            // Helpers
            status_display: Status_Display,
            status_color: Status_Color,
        }
    },
    emits: ["changed"],
    created() {
        this.condition = this.conditions[0]
        this.getPaletteColor = colors.getPaletteColor
    },
    watch: {
        condition() {
            this.$emit("changed")
        },
        status() {
            this.$emit("changed")
        }
    },
    computed: {
        conditions() {
            return ["is", "is not"]
        }
    },
    methods: {
        match(task) {
            if (this.status.length == 0) {
                return true
            }
            if (this.condition == "is") {
                return this.status.includes(task.status)
            } else if (this.condition == "is not") {
                return !this.status.includes(task.status)
            }
            return false
        }
    }
}
</script>

<style scoped lang="scss">
.status_option {
    &:hover {
        transform: scale(0.96, 0.94);
    }

    transition: all 0.3s;
}
</style>
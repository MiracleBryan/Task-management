<template>
    <div class="row q-mb-sm">
        <!-- Where Label / Aggregator -->
        <div v-if="is_first" class="text-grey-7 q-mr-sm self-center no-pointer-events" style="width: 70px">
            Where
        </div>
        <q-select v-else dense options-dense outlined :options="aggregation_options" v-model="aggregated.condition"
            style="width: 70px" class="q-mr-sm" />

        <!-- Column Type -->
        <q-select dense options-dense outlined :options="Object.keys(column_rules)" v-model="column" style="width: 150px"
            class="q-mr-sm">
            <template v-if="!column" v-slot:prepend>
                <div style="font-size:0.6em">Column</div>
            </template>
        </q-select>

        <!-- Column Unselected -->
        <template v-if="!column">
            <q-input dense outlined style="width: 160px" placeholder="Condition" readonly class="no-pointer-events q-mr-sm">
            </q-input>
            <q-input dense outlined style="min-width: 280px" placeholder="Value" readonly class="no-pointer-events q-mr-sm">
            </q-input>
        </template>

        <!-- Column Rule -->
        <component v-if="column" :is="rule_component" @changed="update_rule" ref="rule_ref"></component>

        <!-- Delete Rule Button -->
        <q-btn v-if="!is_first" round flat color="grey-7" icon="close" @click="delete_rule"></q-btn>
        <div v-else style="min-width:42px"></div>
    </div>
</template>

<script>
import { markRaw } from 'vue'
import RuleID from './TaskSearchColumnRuleID.vue'
import RuleTitle from './TaskSearchColumnRuleTitle.vue'
import RuleStatus from './TaskSearchColumnRuleStatus.vue'
import RuleOwnerName from './TaskSearchColumnRuleOwnerName.vue'
import RuleOwnerEmail from './TaskSearchColumnRuleOwnerEmail.vue'
import RuleDescription from './TaskSearchColumnRuleDescription.vue'
import RuleDate from './TaskSearchColumnRuleDate.vue'

export default {
    props: {
        is_first: {
            type: Boolean,
            default: false,
        },
        aggregated_prop: Object,
    },
    emits: ["update_rule", "delete_rule"],
    data() {
        return {
            // Aggregated condition
            aggregated: "",
            aggregation_options: ["And", "Or"],

            // Column Type
            column: "",

            // Column Rules
            column_rules: {
                "ID": markRaw(RuleID),
                "Title": markRaw(RuleTitle),
                "Status": markRaw(RuleStatus),
                "Due Date": markRaw(RuleDate),
                "Description": markRaw(RuleDescription),
                "Owner Name": markRaw(RuleOwnerName),
                "Owner Email": markRaw(RuleOwnerEmail),
            },
        }
    },
    created() {
        this.aggregated = this.aggregated_prop
    },
    computed: {
        rule_component() {
            return this.column_rules[this.column]
        },
    },
    methods: {
        delete_rule() {
            this.$emit("delete_rule")
        },
        update_rule() {
            this.$emit("update_rule")
        },
        match(task) {
            if (this.$refs.rule_ref) {
                return this.$refs.rule_ref.match(task)
            }
            return true
        }
    }
}
</script>

<style scoped lang="scss">
::v-deep {
    .q-field__control {
        border-radius: 4px !important;
    }
}
</style>
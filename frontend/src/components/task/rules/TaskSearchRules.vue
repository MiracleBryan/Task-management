<template>
    <div>
        <div class="text-bold text-grey-8 q-mb-md no-pointer-events">
            Advanced Search
        </div>

        <!-- Ruleset -->
        <template v-for="(rule, index) in rules" :key="rule">
            <TaskSearchRule ref="ruleset" :data-rule_id="rule" :is_first="index == 0" :aggregated_prop="aggregated"
                @delete_rule="delete_rule(index)" @update_rule="search" @aggregated_change="search" />
        </template>

        <!-- Search Controls -->
        <div class="row justify-between text-grey-9 q-mt-lg" style="margin-right: 58px">
            <!-- Add Rule -->
            <q-btn flat no-caps @click="add_rule">+ Add new condition</q-btn>

            <!-- Search Controls -->
            <div>
                <!-- Invalidate Search -->
                <q-btn v-show="allow_refresh" dense class="q-mr-sm" color="grey-8" round flat icon="refresh"
                    @click="invalidate_search">
                    <q-tooltip anchor="top middle" self="center middle">
                        Refresh Search
                    </q-tooltip>
                </q-btn>

                <!-- Search -->
                <q-toggle style="font-size:1.1em; font-weight:500" v-model="active_searching" label="Search" left-label
                    icon="search" color="indigo-5" size="md" />
            </div>
        </div>
    </div>
</template>

<script>
import TaskSearchRule from './TaskSearchRule.vue';

export default {
    components: {
        TaskSearchRule
    },
    emits: ["update_search"],
    props: {
        tasks_prop: Array
    },
    data() {
        return {
            // Aggregation
            aggregated: { condition: "And" },

            // Ruleset
            rule_id: 1,
            rules: [0],

            // Searching
            active_searching: false,

            // Refresh Search
            allow_refresh: false,
            last_searched: false,
        }
    },
    watch: {
        aggregated: {
            handler() {
                this.search()
            },
            deep: true,
        },
        active_searching(new_value, old_value) {
            this.search()
        },
        tasks_prop: {
            handler(new_value, old_value) {
                if (this.last_searched) {
                    this.last_searched = false
                    return
                }
                if (this.active_searching) this.allow_refresh = true
            },
            deep: true
        },
    },
    methods: {
        add_rule() {
            this.rules.push(this.rule_id++)
        },
        delete_rule(index) {
            this.rules.splice(index, 1)
            this.search()
        },
        invalidate_search() {
            this.search()
            this.allow_refresh = false
        },
        search() {
            let visibility = []
            const rules = []
            for (const rule of this.$refs.ruleset) {
                const rule_id = parseInt(rule.$el.dataset.rule_id)
                if (this.rules.includes(rule_id)) rules.push(rule)
            }
            if (this.active_searching) {
                for (const i in this.tasks_prop) {
                    const t = this.tasks_prop[i].data
                    let ok
                    if (this.aggregated.condition == "And") {
                        ok = true
                        for (const rule of rules) {
                            if (!rule.match(t)) {
                                ok = false
                                break
                            }
                        }
                    } else if (this.aggregated.condition == "Or") {
                        ok = false
                        for (const rule of rules) {
                            if (rule.match(t)) {
                                ok = true
                                break
                            }
                        }
                    }
                    visibility.push(ok)
                }
            } else {
                for (const i in this.tasks_prop) {
                    visibility.push(true)
                }
            }
            this.$emit("update_search", visibility)
            this.last_searched = true
        }
    }
}
</script>
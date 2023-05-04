<template>
    <div class="task-main" :class="{ highlight: task.selected }" style="box-sizing: border-box">
        <!-- Selection Checkbox -->
        <div class="task-col" :style="{ 'border-bottom-left-radius': is_last ? '8px' : '0px' }">
            <q-checkbox class="checkbox_selection" v-model="task.selected" />
        </div>

        <!-- ID -->
        <div class="task-col task_column_hide_mobile task-col--noleft" style="min-width: 45px">
            <div>{{ task.data.id }}</div>
        </div>

        <!-- Title -->
        <div class="task-col task_column_title task-col--noleft" :style="{ width: ui_info.sizes[0] + 'px' }">
            <q-input class="title_input" dense outlined v-model="task.data.title" style="width:90%" />
            <div class="resize-column-feedback" :style="{ opacity: ui_info.resizing[0] ? 1 : 0 }"></div>
        </div>

        <!-- Owner Assign To -->
        <div class="task-col task_column_hide_mobile task-col--noleft col-borderhover"
            :style="{ width: ui_info.sizes[1] + 'px' }">
            <q-btn class="assign_owner_btn" outline color="grey-8" no-caps
                :label="task.data.owner_email == user_email ? username : task.data.owner_name" style="width:90%">
                <q-menu auto-close anchor="bottom middle" self="top middle" :offset="[0, 1]"
                    style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
                    <div class="flex column">
                        <div class="pop_triangle self-center" style="z-index: 1"></div>
                        <q-card class="assign_to_card flex column"
                            style="width: 225px; border-radius: 8px; padding-bottom: 1.45em; box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)">
                            <!-- Assign to -->
                            <div class="text-grey-7 q-mx-lg q-mt-md">Assign to</div>

                            <!-- If Owner is not my Email, allow an assignment of this task back to myself -->
                            <q-btn v-if="task.data.owner_email != user_email" no-caps flat class="text-grey-8 self-center"
                                style="width:200px; margin-top: 0.5em"
                                @click="assign_task({ name: username, email: user_email })">Myself</q-btn>

                            <!-- For every connection -->
                            <template v-for="conn in connections" :key="conn.email">
                                <q-btn v-if="task.data.owner_email != conn.email" no-caps flat
                                    class="text-grey-8 self-center" style="width:200px; margin-top: 0.5em"
                                    @click="assign_task(conn)">
                                    {{ conn.name }}
                                </q-btn>
                            </template>
                        </q-card>
                    </div>
                </q-menu>
            </q-btn>
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[1] ? 1 : 0 }"></div>
        </div>

        <!-- Status -->
        <div class="task-col task_column_hide_mobile task-col--noleft" :style="{ width: ui_info.sizes[2] + 'px' }">
            <q-btn filled unelevated :color="status_color[task.data.status]" no-caps
                :label="status_display[task.data.status]" style="width:90%">
                <q-menu auto-close anchor="bottom middle" self="top middle" :offset="[0, 1]"
                    style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
                    <div class="flex column">
                        <div class="pop_triangle self-center" style="z-index: 1"></div>
                        <q-card class="status_card flex column"
                            style="width: 225px; border-radius: 8px; padding: 1.5em 0 1em 0; box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)">
                            <q-btn v-for="[status, display] in Object.entries(status_display)" :key="status" no-caps
                                :push="status == task.data.status" :flat="status != task.data.status"
                                :class="[`bg-${status_color[status]}`, status == task.data.status ? 'glossy' : '']"
                                class="text-white self-center" style="width: 200px; margin-bottom: 0.5em;"
                                @click="task.data.status = status">
                                {{ display }}
                            </q-btn>
                        </q-card>
                    </div>
                </q-menu>
            </q-btn>
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[2] ? 1 : 0 }"></div>
        </div>

        <!-- Dateline -->
        <div class="task-col task_column_hide_mobile task-col--noleft col-borderhover"
            :style="{ width: ui_info.sizes[3] + 'px' }">
            <q-btn class="deadline_btn" outline color="grey-8" icon="event" style="width:90%" no-caps>
                <span class="q-pl-sm">{{ deadline_computed }}</span>
                <q-menu anchor="bottom middle" self="top middle" :offset="[0, 1]" v-model="show_calendar"
                    style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
                    <q-card class="calendar_card flex column">
                        <div class="pop_triangle self-center" style="z-index: 1"></div>
                        <q-date minimal v-model="task.data.deadline"
                            style="box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)"
                            mask="DD MMM YYYY" :options="no_dateline_before_today" />
                    </q-card>
                </q-menu>
                <q-tooltip v-if="days_remaining != null" :delay="350" anchor="top middle" self="center middle">
                    {{ `${days_remaining} days remaining` }}
                </q-tooltip>
                <q-tooltip v-else :delay="350" anchor="top middle" self="center middle">
                    no due date
                </q-tooltip>
            </q-btn>
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[3] ? 1 : 0 }"></div>
        </div>

        <!-- Description -->
        <div class="task-col task_column_hide_mobile task-col--noleft col-borderhover"
            :style="{ 'width': ui_info.sizes[4] + 'px' }">
            <q-input readonly dense outlined v-model="task.data.description" style="width:90%">
                <q-menu class="description_input" cover anchor="top middle">
                    <q-input autofocus outlined v-model="task.data.description" type="textarea" />
                </q-menu>
            </q-input>
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[4] ? 1 : 0 }"></div>
        </div>

        <!-- Estimated_Time -->
        <div class="task-col task_column_hide_mobile task-col--noleft"
            :style="[{ width: ui_info.sizes[5] + 'px' }, { 'border-bottom-right-radius': is_last ? '8px' : '0px' }]">
            <q-input class="title_input" dense outlined v-model="task.data.estimated_time" style="width:90%" type="number"
                @keypress="input_estimated_time($event)" />
            <div class="resize-column-feedback" :style="{ opacity: ui_info.resizing[5] ? 1 : 0 }"></div>
        </div>

        <!-- Dialog for Completion Date of the Task -->
        <div>
            <q-dialog v-model="show_completion_date">
                <q-date v-model="task.data.date_completed" mask="DD MMM YYYY" />
            </q-dialog>
        </div>

        <!-- Responsive Mobile: Edit Tool -->
        <div v-if="task.focused" class="mobile_edit" style="position: absolute; top: 5%; right: 5%; display: none">
            <q-btn icon="edit" round color="indigo-5" @click="mobile_edit" />

            <!-- Mobile Edit Dialog -->
            <q-dialog v-model="show_mobile_edit">
                <div class="bg-grey-1 q-px-xl q-py-xl">
                    <div class="text-h6 q-mb-md text-center">Update Task</div>

                    <!-- Title -->
                    <div>Title</div>
                    <q-input class="q-mb-md" dense outlined v-model="task.data.title" />

                    <!-- Status -->
                    <div>Status</div>
                    <q-btn class="q-mb-md" filled unelevated :color="status_color[task.data.status]" no-caps
                        :label="status_display[task.data.status]" style="width:100%">
                        <q-menu auto-close anchor="bottom middle" self="top middle" :offset="[0, 1]"
                            style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
                            <div class="flex column">
                                <div class="pop_triangle self-center" style="z-index: 1"></div>
                                <q-card class="status_card flex column"
                                    style="width: 225px; border-radius: 8px; padding: 1.5em 0 1em 0; box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)">
                                    <q-btn v-for="[status, display] in Object.entries(status_display)" :key="status" no-caps
                                        :push="status == task.data.status" :flat="status != task.data.status"
                                        :class="[`bg-${status_color[status]}`, status == task.data.status ? 'glossy' : '']"
                                        class="text-white self-center" style="width: 200px; margin-bottom: 0.5em;"
                                        @click="task.data.status = status">
                                        {{ display }}
                                    </q-btn>
                                </q-card>
                            </div>
                        </q-menu>
                    </q-btn>

                    <!-- Deadline -->
                    <div>Deadline</div>
                    <q-btn class="deadline_btn q-mb-md" outline color="grey-8" icon="event" style="width:100%" no-caps>
                        <span class="q-pl-sm">{{ deadline_computed }}</span>
                        <q-menu anchor="bottom middle" self="top middle" :offset="[0, 1]" v-model="show_calendar_mobile"
                            style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
                            <q-card class="calendar_card flex column">
                                <div class="pop_triangle self-center" style="z-index: 1"></div>
                                <q-date minimal v-model="task.data.deadline"
                                    style="box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)"
                                    mask="DD MMM YYYY" :options="no_dateline_before_today" />
                            </q-card>
                        </q-menu>
                        <q-tooltip v-if="days_remaining != null" :delay="350" anchor="top middle" self="center middle">
                            {{ `${days_remaining} days remaining` }}
                        </q-tooltip>
                        <q-tooltip v-else :delay="350" anchor="top middle" self="center middle">
                            no due date
                        </q-tooltip>
                    </q-btn>

                    <!-- Description -->
                    <div>Description</div>
                    <q-input class="q-mb-md" readonly dense outlined v-model="task.data.description" style="width:100%">
                        <q-menu class="description_input" cover anchor="top middle">
                            <q-input autofocus outlined v-model="task.data.description" type="textarea" />
                        </q-menu>
                    </q-input>

                </div>
            </q-dialog>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import { debounce } from 'src/utils/events.js'
import TaskAPI from 'src/services/task.api';
import { useAppStore } from 'src/stores/AppStore';
import { Status_Display, Status_Color } from 'src/utils/data/status.js'

export default defineComponent({
    props: {
        task_prop: Object,
        ui_info: Object,
        is_last: Boolean,
    },
    data() {
        return {
            // Task Data
            task: {},

            // Status
            status_display: Status_Display,
            status_color: Status_Color,

            // Update Debounced Delay
            update_debouncer: debounce(350),
            // Versioning for update revert.
            last_version: null,
            is_reverted: false,

            // UI
            show_calendar: false,
            show_completion_date: false,

            // Responsiveness - Mobile
            show_mobile_edit: false,
            show_calendar_mobile: false,
        }
    },
    computed: {
        deadline_computed() {
            if (this.task.data.deadline == null || this.task.data.deadline == '') return ''
            const [d, m, y] = this.task.data.deadline.split(' ')
            const date = new Date()
            const year = date.getFullYear();
            let display_deadline = `${d} ${m}`
            if (y != year) display_deadline += `, ${y}`
            return display_deadline
        },
        days_remaining() {
            if (this.task.data.deadline == null || this.task.data.deadline == '') return null
            const deadline = Date.parse(this.task.data.deadline)
            const today = new Date()
            const per_day = 24 * 60 * 60 * 1000
            return Math.ceil((deadline - today) / (per_day))
        },
        username() {
            return useAppStore().user.name
        },
        user_email() {
            return useAppStore().user.email
        },
        connections() {
            return useAppStore().connection
        }
    },
    watch: {
        'task.data.deadline': {
            handler(new_value, old_value) {
                if (!this.initializing) this.$emit('deadline_changed')
            },
            deep: true
        },
        'task.data': {
            handler(new_value, old_value) {
                if (this.initializing) return
                if (this.is_reverted) {
                    this.is_reverted = false
                    return
                }
                this.update_debouncer(this.update_task, new_value)
                this.show_calendar = false
                this.$emit('task_changed')
            },
            deep: true,
        },
        'task.data.status': {
            handler(new_value, old_value) {
                if (!this.initializing && new_value == 'completed') {
                    this.show_completion_date = true
                }
            },
            deep: true
        },
    },
    created() {
        this.initializing = true
        this.task = this.task_prop

        // Task versioning, for revert purposes.
        this.last_version = JSON.stringify(this.task.data)
    },
    mounted() {
        this.initializing = false
    },
    methods: {
        update_task(task_data) {
            TaskAPI.update_task(task_data)
                .then(() => {
                    // Task update success, save the latest version.
                    this.last_version = JSON.stringify(task_data)
                })
                .catch((e) => {
                    // Task update failed, revert task to the last version.
                    this.is_reverted = true
                    this.task.data = JSON.parse(this.last_version)

                    // Notify the error message if error out 400, update failures.
                    const response_code = e.response.status
                    const update_error_message = e.response.data
                    if (response_code == 400) {
                        this.$q.notify({
                            message: update_error_message,
                            icon: 'error',
                            position: 'bottom-right',
                            color: 'orange-7'
                        })
                    }
                })
        },
        assign_task(connection) {
            this.task.data.owner_name = connection.name
            this.task.data.owner_email = connection.email
        },
        no_dateline_before_today(date) {
            const per_day = 24 * 60 * 60 * 1000
            return Date.parse(date) >= Date.now() - per_day
        },
        input_estimated_time(e) {
            if (!(48 <= e.which && e.which <= 57) || (this.task.data.estimated_time >= 10_000)) {
                e.preventDefault()
            }
        },

        // Responsiveness - Mobile Design Methods
        mobile_edit() {
            this.show_mobile_edit = true
        },
    }
})
</script>

<style scoped lang="scss">
// Dark Mode
.body--dark {
    .task-col {
        border-color: $grey-9;
    }

    .task-main {
        &:hover {
            background-color: $dark-bg-fill-1;
        }

        ::v-deep {
            .q-field--outlined .q-field__control:before {
                border: 0px solid $lime-11;
                transition: border-color 0.36s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .q-field--outlined:hover .q-field__control:before {
                border: 1px solid $lime-11;
                transition: border-color 0.36s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .q-field__control {
                color: $lime-11;
            }
        }
    }

    .checkbox_selection {
        ::v-deep {
            .q-checkbox__inner--truthy {
                color: $cyan-9;
            }
        }
    }

    .title_input {
        ::v-deep {

            input,
            select,
            textarea {
                color: $grey-5 !important;
                -webkit-text-fill-color: $grey-5 !important;
                -webkit-background-clip: text !important;
                background-clip: text !important;
            }
        }
    }

    .assign_owner_btn {
        color: $grey-5 !important;
    }

    .assign_to_card {
        border: 1px solid $cyan-10;
    }

    .status_card {
        border: 1px solid $cyan-10;
    }

    .calendar_card {
        border: 1px solid $cyan-10;
    }

    .col-borderhover {
        ::v-deep {
            .q-btn--outline:before {
                border: 0px solid $lime-11;
            }

            .q-btn--outline:hover,
            .q-btn--outline:active {
                border: 1px solid $lime-11;
            }
        }
    }

    .deadline_btn {
        color: $grey-5 !important;
    }

    .highlight {
        background-color: $dark-bg-fill-2 !important;
    }
}

// Light Mode
.body--light {
    .task-main {
        ::v-deep {
            .q-field--outlined .q-field__control:before {
                border: 0px solid rgba(0, 0, 0, 0.24);
                transition: border-color 0.36s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .q-field--outlined:hover .q-field__control:before {
                border: 1px solid rgba(0, 0, 0, 0.24);
                transition: border-color 0.36s cubic-bezier(0.4, 0, 0.2, 1);
            }
        }
    }

    .col-borderhover {
        ::v-deep {
            .q-btn--outline:before {
                border: 0px solid currentColor;
            }

            .q-btn--outline:hover,
            .q-btn--outline:active {
                border: 1px solid currentColor;
            }
        }
    }

    .highlight {
        background-color: $blue-1 !important;
    }
}

.pop_triangle {
    // Doesn't work with task at lower positions.
    // width: 0;
    // height: 0;
    // border-left: 8px solid transparent;
    // border-right: 8px solid transparent;
    // border-bottom: 8px solid white;

    // This for now..
    height: 8px;
}

::v-deep {
    .q-date {
        box-shadow: none;
    }
}

.task-main {
    display: flex;
    height: 50px;
    position: relative;

    &:hover,
    &:active {
        background-color: $grey-2;
        box-shadow: 0px 3px 10px -3px rgba(0, 0, 0, 0.2);
    }

}

.task-col {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    border: 1px solid #d0d4e4;
    border-top: 0;

    &--noleft {
        border-left: 0
    }
}

.resize-column-feedback {
    background-color: $primary;
    opacity: 0;
    position: absolute;
    width: 2px;
    top: -2px;
    right: 0px;
    bottom: 0px;
    border-radius: 0;
}

// Responsive
@media (max-width: 600px) {
    .task_column_hide_mobile {
        display: none;
    }

    .mobile_edit {
        display: block !important;
    }

    .task_column_title {
        justify-content: left !important;
    }

    .title_input {
        padding-left: 10px;
        width: 77% !important;
    }
}
</style>
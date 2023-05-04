<template >
    <div class="main_container flex" style="width: 100%" ref="main_container">
        <!-- Task List Toolbar (Add, Search, Delete etc.) -->
        <div class="flex no-wrap" style="margin-bottom: 3em; width:100%" @click="show_adv_search = false">
            <q-toolbar class="main_toolbar bg-indigo-5 text-white rounded-borders justify-between">
                <div class="flex">
                    <!-- Add Task Button -->
                    <q-btn @click.stop="add_task" :disabled="adding_task || readonly" class="q-mr-md" no-caps>Add
                        Task</q-btn>

                    <!-- Basic Search -->
                    <div class="basic_search row items-center search">
                        <q-input dark dense standout v-model="basic_search_text" placeholder="Search"
                            input-class="text-right">
                            <template v-slot:append>
                                <q-icon v-if="basic_search_text == ''" name="search" class="cursor-pointer q-mr-sm" />
                                <q-icon v-else name="clear" class="cursor-pointer q-mr-sm"
                                    @click="basic_search_text = ''" />
                            </template>
                        </q-input>

                        <!-- Advanced Search Component -->
                        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                            <q-card v-show="show_adv_search" class="fixed column q-px-lg q-py-lg"
                                style="z-index:2000; min-width: 800px" @click.stop="" ref="adv_search_component"
                                :style="{ 'top': dragging_search_component_top + 'px' }"
                                @mousemove="drag_search_component($event)" @mouseup="dragend_search_component">
                                <div class="absolute row justify-center items-center"
                                    @mousedown="dragstart_search_component($event)"
                                    style="width: 100px; height: 30px; right: 50px">
                                    <q-icon name="drag_indicator" color="grey-8" size="1.8em" style="cursor: move">
                                    </q-icon>
                                </div>
                                <TaskSearchRules :tasks_prop="tasks" @update_search="update_search" />
                            </q-card>
                        </transition>
                    </div>

                    <!-- Advanced Search Toggle Button -->
                    <div class="advanced_search_btn q-ml-xs q-px-xs cursor-pointer row items-center"
                        @click.stop="show_adv_search = !show_adv_search; basic_search_text = ''; dragging_search_component = false">
                        <q-tooltip anchor="top middle" self="center middle">
                            Advanced Search
                        </q-tooltip>
                        <q-icon name="keyboard_arrow_down" size="1.45em" class="text-grey-3"></q-icon>
                    </div>
                </div>

                <!-- Delete Task Button -->
                <div class=" flex">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <q-btn v-if="selected_tasks.length" color="red-5" no-caps
                            @click.stop="confirm_delete_selected_tasks"><q-icon name="delete" />Delete</q-btn>
                    </transition>

                    <!-- Delete Confirmation Dialog -->
                    <q-dialog v-model="show_delete_confirmation">
                        <q-card>
                            <q-card-section>
                                <div class="text-h6 text-red-7 row items-center">
                                    <span class="q-mr-sm">
                                        {{ selected_tasks.length <= 1 ? 'Deleting Task' : 'Deleting Tasks' }} </span>
                                            <q-icon name="delete" color="red-7"></q-icon>
                                </div>
                            </q-card-section>

                            <q-card-section class="q-pt-none" style="min-width: 400px">
                                {{ selected_tasks.length <= 1 ? 'Delete the selected task?' : `Delete the
                                                                    ${selected_tasks.length} selected tasks?` }} </q-card-section>
                                    <q-checkbox v-model="always_delete" label="Do not ask me again" class="q-ml-sm"
                                        color="red-5" />

                                    <!-- Confirm Delete Button -->
                                    <q-card-actions align="right">
                                        <q-btn no-caps flat label="Delete" color="red-6" @click="delete_selected_tasks"
                                            v-close-popup />
                                    </q-card-actions>
                        </q-card>
                    </q-dialog>
                </div>
            </q-toolbar>
        </div>

        <!-- Task List Container -->
        <div ref="main" class="task-header-container shadow-4 q-mb-xl"
            style="overflow:hidden; border-radius: 8px; box-sizing: border-box;"
            :style="[{ 'width': row_width + 'px' }, { 'pointer-events': readonly ? 'none' : 'auto' }]">
            <!-- Header -->
            <div style="display: flex">
                <!-- Select All Visible Tasks -->
                <div class="task-header" style="border-top-left-radius: 8px;">
                    <q-checkbox v-model="selected_all" @click="select_all" />
                </div>

                <!-- ID (Header) -->
                <div class="task-header task_header_hide_mobile task-header--noleft" style="min-width:45px">
                    <div>ID</div>
                </div>

                <!-- Title (Header) -->
                <div class="task-header task-header--noleft" :style="{ width: col_ui_info.sizes[0] + 'px' }">
                    <div>{{ col_ui_info.title[0] }}</div>
                    <div @mousedown="resizestart($event, 0)" class="resize-column"
                        :class="{ 'resize-column-feedback': col_ui_info.resizing[0] }"></div>
                </div>

                <!-- Owner (Header) -->
                <div class="task-header task_header_hide_mobile task-header--noleft"
                    :style="{ width: col_ui_info.sizes[1] + 'px' }">
                    <div>{{ col_ui_info.title[1] }}</div>
                    <div @mousedown="resizestart($event, 1)" class="resize-column"
                        :class="{ 'resize-column-feedback': col_ui_info.resizing[1] }"></div>
                </div>

                <!-- Status (Header) -->
                <div class="task-header task_header_hide_mobile task-header--noleft"
                    :style="{ width: col_ui_info.sizes[2] + 'px' }">
                    <div>{{ col_ui_info.title[2] }}</div>
                    <div @mousedown="resizestart($event, 2)" class="resize-column"
                        :class="{ 'resize-column-feedback': col_ui_info.resizing[2] }"></div>
                </div>

                <!-- Dateline (Header) -->
                <div class="task-header task_header_hide_mobile task-header--noleft"
                    :style="{ width: col_ui_info.sizes[3] + 'px' }">
                    <div>{{ col_ui_info.title[3] }}</div>
                    <div @mousedown="resizestart($event, 3)" class="resize-column"
                        :class="{ 'resize-column-feedback': col_ui_info.resizing[3] }"></div>
                </div>

                <!-- Description (Header) -->
                <div class="task-header task_header_hide_mobile task-header--noleft"
                    :style="{ width: col_ui_info.sizes[4] + 'px' }">
                    <div>{{ col_ui_info.title[4] }}</div>
                    <div @mousedown="resizestart($event, 4)" class="resize-column"
                        :class="{ 'resize-column-feedback': col_ui_info.resizing[4] }"></div>
                </div>

                <!-- Estimated Time (Header) -->
                <div class="task-header task_header_hide_mobile task-header--noleft"
                    :style="{ width: col_ui_info.sizes[5] + 'px' }" style="border-top-right-radius: 8px;">
                    <div>{{ col_ui_info.title[5] }}</div>
                </div>
            </div>

            <!-- Task Row -->
            <transition-group name="tasklist" tag="div" :style="[{ 'pointer-events': readonly ? 'none' : 'auto' }]">
                <template v-for="(task, index) in visible_tasks" :key="task.data.id">
                    <TaskRow @click="focus_task(task)" :task_prop="task" :ui_info="col_ui_info"
                        :is_last="index == visible_tasks.length - 1" :readonly="readonly" ref="tasks" class="tasklist-item"
                        @deadline_changed="sort_tasks" />
                </template>
            </transition-group>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAppStore } from 'src/stores/AppStore'
import TaskRow from './TaskRow.vue'
import TaskSearchRules from './rules/TaskSearchRules.vue'
import TaskAPI from 'src/services/task.api'

export default defineComponent({
    components: {
        TaskRow,
        TaskSearchRules,
    },
    props: {
        // The task list's main owner
        user_id: Number,

        // Readonly list
        readonly: Boolean,
    },
    data() {
        return {
            // Task List
            tasks: [],

            // Add Task
            adding_task: false,

            // Full selection
            selected_all: false,

            // Columns - Resizing
            col_ui_info: {
                title: ["Task", "Owner", "Status", "Due Date", "Description", "Estimated Hours"],
                sizes: [0, 0, 0, 0, 0, 0],
                resizing: [false, false, false, false, false, false],
                ratio: [0.2, 0.15, 0.15, 0.15, 0.25, 0.1]
            },
            check_box_size: 42,
            check_box_and_id_col_sizes: (42 + 45),

            // Searching - Basic
            basic_search_text: "",

            // Searching - Advanced
            show_adv_search: false,
            dragging_search_component: false,
            dragging_search_component_top: 227,

            // Delete Confirmation Dialog
            show_delete_confirmation: false,
            always_delete: false,
            always_delete_confirmed: false, // Remember always delete option.
        }
    },
    created() {
        this.fetch_task_list()
    },
    mounted() {
        // Ratio for resizing the task row.
        const padding = 20
        let w = this.$refs.main_container.getBoundingClientRect().width - this.check_box_and_id_col_sizes - padding

        // Is mobile.
        if (w <= 600) {
            this.col_ui_info.ratio = [1, 0, 0, 0, 0, 0]
            w = this.$refs.main_container.getBoundingClientRect().width - this.check_box_size
        }
        for (const i in this.col_ui_info.sizes) {
            this.col_ui_info.sizes[i] = this.col_ui_info.ratio[i] * w
        }
    },
    computed: {
        // All selected tasks.
        selected_tasks() {
            const selection = []
            for (const i in this.tasks) {
                if (this.tasks[i].selected) {
                    selection.push(i)
                }
            }
            return selection
        },

        // All visible searched tasks.
        visible_tasks() {
            const tasks = []
            for (const t of this.tasks) {
                if (t.visible) {
                    tasks.push(t)
                }
            }
            return tasks
        },

        // Requires invalidation.
        tasks_dirty() {
            return useAppStore().tasks_dirty
        },

        // Tasks - Index mappings
        task_index_map() {
            const indices = new Map()
            this.tasks.forEach((t, i) => indices.set(t.data.id, i))
            return indices
        },

        // Row width
        row_width() {
            let total_width = 0
            for (const width of this.col_ui_info.sizes) {
                total_width += width
            }
            total_width += this.check_box_and_id_col_sizes
            return total_width
        },
    },
    watch: {
        // Basic searching.
        basic_search_text(new_value, old_value) {
            if (this.tasks.length == 0) return
            this.basic_search(new_value)
        },

        // Task is dirty and requires invalidation.
        tasks_dirty(new_value, old_value) {
            if (new_value) {
                this.fetch_task_list(true)
            }
        },

        // Task list user changes. User changed from web route query.
        user_id: {
            handler(new_value, old_value) {
                this.fetch_task_list(true)
            },
        }
    },
    methods: {
        // API - To fetch all the tasks
        fetch_task_list(clear_all = false) {

            // Invalidates the task list if clear_all is set.
            if (clear_all) {
                this.tasks.splice(0, this.tasks.length)
            }

            // The query task list of the user id.
            TaskAPI.get_tasks(this.user_id)
                .then((res) => {
                    // Pushes to the task list.
                    res.data["TaskList"].forEach(task => {
                        task = this.parse_task_response(task)
                        this.tasks.push(task)
                    });

                    // Sort all the tasks.
                    this.sort_tasks()
                })
        },

        // API Helper - Parses Task data
        parse_task_response(task_data) {
            const task = {
                selected: false,
                focused: false,
                visible: true,
                data: task_data,
            }
            return task
        },

        // Delete Selected Tasks - Confirmation
        confirm_delete_selected_tasks() {
            if (this.always_delete_confirmed) { // Delete if option remembered
                this.delete_selected_tasks()
            } else { // Show Delete Confirmation Dialog
                this.always_delete = false
                this.show_delete_confirmation = true
            }
        },

        // Delete Selected Tasks
        delete_selected_tasks() {
            // Remember delete confirmation choice
            this.always_delete_confirmed = this.always_delete

            // Delete Task
            TaskAPI.delete_tasks(this.selected_tasks.map(i => this.tasks[i].data.id))
                .then(() => {
                    if (this.selected_tasks.length > 4) {
                        this.$q.notify({
                            message: `Deleted ${this.selected_tasks.length} tasks`,
                            icon: 'delete',
                            position: 'bottom-right',
                            color: 'red-7'
                        })
                    } else {
                        this.selected_tasks.forEach(i => {
                            this.$q.notify({
                                message: `Deleted ${this.tasks[i].data.title}`,
                                icon: 'delete',
                                position: 'bottom-right',
                                color: 'red-7'
                            })
                        })
                    }
                    this.selected_tasks.reverse().forEach(i => this.tasks.splice(i, 1))
                })
                .finally(() => {
                    this.selected_all = false
                })
        },

        // Add New Task
        add_task() {
            if (this.adding_task) return
            this.adding_task = true
            TaskAPI.add_task({ title: "New task" })
                .then((res) => {
                    let task = res.data["Task"]
                    task = this.parse_task_response(task)
                    this.tasks.push(task)
                    this.$q.notify({
                        message: `Added a task!`,
                        icon: 'playlist_add',
                        position: 'bottom-right',
                        color: 'primary'
                    })
                })
                .finally(() => {
                    this.adding_task = false
                })
        },

        // Sort Tasks
        sort_tasks() {
            this.tasks.sort((a, b) => {
                const indices = this.task_index_map
                if (!a.data.deadline && !b.data.deadline) return a.data.id < b.data.id ? -1 : 1
                if (!a.data.deadline) return 1
                if (!b.data.deadline) return -1
                const date_a = Date.parse(a.data.deadline)
                const date_b = Date.parse(b.data.deadline)
                if (date_a == date_b) return indices.get(a.data.id) < indices.get(b.data.id) ? -1 : 1
                return date_a < date_b ? -1 : 1
            })
        },

        // Basic Searching
        basic_search(search_value) {
            if (search_value == "") {
                for (const t of this.tasks) {
                    t.visible = true
                }
            } else {
                for (const t of this.tasks) {
                    let ok = false
                    for (const col of Object.keys(t.data)) {
                        if (!t.data[col]) continue
                        let col_str_val = t.data[col].toString()
                        col_str_val = col_str_val.replace(/_/g, ' ') // Replace underscores.
                        // Basic matching on the column values.
                        if (col_str_val == search_value || col_str_val.match(new RegExp(search_value, "i"))) {
                            ok = true
                            break
                        }
                    }
                    t.visible = ok
                }
            }
        },

        // Update Search
        update_search(visibility) {
            for (const i in visibility) {
                this.tasks[i].visible = visibility[i]
            }
        },

        // Selection - All Tasks
        select_all() {
            // Selects all visible tasks.
            for (const i in this.tasks) {
                const t = this.tasks[i]
                if (t.visible) {
                    t.selected = this.selected_all
                }
            }
        },

        // Columns UI Resizing
        resizestart(e, col_idx) {
            this.mx = e.x
            this.drag_ev = this.resizemove.bind(this, col_idx)
            document.addEventListener("mousemove", this.drag_ev, false)
            const stop_ev = this.resizestop.bind(this, col_idx)
            window.addEventListener("mouseup", stop_ev, false)
            e.preventDefault()
            this.col_ui_info.resizing[col_idx] = true
        },
        resizestop(col_idx) {
            document.removeEventListener("mousemove", this.drag_ev, false)
            this.col_ui_info.resizing[col_idx] = false
        },
        resizemove(col_idx, e) {
            const dx = e.clientX - this.mx
            const min_width = 140
            const old_width = this.col_ui_info.sizes[col_idx]
            const new_width = Math.max(min_width, old_width + dx)
            if (old_width != new_width) {
                this.col_ui_info.sizes[col_idx] = new_width
                if (new_width == min_width) {
                    this.mx = e.x - (old_width + dx - min_width)
                } else {
                    this.mx = e.x
                }
                const total = this.col_ui_info.sizes.reduce((s, a) => s + a, this.check_box_and_id_col_sizes)
                this.$refs.main.style.width = total + "px";
            }
        },

        // Advanced Search - Dragging
        dragstart_search_component(e) {
            this.dragging_search_component = true
            this.dragging_search_component_x = e.clientX
            this.dragging_search_component_y = e.clientY
        },
        drag_search_component(e) {
            if (this.dragging_search_component) {
                const search_component = this.$refs.adv_search_component.$el
                search_component.style.top = (search_component.offsetTop - (this.dragging_search_component_y - e.clientY)) + "px"
                search_component.style.left = (search_component.offsetLeft - (this.dragging_search_component_x - e.clientX)) + "px"
                this.dragging_search_component_x = e.clientX
                this.dragging_search_component_y = e.clientY
                this.dragging_search_component_top = search_component.style.top
            }
        },
        dragend_search_component() {
            this.dragging_search_component = false
        },

        // Responsive
        focus_task(task) {
            task.focused = true
            if (this.last_task_focused && task != this.last_task_focused) {
                this.last_task_focused.focused = false
            }
            this.last_task_focused = task
        },
    }
})
</script>

<style scoped lang="scss">
// Dark Mode
.body--dark {
    .main_toolbar {
        background-color: $dark-bg-fill-3 !important;
        transition: all 0.35s ease;
    }

    .task-header-container {
        box-shadow: none;
    }

    .task-header {
        color: $cyan-2;
        border-color: $dark-bg-fill-4;

        &:hover {
            background-color: $dark-bg-fill-1;
        }
    }

    .advanced_search_btn {
        background-color: $dark-bg-fill-4;

        &:hover {
            background-color: $dark-bg-fill-2;
        }
    }
}

// Light Mode
.body--light {
    .advanced_search_btn {
        background-color: #6875c4;

        &:hover {
            background-color: #737fc8;
        }
    }
}

.search {
    &::v-deep .q-field__control {
        border-radius: 0px;
        border-top-left-radius: 5px;
        border-bottom-left-radius: 5px;
    }
}

.advanced_search_btn {
    transition: all 0.2s;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}

.task-header {
    cursor: default;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    border: 1px solid #d0d4e4;

    &--noleft {
        border-left: 0
    }

    &:hover {
        background-color: $grey-2;

        .resize-column {
            background-color: $grey-4;
            opacity: 1;
        }
    }
}

.resize-column {
    background-color: $primary;
    cursor: col-resize;
    position: absolute;
    top: 0px;
    bottom: 0px;
    right: 0px;
    width: 6px;
    opacity: 0;
    border-radius: 2px;
}

.resize-column-feedback {
    background-color: $primary !important;
    opacity: 1;
}

.tasklist-enter-from {
    opacity: 0;
    transform: translateY(-20px) scaleX(0.9);
}

.tasklist-leave-to {
    opacity: 0;
    transform: scaleX(0.9);
}

.tasklist-enter-active,
.tasklist-move {
    transition: all 0.4s ease;
}

.tasklist-leave-active {
    transition: all 0.4s ease;
    position: absolute;
}

// Responsive
@media (max-width: 600px) {
    .basic_search {
        display: none;
    }

    .advanced_search_btn {
        display: none;
    }

    .task_header_hide_mobile {
        display: none;
    }
}
</style>
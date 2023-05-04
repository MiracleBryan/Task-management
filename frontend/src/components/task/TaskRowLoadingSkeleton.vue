<template>
    <div class="task-main" :class="{ highlight: task.selected }" @click="highlight_row"
        style="box-sizing: border-box; opacity: 0.35">
        <div class="task-col">
            <q-checkbox v-model="this.task.selected" />
        </div>

        <!-- Title -->
        <div class="task-col task-col--noleft" :style="{ width: ui_info.sizes[0] + 'px' }">
            <q-input dense outlined v-model="task.title" style="width:90%" />
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[0] ? 1 : 0 }"></div>
        </div>

        <!-- Owner -->
        <div class="task-col task-col--noleft col-borderhover" :style="{ width: ui_info.sizes[1] + 'px' }">
            <q-btn outline color="grey-8" no-caps :label="task.owner_email" style="width:90%">
                <q-menu auto-close anchor="bottom middle" self="top middle" :offset="[0, 1]"
                    style="background-color: transparent; border-radius: 8px; box-shadow: none; overflow: visible">
                    <div class="flex column">
                        <div class="pop_triangle self-center" style="z-index: 1"></div>
                        <div class="flex column bg-white"
                            style="width: 225px; border-radius: 8px; padding-bottom: 1.45em; box-shadow: 0 1px 5px rgb(0 0 0 / 20%), 0 2px 2px rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%)">
                            <div class="text-grey-7 q-mx-lg q-mt-md">Assign to</div>
                            <q-btn v-if="task.owner_email != task.creator_email" no-caps flat
                                class="text-grey-8 self-center" style="width:200px; margin-top: 0.5em"
                                @click="assign_task(task.creator_email)">Myself</q-btn>
                            <template v-for="(conn_email, index) in connections_prop" :key="index">
                                <q-btn v-if="task.owner_email != conn_email" no-caps flat class="text-grey-8 self-center"
                                    style="width:200px; margin-top: 0.5em" @click="assign_task(conn_email)">{{ conn_email
                                    }}</q-btn>
                            </template>
                        </div>
                    </div>
                </q-menu>
            </q-btn>
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[1] ? 1 : 0 }"></div>
        </div>

        <!-- Status -->

        <div class="task-col task-col--noleft" :style="{ width: ui_info.sizes[2] + 'px' }">
            <q-spinner-gears size="50px" color="grey-8" />
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[2] ? 1 : 0 }"></div>
        </div>

        <!-- Dateline -->
        <div class="task-col task-col--noleft col-borderhover" :style="{ width: ui_info.sizes[3] + 'px' }">
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[3] ? 1 : 0 }"></div>
        </div>

        <!-- Description -->
        <div class="task-col task-col--noleft col-borderhover" :style="{ width: ui_info.sizes[4] + 'px' }">
            <q-input readonly dense outlined v-model="task.description" style="width:90%">
                <q-menu cover anchor="top middle">
                    <q-input outlined v-model="task.description" type="textarea" />
                </q-menu>
            </q-input>
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[4] ? 1 : 0 }"></div>
        </div>

        <!-- Estimated_time -->
        <div class="task-col task-col--noleft col-borderhover" :style="{ width: ui_info.sizes[4] + 'px' }">
            <q-input readonly dense outlined v-model="task.estimated_time" style="width:90%">
                <q-menu cover anchor="top middle">
                    <q-input outlined v-model="task.estimated_time" type="textarea" />
                </q-menu>
            </q-input>
            <div class=" resize-column-feedback" :style="{ opacity: ui_info.resizing[4] ? 1 : 0 }"></div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    props: {
        task_prop: Object,
        connections_prop: Array,
        ui_info: Object,
    },
    data() {
        return {
            task: {
                selected: false
            }
        }
    }
})
</script>

<style scoped lang="scss">
.pop_triangle {
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 8px solid white;
}

::v-deep {
    .q-date {
        box-shadow: none;
    }
}

.highlight {
    background-color: $blue-1 !important;
}

.task-main {
    display: flex;
    height: 50px;

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
</style>
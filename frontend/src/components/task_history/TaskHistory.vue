<template>
    <q-dialog v-model="show">
        <q-card class="q-px-md q-py-md">
            <q-card-section>
                <div class="text-h5 text-weight-bold text-center text-teal-13">Task History</div>
            </q-card-section>

            <q-list class="bg-white-9 text-black shadow-2 rounded-borders" style="max-width: 500px; width: 100%;">
                <q-item>
                    <q-item-section side>
                        <div class="text-subtitle1 text-weight-bold text-teal-14" style="min-width: 55px; width: 100%;">Task
                            Completion</div>
                    </q-item-section>
                </q-item>

                <q-separator />

                <q-item>
                    <q-item-section side>
                        <div class="text-body2 text-light-blue-7" style="min-width: 200px; width: 100%;">Early (~{{
                            this.early }}%):</div>
                    </q-item-section>
                    <q-item-section class="text-right">
                        <div>{{ series[1] }}</div>
                    </q-item-section>
                </q-item>

                <q-separator />

                <q-item>
                    <q-item-section side>
                        <div class="text-body2 text-light-blue-7" style="min-width: 60px; width: 100%;">On Time (~{{
                            this.on_time }}%):</div>
                    </q-item-section>
                    <q-item-section class="text-right">
                        <div>{{ series[0] }}</div>
                    </q-item-section>
                </q-item>

                <q-separator />

                <q-item>
                    <q-item-section side>
                        <div class="text-body2 text-light-blue-7" style="min-width: 60px; width: 100%;">Late (~{{ this.late
                        }}%):</div>
                    </q-item-section>
                    <q-item-section class="text-right">
                        <div>{{ series[2] }}</div>
                    </q-item-section>
                </q-item>


            </q-list>
            <VueApexCharts width="500" type="donut" :options="options" :series="series"></VueApexCharts>
        </q-card>
    </q-dialog>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
import TaskAPI from 'src/services/task.api'

export default {
    props: {
        user_id: Number,
        is_dark: Boolean,
    },
    components: {
        VueApexCharts,
    },
    data() {
        return {
            tasks: [],
            show: false,
            update: false,
            early: 0,
            late: 0,
            on_time: 0,
            dark: false,
            options: {
                plotOptions: {
                    pie: {
                        donut: {
                            labels: {
                                show: true,
                                name: {
                                    show: true
                                },
                                value: {
                                    show: true,
                                    fontSize: '22px',
                                    fontFamily: 'Calibri, sans-serif',
                                    fontWeight: 500,
                                    color: '#cfcfc4',
                                },
                                total: {
                                    show: true,
                                    label: 'Tasks Completed',
                                    fontSize: '22px',
                                    fontFamily: 'Calibri, sans-serif',
                                    fontWeight: 600,
                                    color: '#cfcfc4',
                                    formatter: function (w) {
                                        return w.globals.seriesTotals.reduce((a, b) => {
                                            return a + b
                                        }, 0)
                                    }
                                }
                            }
                        }
                    }
                },
                chart: {
                    width: 200
                },
                legend: {
                    position: 'right',
                    labels: {
                        colors: '#cfcfc4'
                    }
                },
                labels: [],
                colors: [],
                dataLabels: {
                    enabled: false
                }
            },
            series: [],
        }
    },
    methods: {
        async show_history() {
            await TaskAPI.get_tasks(this.user_id)
                .then(res => {
                    this.tasks = res.data["TaskList"]
                })

            this.show = true
            let on_time = 0
            let early = 0
            let late = 0
            let total = 0
            for (const t of this.tasks) {
                if (t.status == 'completed') {
                    if (t.deadline == null || t.deadline == '') {
                        continue
                    }
                    total += 1
                    let on_time_date = new Date(t.deadline)
                    on_time_date.setDate(on_time_date.getDate() - 7)
                    if (t.deadline < t.date_completed) {
                        late += 1
                    }
                    else if (on_time_date.toLocaleString() < t.date_completed) {
                        on_time += 1
                    }
                    else {
                        early += 1
                    }
                }
            }
            this.series = [on_time, early, late]
            this.options.labels = ['On Time', 'Early', 'Late']
            this.options.colors = ['#ffeead', '#96ceb4', '#ff6f69']
            if (total > 0) {
                this.early = Math.round(early * 100 / total)
                this.on_time = Math.round(on_time * 100 / total)
                this.late = Math.round(late * 100 / total)
            }

            if (this.is_dark) {
                this.options.legend.labels.colors = '#FFFFFF'
            }
            else {
                this.options.legend.labels.colors = '#777777'
            }
        },
    }
}
</script>

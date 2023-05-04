<template>
    <q-dialog v-model="show">
        <q-card class="q-px-md q-py-md">
            <q-card-section>
                <div class="text-h6 text-purple-4">Workload Over The Next 7 Days</div>
            </q-card-section>

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
                                    label: 'Hours of Work',
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
            },
            series: [],
        }
    },
    methods: {
        async show_busyness() {
            await TaskAPI.get_tasks(this.user_id)
                .then(res => {
                    this.tasks = res.data["TaskList"]
                })

            this.show = true
            let time_ = 0
            for (const t of this.tasks) {
                if (t.deadline == null || t.deadline == '') {
                    continue
                }
                const deadline = Date.parse(t.deadline)
                const today = new Date()
                const per_day = 24 * 60 * 60 * 1000
                if (Math.ceil((deadline - today) / (per_day)) <= 7) time_ += t.estimated_time
            }
            if (time_ == 0) {
                this.series = [40]
                this.options.labels = ['Free']
                this.options.colors = ['#FFDFD3']
                this.options.plotOptions.pie.donut.labels.total.formatter = function (w) { return 0 }

            }
            else if (time_ <= 40) {
                this.series = [40 - time_, time_]
                this.options.labels = ['Free', 'Busy']
                this.options.colors = ['#FFDFD3', '#FEC8D8']
                this.options.plotOptions.pie.donut.labels.total.formatter = function (w) { return time_ }
            }
            else if (time_ < 80) {
                this.series = [80 - time_, time_ - 40]
                this.options.labels = ['Busy', 'Double booked']
                this.options.colors = ['#FEC8D8', '#D291BC']
                this.options.plotOptions.pie.donut.labels.total.formatter = function (w) { return time_ }
            }
            else {
                this.series = [40]
                this.options.labels = ['Overbooked']
                this.options.colors = ['#D291BC']
                this.options.plotOptions.pie.donut.labels.total.formatter = function (w) { return time_ }
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
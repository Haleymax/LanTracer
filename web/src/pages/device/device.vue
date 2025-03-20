<template>
  <v-form v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="12" md="4">
          <v-combobox clearable label="主机地址"
            :items=devices>
          </v-combobox>
        </v-col>

        <v-col cols="12" md="4">
          <v-text-field v-model="day" :counter="10" :rules="dayRules" label="天数" hide-details required></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <v-btn class="mt-2" type="submit" block>查询</v-btn>
        </v-col>
      </v-row>
    </v-container>
    <div ref="DevicesInformation" class="chart-container"></div>
  </v-form>

</template>

<script setup lang="ts" name="Device">
import { computed, onMounted, ref } from 'vue'
import { useDeviceStore } from '@/store/device'
import { getDevice } from '@/api/get_device'
import * as echarts from 'echarts'

const deviceStore = useDeviceStore()

const valid = ref(true)
const host = ref('')
const day = ref('')
const devices = computed(() => deviceStore.getDeviceList())

const DevicesInformation = ref<HTMLDivElement>();

const dayRules = [
  (v: string) => !!v || 'Last name is required',
]

const fetchDevices = async () => {
  const url = "device/get_devices"
  const response = await getDevice(url)
  console.log(response)
  if (response.status) {
    const deviceData = response.message
    deviceData.forEach((device: { host: string, name: string }) => {
      deviceStore.setDevice(device.name, device.host)
    })
  }
}

const initChart = () => {
  const Chart = echarts.init(DevicesInformation.value);
  const option = {
    title: {
      text: 'ECharts 入门示例'
    },
    tooltip: {},
    legend: {
      data: ['销量']
    },
    xAxis: {
      data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    },
    yAxis: {},
    series: [{
      name: '销量',
      type: 'bar',
      data: [5, 20, 36, 10, 10, 20]
    }]
  };
  Chart.setOption(option);
}

onMounted(() => {
  fetchDevices()
  initChart()
})

</script>

<style scoped>
.chart-container {
    width: 500px;
    height: 500px;
}
</style>
<template>
  <v-form v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="12" md="4">
          <v-combobox clearable label="主机地址"
            :items="Array.from(devices)"
            item-title="name"
            item-value="host"
            v-model="host">
          </v-combobox>
        </v-col>

        <v-col cols="12" md="4">
          <v-text-field v-model="days" :counter="10" :rules="dayRules" label="天数" hide-details required></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <v-btn class="mt-2" type="button" block @click="submit">查询</v-btn>
        </v-col>
      </v-row>
    </v-container>
    <div ref="DevicesInformation" class="chart-container"></div>
  </v-form>

</template>

<script setup lang="ts" name="Device">
import { computed, onMounted, ref } from 'vue'
import { useDeviceStore } from '@/store/device'
import { getDevice, getDeviceMemory } from '@/api/get_device'
import * as echarts from 'echarts'

const deviceStore = useDeviceStore()

const valid = ref(true)
const host = ref('')
const days = ref('')
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


const submit = async () => {
  const url2: string = "device/get_menory";
  console.log(host.value, days.value);
  try {
    const response = await getDeviceMemory(url2, host.value, days.value);
    if (response.status) {
      console.log(response.message);

      const data = response.data;
      const times = data.map((item: { time: number }) => new Date(item.time * 1000).toLocaleTimeString());
      const totalMemory = data.map((item: { total_menory: number }) => item.total_menory);
      const remainingMemory = data.map((item: { remaining_menory: number }) => item.remaining_menory);

      const Chart = echarts.init(DevicesInformation.value);
      const option = {
        title: {
          text: '内存使用情况'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['总内存', '剩余内存']
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: times
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} MB'
          }
        },
        series: [
          {
            name: '总内存',
            type: 'line',
            data: totalMemory
          },
          {
            name: '剩余内存',
            type: 'line',
            data: remainingMemory
          }
        ]
      };
      Chart.setOption(option);
    }
  } catch (error) {
    console.log(error);
  }
};


onMounted(() => {
  fetchDevices()
})

</script>

<style scoped>
.chart-container {
    width: 100%;
    max-width: 1800px;
    height: 600px;
    margin: 0 auto;
}
</style>
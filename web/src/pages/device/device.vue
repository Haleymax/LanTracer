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
  </v-form>
</template>

<script setup lang="ts" name="Device">
import { computed, ref } from 'vue'
import { useDeviceStore } from '@/store/device'

const deviceStore = useDeviceStore()

const valid = ref(true)
const host = ref('')
const day = ref('')
const devices = computed(() => deviceStore.getDeviceList())
const hostRules = [
  (v: string) => !!v || '主机地址不能为空',
]
const dayRules = [
  (v: string) => !!v || 'Last name is required',
]


</script>
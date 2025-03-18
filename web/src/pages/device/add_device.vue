<template>
    <v-sheet class="mx-auto" width="300">
      <v-form @submit.prevent>
        <v-text-field
          v-model="host"
          :rules="HostRules"
          label="主机地址"
        ></v-text-field>
        <v-text-field
          v-model="name"
          :rules="NameRules"
          label="主机名称"
        ></v-text-field>
        <v-btn class="mt-2" type="submit" block @click="submit">Submit</v-btn>
      </v-form>
    </v-sheet>
  </template>

<script setup lang="ts" name="AddDevice">
import { ref } from 'vue'
import { addDevice } from '@/api/add_device'
const host = ref('')
const HostRules = [
  (v: string) => !!v || '主机地址不能为空',
]

const name = ref('')
const NameRules = [
  (v: string) => !!v || '主机名称不能为空',
]


const submit = async () => {
    const data = {
      host: host.value,
      name: name.value
    }

    const url:string = "device/add_device"

    try {
      const response = await addDevice(url, data)
      if (response.status) {
        alert('Device added')
      } else {
        alert('Device not added')
      }
    } catch (error) {
      alert('Error')
    }
}



</script>
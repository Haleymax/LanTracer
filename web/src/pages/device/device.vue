<template>
    <v-form v-model="valid">
      <v-container>
        <v-row>
          <v-col
            cols="12"
            md="4"
          >
            <v-text-field
              v-model="host"
              :counter="10"
              :rules="hostRules"
              label="主机地址"
              hide-details
              required
            ></v-text-field>
          </v-col>
  
          <v-col
            cols="12"
            md="4"
          >
            <v-text-field
              v-model="day"
              :counter="10"
              :rules="dayRules"
              label="Last name"
              hide-details
              required
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </template>

<script setup lang="ts" name="Device">
import { ref } from 'vue'

const valid = ref(true)
const host = ref('')
const day = ref('')
const hostRules = [
  (v: string) => !!v || '主机地址不能为空',
]
const dayRules = [
  (v: string) => !!v || 'Last name is required',
]


</script>
<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer">
      <v-list-item title="菜单" subtitle=""></v-list-item>
      <v-divider></v-divider>
      <v-list>
        <v-list-item to="/home">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item to="/device">
          <v-list-item-icon>
            <v-icon>mdi-memory</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>设备内存信息</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item to="/add_device">
          <v-list-item-icon>
            <v-icon>mdi-usb</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>添加设备</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item to="/devicemanagement">
          <v-list-item-icon>
            <v-icon>mdi-settings</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>节点管理</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-app-bar-title>LanTracer</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup lang="ts" name="Index">
import { ref } from 'vue'
import Device from './device/device.vue';

const drawer = ref(false)
</script>


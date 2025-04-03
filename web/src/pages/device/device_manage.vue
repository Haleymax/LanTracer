<template>
    <v-table>
      <thead>
        <tr>
          <th class="text-left">
            节点名称
          </th>
          <th class="text-left">
            地址
          </th>
          <th class="text-left">
            操作
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in devices"
          :key="item.name"
        >
          <td>{{ item.name }}</td>
          <td>{{ item.host }}</td>
          <td>
            <v-btn color="primary" small >修改</v-btn>
            <v-btn color="error" small >删除</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    
  </template>

<script setup lang="ts" name="DeviceManage">
    import { ref } from 'vue'
    const devices = ref([
        { name: 'mac-mini-01', host: "192.168.98.2" },
        { name: 'mac-mini-02', host: "192.168.98.2" },
        { name: 'mac-mini-03', host: "192.168.98.2" },
        { name: 'mac-mini-04', host: "192.168.98.2" },
        { name: 'mac-mini-05', host: "192.168.98.2" },
    ])

</script>
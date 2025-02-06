<template>
    <div class="common-layout">
      <el-container>
        <el-aside width="100px">
          <Menu></Menu>
        </el-aside>
        <el-container>
          <el-header>Header</el-header>
          <el-main>Main</el-main>
        </el-container>
      </el-container>
    </div>
</template>

<script setup lang="ts" name="Home">
import { ElContainer, ElAside, ElHeader, ElMain } from 'element-plus';


</script>

<style scoped>
.common-layout {
  width: 100%;
  height: 100%;
  background-color: white;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
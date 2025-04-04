/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import Device from '@/pages/device/device.vue'
import Index from '@/pages/index.vue'
import Home from '@/pages/home.vue'
import AddDevice from '@/pages/device/add_device.vue'
import DeviceManage from '@/pages/device/device_manage.vue'

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/device',
    name: 'Device',
    component: Device,
  },
  {
    path: '/add_device',
    name: 'AddDevice',
    component: AddDevice,
  },
  {
    path: '/devicemanagement',
    name: 'DeviceManagement',
    component: DeviceManage,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router

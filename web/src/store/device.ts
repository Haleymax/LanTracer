import { defineStore } from 'pinia'

interface Device {
  device: string
  ipaddress: string
}

export const useDeviceStore = defineStore('device', {
  state: () => ({
    devices: [] as Device[],
  }),
  actions: {
    setDevice(device: string, ipaddress: string) {
      this.devices.push({ device, ipaddress })
    },
    getDevices(): Map<string, string> {
      if (this.devices.length === 0) {
        this.devices.push({ device: 'MainHost', ipaddress: '127.0.0.1' })
      }
      return this.convertToMap(this.devices)
    },
    getDeviceList(): Map<string, string> {
      return this.convertToMap(this.devices)
    },
    convertToMap(devices: Device[]): Map<string, string> {
      const deviceMap = new Map<string, string>()
      devices.forEach(device => {
        deviceMap.set(device.device, device.ipaddress)
      })
      return deviceMap
    }
  },
})
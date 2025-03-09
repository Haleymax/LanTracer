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
    getDevices(): Device[] {
      if (this.devices.length === 0) {
        this.devices.push({ device: 'MainHost', ipaddress: '127.0.0.1' })
      }
      return this.devices
    },
    getDeviceList(): string[] {
        return this.devices.map((device) => device.device || device.ipaddress)
    }
  },
})
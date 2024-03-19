import asyncio
from bleak import BleakClient

# MAC address of your Bluetooth device
DEVICE_ADDRESS = "D8:C6:FA:05:F9:F2"

async def discover_device():
    async with BleakClient(DEVICE_ADDRESS) as client:
        services = await client.get_services()
        for service in services:
            print("=============")
            print(f"Service: {service}")
            for char in service.characteristics:
                print(f"Characteristic: {char}")

if __name__ == "__main__":
    asyncio.run(discover_device())


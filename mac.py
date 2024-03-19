import asyncio
from bleak import BleakScanner

async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        print("Name:", device.name if device.name else "Unknown",
              "MAC Address:", device.address)

if __name__ == "__main__":
    asyncio.run(scan())
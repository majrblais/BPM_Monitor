import asyncio
import os
from bleak import BleakClient

# MAC address of your Bluetooth device
DEVICE_ADDRESS = "D8:C6:FA:05:F9:F2"

# UUIDs for Heart Rate Service and its characteristic
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    output_numbers = list(data)
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for Windows and Unix-like systems
    print(output_numbers[1])
    
async def get_heart_rate():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print("Connected...")
        await client.start_notify(HR_CHAR_UUID, notification_handler)
        # No need to await anything here, keep the notifications running indefinitely
        await asyncio.Event().wait()  # This line keeps the event loop running indefinitely

if __name__ == "__main__":
    asyncio.run(get_heart_rate())

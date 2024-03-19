import asyncio
import os
from bleak import BleakClient
import matplotlib.pyplot as plt
from colorama import Fore, Back, Style  # for colored console output

# MAC address of your Bluetooth device
DEVICE_ADDRESS = "D8:C6:FA:05:F9:F2"

# UUIDs for Heart Rate Service and its characteristic
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Initialize plot
plt.ion()
fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})  # Create subplots with different heights
heart_rate_data = []
line, = ax[0].plot(heart_rate_data, 'r-')
ax[0].set_xlim(0, 30)  # Set x-axis limits
ax[0].set_xlabel('Time (seconds)')
ax[0].set_ylabel('Heart Rate (bpm)')
heart_rate_text = ax[1].text(0.5, 0.5, '', horizontalalignment='center', verticalalignment='center', fontsize=20)

# Add horizontal lines at y=50 and y=170
ax[0].axhline(y=60, color='b', linestyle='--', linewidth=1, label='CalmBoi (60 bpm)')
ax[0].axhline(y=100, color='b', linestyle='--', linewidth=1, label='Ej Shake (100 bpm)')
ax[0].legend()

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    global heart_rate_data
    output_numbers = list(data)
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for Windows and Unix-like systems
    heart_rate = output_numbers[1]
    heart_rate_data.append(heart_rate)
    heart_rate_text.set_text(f"Heart Rate: {heart_rate} bpm")

    # Update plot
    x_values = range(len(heart_rate_data))  # Generate x-values based on the length of heart_rate_data
    line.set_data(x_values, heart_rate_data)  # Update the data for the line plot
    ax[0].set_xlim(max(0, len(heart_rate_data) - 100), max(100, len(heart_rate_data)))  # Update x-axis limits for scrolling
    ax[0].set_ylim(min(heart_rate_data) - 10, max(heart_rate_data) + 10)  # Adjust y-axis limits based on heart rate data
    ax[0].relim()
    ax[0].autoscale_view()
    plt.draw()
    plt.pause(0.001)

async def get_heart_rate():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print("Connected...")
        await client.start_notify(HR_CHAR_UUID, notification_handler)
        # No need to await anything here, keep the notifications running indefinitely
        await asyncio.Event().wait()  # This line keeps the event loop running indefinitely

if __name__ == "__main__":
    asyncio.run(get_heart_rate())

from datetime import datetime
import pytz

# Define the timezone for Dhaka, Bangladesh
dhaka_timezone = pytz.timezone('Asia/Dhaka')

# Get the current time in Dhaka
current_time_dhaka = datetime.now(dhaka_timezone)

# Print the current time
print("Current time in Dhaka, Bangladesh:", current_time_dhaka.strftime("%Y-%m-%d %H:%M:%S"))

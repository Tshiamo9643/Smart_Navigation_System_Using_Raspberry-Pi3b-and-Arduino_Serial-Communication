import serial
import time
import re

# Initialize serial connection
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)

def log_data(data):
    """
    Log the raw GPS data with a timestamp.
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{current_time} - Received: {data}")

def process_data(data):
    """
    Process the GPS data to extract latitude, longitude, and date.
    """
    match = re.search(r'Location: ([\d.-]+),([\d.-]+)\s+Date (\d+/\d+/\d+)', data)
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        date = match.group(3)
        print(f"Latitude: {latitude}, Longitude: {longitude}, Date: {date}")
        return latitude, longitude, date
    else:
        print("Data format not recognized.")
        return None, None, None

def read_gps():
    """
    Read data from the GPS module and return processed data.
    """
    print("Reading GPS data...")
    if ser.in_waiting > 0:  # Check if there is data in the buffer
        data = ser.readline().decode('utf-8', errors='ignore').rstrip()  # Ignore decode errors
        log_data(data)  # Log the received data
        return process_data(data)  # Process and extract specific parts
    print("No data available.")
    return None, None, None

if __name__ == '__main__':
    try:
        while True:
            latitude, longitude, date = read_gps()
            if latitude and longitude:
                print(f"GPS Data - Latitude: {latitude}, Longitude: {longitude}, Date: {date}")
            else:
                print("No valid GPS data received.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("GPS reading stopped by User")
    finally:
        ser.close()


# import serial
# import time
# 
# ser=serial.Serial('/dev/ttyACM0',baudrate=9600)
# 
# 
# 
# while True:
#     if ser.in_waiting >0:
#         data =ser.readline().decode('utf-8').rstrip()
#         print(f"received: {data}")
#         time.sleep(1)
# 
# import serial
# import time
# 
# # Initialize serial connection
# ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
# 
# # Function to log data
# def log_data(data):
#     current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     print(f"{current_time} - Received: {data}")
# 
# # Continuously read from the serial port
# while True:
#     if ser.in_waiting > 0:  # Check if there is data in the buffer
#         data = ser.readline().rstrip()  # Read raw bytes
#         try:
#             data_str = data.decode('utf-8')  # Try decoding to UTF-8
#         except UnicodeDecodeError:
#             data_str = str(data)  # Fallback to raw string representation
#         log_data(data_str)  # Log the received data
#         if "INVALID" in data_str:
#             print("Warning: Received invalid data.")
#         time.sleep(1)  # Delay to control the loop speed
# import serial
# import time
# import re
# #import Ultrasonic_Sensor as t
# 
# # Initialize serial connection
# ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
# 
# # Function to log data
# def log_data(data):
#     current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     print(f"{current_time} - Received: {data}")
# 
# # Function to extract and log specific parts of the data
# def process_data(data):
#     match = re.search(r'Location: ([\d.-]+),([\d.-]+)\s+Date (\d+/\d+/\d+)', data)
#     if match:
#         latitude = match.group(1)
#         longitude = match.group(2)
#         date = match.group(3)
#         print(f"Latitude: {latitude}, Longitude: {longitude}, Date: {date}")
#     else:
#         print("Data format not recognized.")
# 
# # Continuously read from the serial port
# while True:
#     if ser.in_waiting > 0:  # Check if there is data in the buffer
#         data = ser.readline().decode('utf-8', errors='ignore').rstrip()  # Ignore decode errors
#         log_data(data)  # Log the received data
#         process_data(data)  # Process and extract specific parts
#         time.sleep(1)  # Delay to control the loop speed
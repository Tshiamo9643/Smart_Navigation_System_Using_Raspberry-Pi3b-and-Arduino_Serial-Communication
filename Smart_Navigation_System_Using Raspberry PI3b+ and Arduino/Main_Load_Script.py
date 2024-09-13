import subprocess

# Define the scripts to run
scripts = ["SDNS_App.py", "Ultrasonic_Sensor.py"]

# Launch each script in a subprocess
processes = [subprocess.Popen(["python3", script]) for script in scripts]

# Wait for both processes to complete
for process in processes:
    process.wait()

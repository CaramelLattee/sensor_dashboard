#generate_data.py
#generates sample sensor csv data
import csv
import random
from datetime import datetime, timedelta

def generate_sensor_data(filename, num_readings=100):
    """Generate realistic sensor readings"""

    start_time = datetime.now() - timedelta(hours=8)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp", "Voltage", "Current",
            "Temperature", "Pressure", "Status"
        ])

        for i in range(num_readings):
            timestamp = start_time + timedelta(
                        minutes=i*5)

            # Simulate realistic readings
            # Occasional failures (15% chance)
            if random.random() < 0.08:
                voltage = random.uniform(3.8, 4.4)  # LOW
            elif random.random() < 0.05:
                voltage = random.uniform(5.6, 6.2)  # HIGH
            else:
                voltage = random.uniform(4.6, 5.4)  # NORMAL

            current = random.uniform(0.75, 1.25)
            temp    = random.uniform(18.0, 37.0)
            pressure = random.uniform(1.8, 4.2)

            # Determine status
            volt_ok = 4.5 <= voltage <= 5.5
            curr_ok = 0.8 <= current <= 1.2
            status  = "PASS" if volt_ok and curr_ok \
                      else "FAIL"

            writer.writerow([
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                round(voltage,  3),
                round(current,  3),
                round(temp,     1),
                round(pressure, 3),
                status
            ])

    print(f"✅ Generated {num_readings} readings → {filename}")

if __name__ == "__main__":
    generate_sensor_data(
        "sensor_readings.csv", 100)
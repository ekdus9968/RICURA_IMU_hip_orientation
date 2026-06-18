import board
import busio
import adafruit_bno055
import time

# I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# BNO055 initialize
sensor = adafruit_bno055.BNO055_I2C(i2c)

print("BNO055 connecting...")
print("-" * 40)

while True:
    # 1. Calibration status
    sys, gyro, accel, mag = sensor.calibration_status
    print(f"Calibration - System: {sys} Gyro: {gyro} Accel: {accel} Mag: {mag}")

    # 2. Euler angles (yaw, pitch, roll)
    euler = sensor.euler
    if euler[0] is not None:
        print(f"Euler - Yaw: {euler[0]:.2f}° Pitch: {euler[1]:.2f}° Roll: {euler[2]:.2f}°")

    # 3. Quaternion
    quat = sensor.quaternion
    if quat[0] is not None:
        print(f"Quaternion - w:{quat[0]:.3f} x:{quat[1]:.3f} y:{quat[2]:.3f} z:{quat[3]:.3f}")

    # 4. Temperature (check sensors work)
    print(f"Temperature: {sensor.temperature}°C")

    print("-" * 40)
    time.sleep(1)
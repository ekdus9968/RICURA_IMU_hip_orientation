import board
import busio
import adafruit_bno055
import time

# I2C 연결
i2c = busio.I2C(board.SCL, board.SDA)

# BNO055 초기화
sensor = adafruit_bno055.BNO055_I2C(i2c)

print("BNO055 연결 확인 중...")
print("-" * 40)

while True:
    # 1. Calibration 상태 확인
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

    # 4. Temperature (센서 정상 동작 확인용)
    print(f"Temperature: {sensor.temperature}°C")

    print("-" * 40)
    time.sleep(1)
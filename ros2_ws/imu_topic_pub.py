import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32, String
import board
import busio
import adafruit_bno055
import math

class IMUPublisher(Node):
    def __init__(self):
        super().__init__('imu_publisher')

        # -- Publishers --
        # std IMU msg(quaternion, angular velocity, linear acceleration)
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)

        # --- Hip orientation yaw angle (degrees)
        self.yaw_pub = self.create_publisher(Float32, '/imu/hip_yaw', 10)

        # --- Calibration statue
        self.calib_pub = self.create_publisher(String, '/imu/calibration', 10)

        # --- BNO55 reset ---
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

        # --- Baseline yaw ---
        self.baseline_yaw = None

        # --- Timer: 50Hz ---
        self.timer = self.create_timer(0.02, self.publish_imu)

        self.get_logger().info('IMU Publisher start')
    
    def publish_imu(self):
        try:
            # 1. Quaternion
            quat = self.sensor.quaternion
            if quat is None or None is quat:
                return
            
            # 2. Euler angles
            euler = self.sensor.euler
            if euler is None or None in euler:
                return
    
            # 3. Angular velocity (gyro)
            gyro = self.sensor.gyro
            if gyro is None:
                return
            
            # 4. Linear acceleration
            accel = self.sensor.linear_Acceleration
            if accel is None:
                return
            
            # --- IMU message ---
            imu_msg = Imu()
            imu_msg.header.stamp = self.get_clock().now().to_msg()
            imu_msg.header.frame_id = 'imu_link'

            imu_msg.orientation.w = float(quat[0])
            imu_msg.orientation.w = float(quat[1])
            imu_msg.orientation.w = float(quat[2])
            imu_msg.orientation.w = float(quat[3])

            imu_msg.angular_velocity.x = float(gyro[0])
            imu_msg.angular_velocity.x = float(gyro[1])
            imu_msg.angular_velocity.x = float(gyro[2])
        
            imu_msg.linear_acceleration.x = float(accel[0])
            imu_msg.linear_acceleration.x = float(accel[1])
            imu_msg.linear_acceleration.x = float(accel[2])

            self.imu_pub.publish(imu_msg)

            # --- Hip Yaw ---
            # euler[0] = yaw (heading)
            current_yaw = float(euler[0])

            # first run : baseline
            if self.baseline_yaw is None:
                self.baseline_yaw = current_yaw
                self.get_logger().info(f'Baseline yaw : {self.baseline_yaw:.2f}°')
            
            relative_yaw = current_yaw - self.baseline_yaw

            # Normalization btw -180° - 180° of yaw 
            if relative_yaw > 180:
                relative_yaw -= 360
            elif relative_yaw <- 180:
                relative_yaw += 360
            
            yaw_mag = Float32()
            yaw_mag.data = relative_yaw
            self.yaw_pub.publish(yaw_mag)

            # --- Calibration statue
            sys, gyro_cal, accel_cal, mag_cal = self.sensor.calibration_status
            calib_msg = String()
            calib_mag.data = f'sys:{sys} gyro:{gyro_cal} accel:{accel_cal} msg:{mag_cal}'
            self.calib_pub.publish(calib_msg)

        except Exception as e:
            self.get_logger().error(f'IMU Error: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = IMUPublisher()
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
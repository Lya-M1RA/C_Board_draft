import os
import rclpy
from rclpy.node import Node
from share.msg import CBoard
import serial

class CBoardPub(Node):


    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("CBoardPub node started")

        self.cboard_pub = self.create_publisher(CBoard, "c_board", 10)

        self.ser = serial.Serial('/dev/ttyACM0', 9600)  # Please check the port name

        self.timer = self.create_timer(0.01, self.timer_callback) # Please check the frequency

    def timer_callback(self):
        if self.ser.in_waiting:
            # Read one line from serial port
            line = self.ser.readline().decode('utf-8').strip()
            # Split the line into a list of strings
            data = line.split(',')
            if len(data) == 15:
                try:
                    # Map the data to the message
                    msg = CBoard()
                    msg.gps = [float(data[0]), float(data[1])]
                    msg.chassis_motor_speed = [int(data[2]), int(data[3]), int(data[4]), int(data[5])]
                    msg.real_vcx = float(data[6])
                    msg.real_w = float(data[7])
                    msg.gyro_z = float(data[8])
                    msg.roll = float(data[9])
                    msg.pitch = float(data[10])
                    msg.yaw = float(data[11])
                    msg.linear_acc_x = float(data[12])
                    msg.gps_diff = [float(data[13]), float(data[14])]

                    # Publish the message
                    self.cboard_pub.publish(msg)
                except ValueError:
                    self.get_logger().error("Invalid data received from serial port")

def main(args=None):
    rclpy.init(args=args)
    node = CBoardPub("cboard_pub")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

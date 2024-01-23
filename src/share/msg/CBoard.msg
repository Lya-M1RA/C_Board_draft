# std_msgs/Header header

# gps (lat,lon)
float64[2]  gps

# motor
int32[4]    chassis_motor_speed
float32     real_vcx
float32     real_w

# imu
float32     gyro_z
float32     roll
float32     pitch
float32     yaw
float32     linear_acc_x

# gps_diff (x,y)
float32[2]  gps_diff
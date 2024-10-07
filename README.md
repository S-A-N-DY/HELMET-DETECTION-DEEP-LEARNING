# HELMET-DETECTION-DEEP-LEARNING
A convolutional neural network (CNN) will be developed using deep learning techniques to identify whether a person is wearing a helmet or not.
Features
Helmet Detection: The system detects whether a person is wearing a helmet using a camera and a Keras-based deep learning model.
Safety Alerts: Sends SMS alerts when:
No helmet is detected.
Abnormal heartbeat is measured.
Entry into restricted zones is detected.
GPS Tracking: Logs the geographical coordinates and sends them to a server.
Heart Rate and Oxygen Level Monitoring: Monitors the heart rate and oxygen levels using sensors and triggers the pump or alarm if thresholds are crossed.
Real-Time Camera Capture: Captures images periodically and uses them for inference.
Components
Raspberry Pi: The central unit controlling all the processes.
PiCamera: Captures images for helmet detection.
MCP3008 ADC: Analog-to-digital converter for reading heart rate and oxygen sensors.
Heart Rate & Oxygen Sensor: Measures heartbeat and oxygen levels.
Buzzer: Alerts for abnormal situations (e.g., no helmet, abnormal heart rate).
Motor Control (LED in code): Represents actions that would engage specific machinery.
GPS Module: Provides real-time latitude and longitude data.
GSM Module: Sends SMS alerts to predefined contacts.
Prerequisites
Python 3.x
TensorFlow & Keras for loading the deep learning model.
OpenCV for image handling.
Pillow for image manipulation.
Requests library for handling HTTP requests.
RPi.GPIO & gpiozero for handling Raspberry Pi GPIO pins.
Install necessary libraries via pip:

bash
Copy code
pip install tensorflow keras opencv-python pillow requests gpiozero
Setup and Installation
Hardware Setup
Connect the PiCamera to the Raspberry Pi camera interface.
Connect the MCP3008 ADC to the Raspberry Pi SPI interface.
Attach the sensors for heart rate and oxygen to the MCP3008.
Connect the GPS module and GSM module to the UART pins of the Raspberry Pi.
Connect the buzzer and motor control LEDs to the specified GPIO pins.
Software Setup
Clone the repository or transfer the code to your Raspberry Pi.
Load the deep learning model (keras_model.h5) and place it in the same directory as the script.
Modify the recipient's phone number for SMS alerts in the code:
python
Copy code
recipient="YOUR_PHONE_NUMBER"
Run the script on the Raspberry Pi:
bash
Copy code
python helmet_detection.py
Code Workflow
Helmet Detection:

The PiCamera captures an image (seed.jpg) periodically.
The image is preprocessed and normalized, then passed to a deep learning model.
The model predicts one of three classes: "Helmet," "No Helmet," or "QR Code."
If "No Helmet" is detected, a buzzer alarm is triggered and the motor is stopped.
If "Helmet" is detected, the motor is activated, and the buzzer is off.
If "QR Code" is detected, an HTTP request logs identification details to the cloud server.
GPS Location:

The GPS module fetches latitude and longitude.
The location data is converted into degrees and sent to a cloud server for logging or attached to SMS alerts.
Heart Rate & Oxygen Level Monitoring:

Heart rate and oxygen levels are read from the MCP3008 analog inputs.
If oxygen levels drop below a certain threshold, the pump is activated.
If the heart rate exceeds normal levels, an SMS alert is triggered with the location data.
Zone Monitoring:

The system monitors two restricted zones using RF signals.
When the system detects an entry into these zones, the buzzer is triggered and a warning is displayed.
Alert and Notification:

SMS alerts are sent via the GSM module when abnormal heart rate is detected or if someone enters restricted zones without wearing a helmet.
Circuit Diagram
Ensure all connections are made securely. The GPIO pins used in the code are:

Camera: Default PiCamera setup.
RF Zone Monitors: GPIO pins 16 and 19.
Buzzer: GPIO 21.
Motor (LED): GPIO 26.
Heart Rate & Oxygen Sensors: MCP3008 channels 0 and 1.
Example Output
SMS Alert:

makefile
Copy code
Heart Beat Abnormal
Lat: 13.01212 Lon: 80.0123
Console Output:

makefile
Copy code
Oxygen = 95
HB = 72
Helmet
QR Code Detected
lat in degrees: 13.0121 long in degree: 80.0123
Future Enhancements
Add more sensor inputs: Include additional sensors for environmental factors such as temperature, humidity, etc.
Improved Helmet Detection: Train a more robust deep learning model on a larger dataset to enhance accuracy in various conditions.
Cloud Integration: Extend the project by logging all data to a centralized cloud platform for real-time monitoring and analytics.

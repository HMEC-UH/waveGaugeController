// dependency: Arduino, WiFiNINA, AccelStepper
// This code is for an Arduino project that connects to WiFi, receives a value from a web request,
// and moves a stepper motor based on that value.
// It uses the AccelStepper library for controlling the stepper motor and WiFiNINA for WiFi connectivity.

#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <AccelStepper.h>

char ssid[] = "HNEI (HIG 418)"; // your network SSID (name)
char pass[] = "WETSHne!1680"; // your network password

const uint8_t stepPin = 10; // Pin connected to the stepper motor step input
const uint8_t dirPin = 11; // Pin connected to the stepper motor direction input
const uint8_t enablePin = 13; // Pin connected to the stepper motor enable input

AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin); // defining the stepper motor type and pins

WiFiServer server(80); // Create a WiFi server on port 80

int parseValue(String input) { // Function to parse the value from the input string
  int i = input.indexOf('value='); // Find the index of 'value=' in the input string
  if (i<0) {
    return -1; // If 'value=' is not found, return -1
  }
  String num = input.substring(i+1, i+6); // Extract the substring starting from 'value=' to the next 5 characters
  // Serial.print("Extracted number: ");
  // Serial.println(num);
  int space = num.indexOf(' '); // Find the index of the first space in the extracted number
  // Serial.print("Space found at: ");
  // Serial.println(space);
  if (space >= 0) { // If a space is found, trim the number to that point
    num = num.substring(0, space);
    Serial.print("Trimmed number: ");
    Serial.println(num);
  }
  return num.toInt(); // Convert the trimmed string to an integer and return it
}

void setup() { // Setup function to initialize the Arduino
  Serial.begin(115200); // Start serial communication at 115200 baud rate

  pinMode(enablePin, OUTPUT); // enabling the stepper motor
  digitalWrite(enablePin, LOW); 

  stepper.setMaxSpeed(10000); // Set the maximum speed of the stepper motor
  stepper.setAcceleration(2500); // Set the acceleration of the stepper motor

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(1000);
  } // stays in this loop until the WiFi connection is established

  IPAddress ip = WiFi.localIP(); // returns the local IP address of the wifi module
  Serial.print("IP Address: "); // Print the local IP address to the serial monitor
  Serial.println(ip);

  server.begin(); // Start the WiFi server

  stepper.setCurrentPosition(0); // home the stepper motor position
}

void loop() { // Main loop to handle incoming requests
  WiFiClient client = server.available(); // Check if a client has connected to the server
  if (!client) {
    return; // If no client is connected cut the cycle short
  }

  String request = client.readStringUntil('\r'); // Read the incoming request from the client until a carriage return is found

  // Serial.println(request);
  
  int value = parseValue(request); // Parse the value from the request string

  // Serial.print("Parsed value: ");
  // Serial.println(value);
  
  // steps to move is calculated using the input value (in mm vertically moved)
  // The reduction attached to the stepper motor is 25:1, and the stepper motor has 200 steps per revolution.
  // The lead screw has a pitch of 3mm, so the number of steps to move is calculated as follows:
  // stepsToMove = (value in mm) * (reduction ratio) * (steps per revolution) / (pitch of lead screw)
  // In this case, the calculation is:
  // stepsToMove = (value in mm) * 25 * 200 / 3

  long stepsToMove = (long)value * (long)25 * (long)200 / (long)3;

  // Serial.println(stepsToMove);

  stepper.moveTo(stepsToMove);
  
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }

  // rezero after move is complete so that it can move the desired parse distance
  stepper.setCurrentPosition(0);
  
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/plain");
  client.println("Connection: close");

  delay(1);
  client.stop();
}
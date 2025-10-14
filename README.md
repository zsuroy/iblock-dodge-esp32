# Block Dodge Game on ESP32

**Tech Stack:** MicroPython

## Resources

- Core Board: ESP32
- Temperature and Humidity Sensor: DHT11
- Buttons: x 2
- Display: OLED 0.96 inch (128x64, SSD1306)

## Demo Video

🎥 [Video Preview](src/Block-Dodge.mp4)

## Game Features

- **Block Dodging Gameplay**: Control a player at the bottom of the screen to dodge falling blocks
- **Score System**: Earn points for each block that reaches the bottom without collision
- **Real-time Temperature & Humidity Display**: Shows current environmental data from DHT11 sensor
- **Game Over & Restart**: Automatic restart after game over with score display
- **Dual Control Modes**: Both physical buttons and Web-based control
- **WiFi Access Point**: Built-in AP mode for wireless control
- **Real-time Web Interface**: Monitor game status and control via browser

## Hardware Wiring

| Module             | ESP32 Pin | Description           |
|--------------------|-----------|-----------------------|
| DHT11              | GPIO26    | Temperature & Humidity Sensor |
| OLED SCL           | GPIO10    | OLED Clock Line       |
| OLED SDA           | GPIO9     | OLED Data Line        |
| KEY1 (Left Button) | GPIO27    | Left Button           |
| KEY2 (Right Button)| GPIO28    | Right Button          |
| Power              | 3.3V/GND  | Shared for all modules |

## Game Controls

### Physical Button Controls
- **Left Button (GPIO27)**: Move player left
- **Right Button (GPIO28)**: Move player right

### Web Control Interface
- **WiFi Network**: Connect to "ESP32-Game" (Password: 12345678)
- **Access URL**: Open browser and visit the ESP32's IP address (displayed on OLED)
- **Web Controls**:
  - Left/Right arrow buttons for movement
  - Restart button for game reset
  - Real-time status display (score, temperature, humidity)

## Web Control Features

- **Responsive Design**: Works on both mobile and desktop browsers
- **Real-time Updates**: Live game status and sensor data
- **Dual Control Support**: Use both physical buttons and web controls simultaneously
- **Non-blocking Operation**: Web requests don't interrupt game flow

## Getting Started

1. **Hardware Setup**: Connect components as per wiring diagram
2. **Power On**: The ESP32 will automatically start in AP mode
3. **Connect WiFi**: Connect your device to "ESP32-Game" network
4. **Open Browser**: Navigate to the IP address shown on OLED
5. **Start Playing**: Use either physical buttons or web interface

## Development Environment

+ MacOS 10.15.7
+ Python 3.7
+ PyCharm
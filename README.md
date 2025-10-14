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
- **Button Controls**: Left and right movement using physical buttons

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

- **Left Button (GPIO27)**: Move player left
- **Right Button (GPIO28)**: Move player right

## Development Environment

+ MacOS 10.15.7
+ Python 3.7
+ PyCharm

#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <SPI.h>
#include <LoRa.h>


Adafruit_BMP280 bmp;



void setup() {
  Serial.begin(9600);
  bmp.begin();
  LoRa.begin(433E6);
}

void loop() {
    Serial.print(F("Temperature = "));
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");

    Serial.print(F("Pressure = "));
    Serial.print(bmp.readPressure()/1000);
    Serial.println(" KPa");

    Serial.print(F("Appox altitude = "));
    Serial.print(bmp.readAltitude(1015.25));
    Serial.println(" m");
    Serial.println();

    LoRa.beginPacket();
    LoRa.print(bmp.readTemperature());
    LoRa.print(",");
    LoRa.print(bmp.readPressure()/1000);
    LoRa.print(",");
    LoRa.println(bmp.readAltitude(1015.25));
    
    LoRa.endPacket();
    
    delay(2000);
}

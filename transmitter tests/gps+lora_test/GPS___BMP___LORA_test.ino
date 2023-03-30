#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>


Adafruit_BMP280 bmp;

static const int RX = 4, TX = 3;
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;

SoftwareSerial ss(RX, TX);

void setup()
{
  Serial.begin(9600);
  ss.begin(GPSBaud);
  bmp.begin();
  LoRa.begin(433E6);

}

void loop()
{
  //block for gps and bmp280 serial print 

  
    Serial.print("Latitude: ");
    Serial.print(gps.location.lat(),6);
    Serial.println();
  
    Serial.print("Longitude: ");
    Serial.print(gps.location.lng(),6);
    Serial.println();

    Serial.print("GPS Altitude: ");
    Serial.print(gps.altitude.meters());
    Serial.println(" meter");

    Serial.print(F("Temperature = "));
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");

    Serial.print(F("Pressure = "));
    Serial.print(bmp.readPressure()/1000);
    Serial.println(" KPa");

    Serial.print(F("Appox altitude = "));
    Serial.print(bmp.readAltitude(1015.25));
    Serial.print(" m");
    Serial.println();
  
    Serial.println();

  
   
   
   //block for lora transmission of gps and bmp280 sensor data
   
    LoRa.beginPacket();
  
    LoRa.print(gps.altitude.meters(), 3);
    LoRa.print(",");
    LoRa.print(gps.location.lat(), 6);
    LoRa.print(",");
    LoRa.print(gps.location.lng(), 6);
    LoRa.print(",");
    LoRa.print(bmp.readTemperature());
    LoRa.print(",");
    LoRa.print(bmp.readPressure()/1000);
    LoRa.print(",");
    LoRa.print(bmp.readAltitude(1015.25));
    LoRa.println("");
    
    LoRa.endPacket();


  
    smartDelay(1000);

}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (ss.available())
      gps.encode(ss.read());
  } while (millis() - start < ms);
}

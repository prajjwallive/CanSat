#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <MPU6050_light.h>


Adafruit_BMP280 bmp;

MPU6050 mpu(Wire);
long timer = 0;

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
  
  Wire.begin();
  mpu.begin();
  delay(1000);
  mpu.calcOffsets(true,true);

}

void loop()
{
  //block for gps, bmp280 and mpu serial print 
    mpu.update();
    if(millis() - timer > 1000){
    Serial.println(F("ACCELERO"));
    Serial.print(mpu.getAccX());
    Serial.print(",");
    Serial.print(mpu.getAccY());
    Serial.print(",");
    Serial.println(mpu.getAccZ());
  
    Serial.println(F("GYRO"));
    Serial.print(mpu.getGyroX());
    Serial.print(",");
    Serial.print(mpu.getGyroY());
    Serial.print(",");
    Serial.println(mpu.getGyroZ());
    timer = millis();
  }
  
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

  
   
   
   //block of code for lora transmission of gps, bmp280 and mpu sensor data
   
    LoRa.beginPacket();
  
    LoRa.print("/*");
    LoRa.print(gps.location.lat(), 6);
    LoRa.print(",");
    LoRa.print(gps.location.lng(), 6);
    LoRa.print(",");
    LoRa.print(gps.altitude.meters(), 3);
    LoRa.print(",");
    LoRa.print(bmp.readTemperature());
    LoRa.print(",");
    LoRa.print(bmp.readPressure()/1000);
    LoRa.print(",");
    LoRa.print(bmp.readAltitude(1015.25));
    LoRa.print(",");
    LoRa.print(mpu.getAccX());
    LoRa.print(",");
    LoRa.print(mpu.getAccY());
    LoRa.print(",");
    LoRa.print(mpu.getAccZ());
    LoRa.print(",");
    LoRa.print(mpu.getGyroX());
    LoRa.print(",");
    LoRa.print(mpu.getGyroY());
    LoRa.print(",");
    LoRa.print(mpu.getGyroZ());
    LoRa.println("*/");
    
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

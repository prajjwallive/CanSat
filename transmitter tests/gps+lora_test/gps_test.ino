#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <SPI.h>
#include <LoRa.h>

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;


TinyGPSPlus gps;

SoftwareSerial ss(RXPin, TXPin);

void setup()
{
  Serial.begin(9600);
  ss.begin(GPSBaud);
  LoRa.begin(433E6);

}

void loop()
{

  Serial.print("Latitude: ");
  Serial.print(gps.location.lat(),6);
  Serial.println();

  Serial.print("Longitude: ");
  Serial.print(gps.location.lng(),6);
  Serial.println();



  Serial.print("GPS Altitude: ");
  Serial.print(gps.altitude.meters());
  Serial.println(" meter");
  
  Serial.println();


  LoRa.beginPacket();

  LoRa.print(gps.altitude.meters(), 3);
  LoRa.print(",");
  LoRa.print(gps.location.lat(), 6);
  LoRa.print(",");
  LoRa.print(gps.location.lng(), 6);
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

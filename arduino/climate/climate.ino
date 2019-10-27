#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

//
// NOTE:
// This is for the D1 mini and NOT a normal Arduino
//

#include "DHTesp.h"

#include "settings.h"
 
ESP8266WiFiMulti WiFiMulti;
DHTesp dht;
char mac[20];

void setup() {

  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(WIFI_ESSID, WIFI_PASSWORD);
  WiFi.macAddress().toCharArray(mac, 20);

  Serial.println(mac);

  dht.setup(D1, DHTesp::DHT22);

}

void loop() {

  float rh = dht.getHumidity();
  float t = dht.getTemperature();

  Serial.print("\"humidity\": ");
  Serial.print(rh);
  Serial.print(", \"temp\": ");
  Serial.println(t);

  char payload[50];
  char pushgwUrl[100];
  sprintf(payload, "temp %f\nrh %f\n", t, rh);
  sprintf(pushgwUrl, "http://%s:%u/metrics/job/%s/instance/%s", PUSHGW_IP, PUSHGW_PORT, JOB, mac);

  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    Serial.println("[HTTP] begin...");
    Serial.println(pushgwUrl);
    if (http.begin(client, pushgwUrl)) {  // HTTP

      Serial.print("[HTTP] POST...\n");
      int httpCode = http.POST(payload);

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] POST... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String response = http.getString();
          Serial.println(response);
        }
      } else {
        Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP] Unable to connect\n");
    }
  }

  // TODO: hard-coded value
  delay(2000);
}

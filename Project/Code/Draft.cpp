//Initial Setup
cpp
void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);
  
  // Initialize OLED display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  
  // Initialize sensors
  dht.begin();
  
  // Initialize Bluetooth
  SerialBT.begin("NerG");
  
  // Set pin modes
  pinMode(piezoPin, INPUT);
  pinMode(capacitorPin, OUTPUT);
}


//Harvesting Energy
cpp
void harvestEnergy() {
  int piezoValue = analogRead(piezoPin);
  if (piezoValue > threshold) {
    // Simulate storing energy in the capacitor
    digitalWrite(capacitorPin, HIGH);
    delay(10);
    digitalWrite(capacitorPin, LOW);
  }
}



//Collecting Temp and Humidity Data
cpp
void collectData() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Display data for debugging
  Serial.print("Temp: ");
  Serial.print(temperature);
  Serial.print(" Humidity: ");
  Serial.println(humidity);
}



//Display 
cpp
void updateDisplay() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  
  display.print("Energy: ");
  display.print(analogRead(capacitorPin));
  display.print(" mV");
  
  display.display();
}


//Data Transmission
cpp
void transmitData() {
  if (SerialBT.available()) {
    SerialBT.print("Energy: ");
    SerialBT.print(analogRead(capacitorPin));
    SerialBT.print(" mV\n");
    
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    SerialBT.print("Temp: ");
    SerialBT.print(temperature);
    SerialBT.print(" Humidity: ");
    SerialBT.print(humidity);
    SerialBT.print("\n");
  }
}


//Main 
cpp
void loop() {
  harvestEnergy();
  collectData();
  updateDisplay();
  transmitData();
  
  delay(1000); // Delay as per need
}
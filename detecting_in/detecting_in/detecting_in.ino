const int pieces = 9;//number of pieces

//not used in this test but gives a consistent output
int red = 0;
int green = 0;
int blue = 0;

//ldr input pins
const int ldr_pins[pieces] = {32,35,34, 27,26,33, 13,12,14};

/*prints the LED output and the LDR readings in a standard format*/
void print_readings(){
  Serial.print(red);
  Serial.print(",");
  Serial.print(green);
  Serial.print(",");
  Serial.print(blue);
  Serial.print(",  ");
  
  for(int piece_number = 0; piece_number<pieces; piece_number++){
    int ldr_pin = ldr_pins[piece_number];
    float sensorValue = analogRead(ldr_pin);
    Serial.print(sensorValue);
    Serial.print(",");
  }
  Serial.println("");
}

void setup() {
  //starts serial connection
  Serial.begin(115200);

  //sets up all the LDR pins as inputs
  for(int piece_number = 0; piece_number<pieces; piece_number++){
    pinMode(ldr_pins[piece_number], INPUT);
  }
}

void loop() {
  //prints out the raw sensor values as quickly as possible
  print_readings();
}

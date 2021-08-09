/*
 * Collects data about the reflectivity of the pieces.
 * Outputs it as a calculated intensity reading
 */
const int KNOWN_RESISTANCE = 2000;//Omhs
const int INPUT_RANGE = 4095;//max analog input value

const int pieces = 9;//number of pieces
const int red_pin = 21;
const int green_pin = 22;
const int blue_pin = 23;

const int PWMFreq = 5000; /* 5 KHz */
const int PWMResolution = 10;
const int MAX_DUTY_CYCLE = (int)(pow(2, PWMResolution) - 1);

const int redPwmChannel = 0;
const int greenPwmChannel = 1;
const int bluePwmChannel = 2;

int red;
int green;
int blue;

//ldr input pins
const int ldr_pins[pieces] = {32,35,34, 27,26,33, 13,12,14};
//led control pins
const int digital_pins[pieces] = {5,18,19, 4,16,17, 15,2,0};
boolean pieces_in[pieces];//which pins are in

int iterations = 0;

/*gets the resistance of the ldr in the specified slot*/
float getLdrResistance(int piece_number){
  int ldr_pin = ldr_pins[piece_number];
  float sensorValue = analogRead(ldr_pin);
  float resistance = ((INPUT_RANGE / sensorValue) - 1) * KNOWN_RESISTANCE;
  return resistance;
}

/*gets the measured brightness in the specified slot*/
float getIntensity(int piece_number){
  float resistance = getLdrResistance(piece_number);
  float light_intensity = 1600000000 * pow(resistance, -1.75);
  //calibration coefficients aren't used as they cancel(and would just complicate the program)
  if(light_intensity < 0){
    light_intensity = 0;
  }
  return light_intensity;
}

/*updates the leds with the latest values*/
void update_leds(){
  for(int piece_number = 0; piece_number<pieces; piece_number++){
    digitalWrite(digital_pins[piece_number], pieces_in[piece_number]);
  }
  
  ledcWrite(redPwmChannel, red);
  ledcWrite(greenPwmChannel, green);
  ledcWrite(bluePwmChannel, blue);
}

/*prints the LED output and the LDR readings in a standard format*/
void print_readings(){
  Serial.print(red);
  Serial.print(",");
  Serial.print(green);
  Serial.print(",");
  Serial.print(blue);
  Serial.print(",  ");
  
  for(int piece_number = 0; piece_number<pieces; piece_number++){
    Serial.print(getIntensity(piece_number));
    Serial.print(",");
  }
  Serial.println("");
}

void setup() {
  //initialises array
  for(int piece_number = 0; piece_number<pieces; piece_number++){
    pieces_in[piece_number] = 1;
  }
  
  Serial.begin(115200);

  //sets up the LEDs
  ledcSetup(redPwmChannel, PWMFreq, PWMResolution);
  ledcSetup(greenPwmChannel, PWMFreq, PWMResolution);
  ledcSetup(bluePwmChannel, PWMFreq, PWMResolution);

  ledcAttachPin(red_pin, redPwmChannel);
  ledcAttachPin(green_pin, greenPwmChannel);
  ledcAttachPin(blue_pin, bluePwmChannel);

  for(int piece_number = 0; piece_number<pieces; piece_number++){
    pinMode(digital_pins[piece_number], OUTPUT);
    digitalWrite(digital_pins[piece_number], pieces_in[piece_number]);
  }
  
  red = 0;
  green = 0;
  blue = 0;

  update_leds();
  
  //sets up the LDRs
  for(int piece_number = 0; piece_number<pieces; piece_number++){
    pinMode(ldr_pins[piece_number], INPUT);
  }
}

void loop() {
  //sets the output colour
  red = 0;
  green = 0;
  blue = 0;
  
  if(iterations % 4 == 0){
    //all off
  }else if(iterations % 4 == 1){
    red = 1023;
  }else if(iterations % 4 == 2){
    green = 1023;
  }else if(iterations % 4 == 3){
    blue = 1023;
  }
  update_leds();
  
  delay(10000);//waits 10 seconds to eliminate the effect of hysteresis
  print_readings();//outputs the recorded value
  iterations++;//goes to the next part of the sequence
}

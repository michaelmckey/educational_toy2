/*
 * Tries to predict and remove the effect of the LED on LDR readings
 * Outputs calculation to be plotted (in order to determine accuracy)
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

float red_reflected;
float green_reflected;
float blue_reflected;

const int TEST_SLOT = 2;//3rd slot

const int sequence_speed = 8;//should be 2 to the power of something
const int length_of_sequence = 3072;

const float time_per_iteration = 4000;//microseconds
float last_time = 0;

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

  //sets up the LDRs
  for(int piece_number = 0; piece_number<pieces; piece_number++){
    pinMode(ldr_pins[piece_number], INPUT);
  }

  //keeps the LEDs off and records the brightness with no LEDs
  red = 0;
  green = 0;
  blue = 0;
  update_leds();
  
  float none_reading = getIntensity(TEST_SLOT);

  //records the light intensity when the red LED is on
  red = 1023;
  green = 0;
  blue = 0;
  update_leds();
  
  delay(1000);//waits 1 seconds to eliminate the effect of hysteresis
  float red_reading = getIntensity(TEST_SLOT);

  
  //records the light intensity when the green LED is on
  red = 0;
  green = 1023;
  blue = 0;
  update_leds();
  
  delay(1000);//waits 1 seconds to eliminate the effect of hysteresis
  float green_reading = getIntensity(TEST_SLOT);

  
  //records the light intensity when the blue LED is on
  red = 0;
  green = 0;
  blue = 1023;
  update_leds();
  
  delay(1000);//waits 1 seconds to eliminate the effect of hysteresis
  float blue_reading = getIntensity(TEST_SLOT);

  //calculates the amount of light reflected
  red_reflected = red_reading - none_reading;
  green_reflected = green_reading - none_reading;
  blue_reflected = blue_reading - none_reading;
  
  if(red_reflected < 0){
    red_reflected = 0;
  }
  if(green_reflected < 0){
    green_reflected = 0;
  }
  if(blue_reflected < 0){
    blue_reflected = 0;
  }


  //prints a header so that each line is labelled by the serial plotter
  Serial.print("measured_intensity");
  Serial.print(",");
  Serial.print("predicted_LED_effect");
  Serial.print(",");
  Serial.print("predicted_actual_intensity");
  Serial.println();
}

void loop() {
  //works out the current position in the sequence
  int part_of_sequence = (iterations % (length_of_sequence/sequence_speed)) * sequence_speed;
  
  //determines the LEDs output
  red = 0;
  green = 0;
  blue = 0;
  
  if(part_of_sequence < 1024){
    red = (part_of_sequence % 1024);
  }else if(part_of_sequence < 2048){
    green = (part_of_sequence % 1024);
  }else if(part_of_sequence < 3072){
    blue = (part_of_sequence % 1024);
  }
  update_leds();

  //gets the total intensity measured by the LDR
  float measured_intensity = getIntensity(TEST_SLOT);

  //predicts the effect of the LED on the result
  float red_led_effect = (red / 1023.0) * red_reflected;
  float green_led_effect = (green / 1023.0) * green_reflected;
  float blue_led_effect = (blue / 1023.0) * blue_reflected;
  
  float total_led_effect = red_led_effect + green_led_effect + blue_led_effect;

  //predicts the intensity if the LEDs were off
  float real_intensity = measured_intensity - total_led_effect;
  
  if(real_intensity < 0){
   real_intensity = 0;
  }

  //prints the data to plot
  Serial.print(measured_intensity);
  Serial.print(",");
  Serial.print(total_led_effect);
  Serial.print(",");
  Serial.print(real_intensity);
  Serial.println();

  //ensures time per iteration is constant by delaying remaining time
  float time_past = micros() - last_time;
  float delay_time = time_per_iteration - time_past;
  if(delay_time > 0){
    delayMicroseconds(delay_time);
  }
  last_time = micros();
  
  iterations++;//goes to the next part of the sequence
}

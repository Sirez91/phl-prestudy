const int motor1 = 2;
const int motor2 = 3;
const int motor3 = 5;
const int motor4 = 7;
const int motor5 = 9;
const int motor6 = 11;
const int motor7 = 13;

const int vibration_duration = 869;//869;

void testMotor(int motor)
{
    digitalWrite(motor, HIGH);
    digitalWrite(motor3, HIGH);
    delay(vibration_duration);
    digitalWrite(motor, LOW);
    digitalWrite(motor3, LOW);
}

void setup()
{
  Serial.begin(9600);
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);
  pinMode(motor5, OUTPUT);
  pinMode(motor6, OUTPUT);
  pinMode(motor7, OUTPUT);
  Serial.println("started");
}

int mapToMotor(int finger) {
  Serial.println(finger);
  if(finger == 1) {
    return motor1;
  } else if(finger == 2) {
    return motor2;
  } else if(finger == 3) {
    return motor3;
  } else if(finger == 4) {
    return motor4;
  } else if(finger == 5) {
    return motor5;
  } else if(finger == 6) {
    return motor6;
  } else {
    return motor7;
  }
}

void playSong(String input) {
  int ind = input.indexOf(',');  //finds location of first ,
  String fingers = input.substring(0, ind);
  String remainingFingers = fingers;
  int ind_fingers = -1;
  do {
    remainingFingers = remainingFingers.substring(ind_fingers+1);
    int motor = mapToMotor(remainingFingers.substring(0, 1).toInt());
    digitalWrite(motor, HIGH);
    ind_fingers = remainingFingers.indexOf(';');
  } while (ind_fingers>0);
  delay(vibration_duration);
  remainingFingers = fingers;
  ind_fingers = -1;
  do {
    remainingFingers = remainingFingers.substring(ind_fingers+1);
    int motor = mapToMotor(remainingFingers.substring(0, 1).toInt());
    digitalWrite(motor, LOW);
    ind_fingers = remainingFingers.indexOf(';');
  } while (ind_fingers>0);
  delay(48);
  if (ind > 0) {
    playSong(input.substring(ind+1));
  }
}

void test() {
  digitalWrite(motor1, HIGH);
  delay(vibration_duration+48);
  digitalWrite(motor1, LOW);
  digitalWrite(motor2, HIGH);
  delay(vibration_duration+48);
  digitalWrite(motor2, LOW);
  digitalWrite(motor3, HIGH);
  delay(vibration_duration+48);
  digitalWrite(motor3, LOW);
  digitalWrite(motor4, HIGH);
  delay(vibration_duration+48);
  digitalWrite(motor4, LOW);
  digitalWrite(motor5, HIGH);
  delay(vibration_duration+48);
  digitalWrite(motor5, LOW);
  digitalWrite(motor6, HIGH);
  delay(vibration_duration+48);
  digitalWrite(motor6, LOW);
  digitalWrite(motor7, HIGH);
  delay(vibration_duration+48);
  digitalWrite(motor7, LOW);
}

void loop() {
  //test();
  if(Serial.available()){
    String input = Serial.readStringUntil('\n');
    if( input == "reset"){
      // reset motors
    } else {
      playSong(input);
    }
  }
}

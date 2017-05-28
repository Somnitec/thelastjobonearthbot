int motors[] = {10, 11};

int states[] = {100, 300, 700, 1500};
int odddivision[] = {10, 50, 90};

int waitTime = 1000;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;

void setup() {
  pinMode(motors[0], OUTPUT);
  pinMode(motors[1], OUTPUT);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  inputString.reserve(200);
}

void loop() {
  if (Serial.available() > 0)  serialEvent();

  if (stringComplete) {
    Serial.println(inputString);
    // clear the string:
    inputString = "";
    stringComplete = false;
    vibrate(0, random(100));
    delay(waitTime);
    vibrate(1, random(100));
  }
}

void vibrate(int motor, int state) {
  Serial.print("odds =");
  Serial.println(state);
  if (state < odddivision[0])state = 0;
  else if (state < odddivision[1])state = 1;
  else if (state < odddivision[2])state = 2;
  else state = 3;
  Serial.print("state =");
  Serial.println(state);
  digitalWrite(motors[motor], HIGH);
  delay(states[state]);
  digitalWrite(motors[motor], LOW);
  /*
    if (state == 0) {
    digitalWrite(motors[motor],HIGH);
    delay(100
    }
    else if (state == 0) {

    }
  */
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }


}


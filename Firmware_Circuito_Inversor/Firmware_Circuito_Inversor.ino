int incomingByte = 0; // for incoming serial data
int tempo =  millis();
int estado[] = {0, 0, 0, 0, 0, 0}; // D7,D6,D5,A0,A1,A2
int n = 0;

void setup()
{
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
}

void loop()
{

  String msg = "";
  while (Serial.available() > 0)
  {
    msg += char(Serial.read());
    delay(10);

  }
  if (msg != "") {
    if (msg.length() == 8)
    {
      if (msg[4] == '1')
      {
        digitalWrite(5, HIGH);
        estado[0] = 1;
      }
      else
      {
        digitalWrite(5, LOW);
        estado[0] = 0;
      }
      if (msg[5] == '1')
      {
        digitalWrite(6, HIGH);
        estado[1] = 1;
      }
      else
      {
        digitalWrite(6, LOW);
        estado[1] = 0;
      }
      if (msg[6] == '1')
      {
        digitalWrite(7, HIGH);
        estado[2] = 1;
      }
      else
      {
        digitalWrite(7, LOW);
        estado[2] = 0;
      }
      estado[3] = analogRead(A0);
      estado[4] = analogRead(A1);
      estado[5] = analogRead(A2);
      Serial.print("$INV");
      for (int i = 0; i < 6; i++)
      {
        Serial.print(estado[i]);
        if (i >= 2 and i < 5) Serial.print(" ");
      }
      Serial.println(";");
    }
    if ( msg == "$INV;" or msg == "$INV?;" )
    {
      Serial.print("$INV");
      estado[3] = analogRead(A0);
      estado[4] = analogRead(A1);
      estado[5] = analogRead(A2);
      for (int i = 0; i < 6; i++)
      {
        Serial.print(estado[i]);
        if (i >= 2 and i < 5) Serial.print(" ");
      }

      Serial.println(";");
    }
    //Serial.println(msg);
  }
  // say what you got:

}

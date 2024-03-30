#define Q0_PIN     8  // Pin connected to output (Q) of first flip-flop (non-standard)
#define Q1_PIN     7  // Pin connected to output (Q) of second flip-flop (non-standard)
#define Q2_PIN     2  // Pin connected to output (Q) of third flip-flop (non-standard)

void setup() {
  // Set digital pins for outputs as outputs
  pinMode(Q0_PIN, OUTPUT);
  pinMode(Q1_PIN, OUTPUT);
  pinMode(Q2_PIN, OUTPUT);
}

void loop() {
  int i = 0;
  while(i<8)
  {
  	delay(1000);
    if(i==0)
    {
     	digitalWrite(Q0_PIN,LOW);
      digitalWrite(Q1_PIN,LOW);
      digitalWrite(Q2_PIN,LOW);
    }
    if(i==1)
    {
      digitalWrite(Q0_PIN,LOW);
      digitalWrite(Q1_PIN,LOW);
      digitalWrite(Q2_PIN,HIGH);
    }
    if(i==2)
    {
      digitalWrite(Q0_PIN,LOW);
      digitalWrite(Q1_PIN,HIGH);
      digitalWrite(Q2_PIN,LOW);
    }
    if(i==3)
    {
      digitalWrite(Q0_PIN,LOW);
      digitalWrite(Q1_PIN,HIGH);
      digitalWrite(Q2_PIN,HIGH);
    }
    if(i==4)
    {
      digitalWrite(Q0_PIN,HIGH);
      digitalWrite(Q1_PIN,LOW);
      digitalWrite(Q2_PIN,LOW);
    }
    if(i==5)
    {
      digitalWrite(Q0_PIN,HIGH);
      digitalWrite(Q1_PIN,LOW);
      digitalWrite(Q2_PIN,HIGH);
    }
    if(i==6)
    {
      digitalWrite(Q0_PIN,HIGH);
      digitalWrite(Q1_PIN,HIGH);
      digitalWrite(Q2_PIN,LOW);
    }
    if(i==7)
    {
      digitalWrite(Q0_PIN,HIGH);
      digitalWrite(Q1_PIN,HIGH);
      digitalWrite(Q2_PIN,HIGH);
    }
    i++;
  }
  
}

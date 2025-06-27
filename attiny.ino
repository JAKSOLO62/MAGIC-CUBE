#include <avr/sleep.h>

#define LED_PIN 0
#define WAKEUP_PIN 3
#define WAKEUP_INT_MASK PCINT3
#define WAKEUP_PIN2 1
#define WAKEUP_INT_MASK2 PCINT1
#define ESP_ENABLE_PIN 4
#define ESP_SIGNAL_PIN 2
#define TIMEOUT 30000L

ISR (PCINT0_vect) {}

bool timed_out;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(WAKEUP_PIN, INPUT_PULLUP);
  pinMode(WAKEUP_PIN2, INPUT_PULLUP);
  pinMode(ESP_ENABLE_PIN, OUTPUT);
  digitalWrite(ESP_ENABLE_PIN, LOW);
  pinMode(ESP_SIGNAL_PIN, INPUT);
  ADCSRA &= ~(1<<ADEN); 
  GIMSK |= (1<<PCIE); 
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  timed_out = false;
}

void loop() {
  if (!timed_out) {
    PCMSK |= 1<<WAKEUP_INT_MASK; 
  }
  timed_out = false;
  PCMSK |= 1<<WAKEUP_INT_MASK2; 

  digitalWrite(LED_PIN, LOW);
 
  sleep_mode();
 
  digitalWrite(LED_PIN, HIGH);

  PCMSK &= ~(1<<WAKEUP_INT_MASK | 1<<WAKEUP_INT_MASK2); 

  digitalWrite(ESP_ENABLE_PIN, HIGH);

  long start_time = millis();

  delay(2000); 

  while (!digitalRead(ESP_SIGNAL_PIN)) {
    if (millis() - start_time > TIMEOUT) {
      timed_out = true;
      for (int i = 0; i < 10; i++) {
        digitalWrite(LED_PIN, LOW);
        delay(100);
        digitalWrite(LED_PIN, HIGH);
        delay(100);
      }
      break;
    }
  }

  digitalWrite(ESP_ENABLE_PIN, LOW);
}

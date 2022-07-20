/*
--- Write to screen ---
charging current *
battery voltage *
outside temp *
humidity *
inside temp *
bilge water level* 
battery load

--- Alarms ---
bilge
security
*/

#include <LiquidCrystal.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#include <DHT.h>


const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2; // LCD screen variables
const int current_sensor = A0;  //ACS712 Current sensor analog input pin
const int screenButtonPin = 6;
const int alarmPin = 7;
const int bilge_alarm = 8;
const int one_wire_bus = 9;
const int DHTPIN = 10; // Temperature and humidity sensor
const int voltagePin = A1;
const int echoPin = 20; // Echo pin of HC-SR04
const int trigPin = 13; // Trigger pin of HC-SR04
const int relay1 = 21;
const int relay2 = 22;
#define DHTTYPE DHT21   // AM2301 


boolean currentState = LOW;
boolean lastState    = LOW;
boolean stateChange  = false;

int currentButton = 0;
int lastButton    = 5;    
unsigned long interval;

float humidity;
float inside_temperature;

int bilge_water_level;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
OneWire oneWire(one_wire_bus); 
DallasTemperature sensors(&oneWire);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(9600);
    sensors.begin();
    dht.begin();
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
    pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
    pinMode(current_sensor, INPUT);
    pinMode(screenButtonPin, INPUT);
    pinMode(alarmPin, OUTPUT);
    pinMode(bilge_alarm, INPUT);
    pinMode(relay1, OUTPUT);
    pinMode(relay2, OUTPUT);
    digitalWrite(alarmPin, LOW);
    digitalWrite(relay1, LOW);
    digitalWrite(relay2, LOW); 
    interval = 10000;

}


class ButtonClass {
    public:
    int buttonPin;

    ButtonClass(int x) {
      buttonPin = x;
    }

    // method debounceButton
    boolean debounceButton()
    {
        boolean firstCheck   = LOW;
        boolean secondCheck  = LOW;
        boolean current = LOW;  
        firstCheck  = digitalRead(buttonPin);
        delay(50);
        secondCheck = digitalRead(buttonPin);  
        if (firstCheck == secondCheck){
            current = firstCheck;
        }
        return current;
    }

    // method checkForChange
    boolean checkForChange(boolean current, boolean last)
    {
        boolean change;  
        if (current != last)
        {
            change = true;
        }
        else 
        {
        change = false;
        }  
        return change;
    }

    // function getButtonNumber
    int getButtonNumber(int button, boolean state, boolean change)
    {
        if (change == true && state == LOW)
        {
            button++;
            if (button > 5){
            button = 0;
            }
            //Serial.println(button);
        }
        return button;
    }

    // method write to LCD screen
    void write_to_screen(int button)
    {   
        // for (int i=0; i<5; i++) {
        //    digitalWrite(ledArray[i], LOW);
        // }
        
        typedef float (*FloatFunctionWithNoParameter) ();
        FloatFunctionWithNoParameter functions[] = 
        {
            get_charging_current,
            get_battery_voltage, 
            get_water_temperature,
            get_inside_temperature,
            get_humidity_temperature,
            get_bilge_water_level,

        };
        float write_to_lcd = functions[button]();
    }
};

void loop() {
    unsigned long startMillis = millis(); 
    ButtonClass displayButton(screenButtonPin);
    currentState = displayButton.debounceButton();
    stateChange = displayButton.checkForChange(currentState, lastState);
    currentButton = displayButton.getButtonNumber(lastButton, currentState, stateChange);
    displayButton.write_to_screen(currentButton);
    lastState  = currentState;
    lastButton = currentButton;
    check_bilge();
    if(startMillis >= interval)
    {
        send_mode();
        interval = interval + 10000;

    }
}

void send_mode()
{
    lcd.begin(16, 2);
    lcd.print("Send mode");
    float charging_current = get_charging_current();
    float battery_voltage = get_battery_voltage();
    float water_temperature = get_water_temperature();
    float inside_temperature = get_inside_temperature();
    float humidity_temperature = get_humidity_temperature();
    int bilge_water_level = get_bilge_water_level();
    Serial.print(charging_current);
    Serial.print(";");
    Serial.print(battery_voltage);
    Serial.print(";");
    Serial.print(water_temperature);
    Serial.print(";");
    Serial.print(inside_temperature);
    Serial.print(";");
    Serial.print(humidity_temperature);
    Serial.print(";");
    Serial.print(bilge_water_level);
    Serial.println();
}

float get_charging_current()
{
    // calculation for ACS712 current sensor
    // https://www.youtube.com/watch?v=d6MnA4aPDag&t=499s
    float current = analogRead(current_sensor);
    float voltage = current * 5 / 1023.0;
    float charging_current = (voltage - 2.5) / 0.066;
    
    // TODO: measure lowest charging current
    // if current below 0.16 show 0 amps
    //if (current < 0.16)
    //{
    //    current = 0;
    //}
    //Serial.println(charging_current);
    
    lcd.begin(16, 2);
    lcd.print("Charg. current:");
    lcd.setCursor(0, 1);
    lcd.print(charging_current);
    // try without delay
    //delay(300);
    return charging_current;
}

float get_water_temperature()
{
    sensors.requestTemperatures();
    float water_temp = sensors.getTempCByIndex(0);
    lcd.begin(16, 2);
    lcd.print("Water temp:");
    lcd.setCursor(0, 1);
    lcd.print(water_temp);
    delay(300);
    return water_temp;
}

float get_battery_voltage()
{
    /*
    Math behind voltage calculation
    Vout = (Vs*R2)/(R1+R2)
    Vs is the source voltage, measured in volts (V),
    R1 is the resistance of the 1st resistor, measured in Ohms (Ω).
    R2 is the resistance of the 2nd resistor, measured in Ohms (Ω).
    Vout is the output voltage, measured in volts (V),
    Vs = 15V
    R1 = 50 kilohm
    R2 = 10 kilohm
    Vout = 2.5V
    https://ohmslawcalculator.com/voltage-divider-calculator
    */
    float val; 
    float step;
    float battery_voltage;
    float ratio = 6.0; // 15V/2.5V 
    val = analogRead(voltagePin);  // read the voltage input pin
    float pin_voltage = val * 0.00488;
    step = 2.5/775;
    val = val*step;
    battery_voltage = pin_voltage * ratio;
    lcd.begin(16, 2);
    lcd.print("Bat. voltage:");
    lcd.setCursor(0, 1);
    lcd.print(battery_voltage);
    delay(300);
    return battery_voltage;
}

float get_inside_temperature()
{
    humidity = dht.readHumidity();
    float inside_temp = dht.readTemperature();
    lcd.begin(16, 2);
    lcd.print("Inside temp:");
    lcd.setCursor(0, 1);
    lcd.print(inside_temp);
    delay(300);
    return inside_temp;
}

float get_humidity_temperature()
{
    humidity = dht.readHumidity();
    lcd.begin(16, 2);
    lcd.print("Inside humidity:");
    lcd.setCursor(0, 1);
    lcd.print(humidity);
    delay(300);
    return humidity;
}


void check_bilge()
{
    int water_level = digitalRead(bilge_alarm);
    if (water_level == 1) 
    {
        digitalWrite(alarmPin, HIGH); 
        digitalWrite(relay1, HIGH);
    }
    else
    {
        digitalWrite(alarmPin, LOW);
        digitalWrite(relay1, LOW);
    }
}

int get_bilge_water_level()
{
    // defines variables
    long duration; // variable for the duration of sound wave travel
    int distance; // variable for the distance measurement
    // Clears the trigPin condition
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance, return cm
    distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back) 
    lcd.begin(16, 2);
    lcd.print("Bilge level:");
    lcd.setCursor(0, 1);
    lcd.print(distance);
    delay(300);
    return distance;
}

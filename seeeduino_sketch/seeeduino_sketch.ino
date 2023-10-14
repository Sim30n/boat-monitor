
#define voltagePin A0

void setup() {
    Serial.begin(9600);
}

void loop() {
    float battery_voltage = get_battery_voltage();
    Serial.println(battery_voltage);
    delay(100);
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
    https://www.instructables.com/DIY-Amp-Hour-Meter-Arduino/
    */

    float val; 
    float step;
    float battery_voltage;
    float ratio = 6.0; // 15V/2.5V 
    val = analogRead(voltagePin);  // read the voltage input pin
    float pin_voltage = val * 0.00322;
    step = 2.5/775;
    val = val*step;
    battery_voltage = pin_voltage * ratio;
    return battery_voltage;
}
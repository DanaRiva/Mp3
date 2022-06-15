#include <Arduino_FreeRTOS.h>
#include "queue.h"

//macros para la configuración y manejo de pines
#define MakeInputPin(REG, PIN)       (REG &= (~(1 << PIN)))
#define MakeOutputPin(REG, PIN)      (REG |= (1 << PIN))
#define EnablePullUp(REG, PIN)       (REG |= (1 << PIN))
#define ReadInputPin(REG, PIN)       (REG & (1 << PIN))
#define WriteOutputPinLow(REG, PIN)  (REG &= ~(1 << PIN))
#define WriteOutputPinHigh(REG, PIN) (REG |= (1 << PIN))
#define ToggleOutputPin(REG, PIN)    (REG ^= (1 << PIN))

//declaraciones de la tasa de comunicación serial
#define F_CPU 16000000UL
#define USART_BAUDRATE 19200
#define UBRR_VALUE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

//retardo en ms
const unsigned int period = 25;

//buffer para el UART
unsigned char mybuffer[25];

//handle para un queue
QueueHandle_t glob;

void setup()
{
  xTaskCreate(button_read, "lee el boton", 100, NULL, 1, NULL);
  xTaskCreate(clasificacion, "clasifica los datos", 100, NULL, 1, NULL);

  //configuración del puerto serial
  UBRR0H = (uint8_t)(UBRR_VALUE >> 8);
  UBRR0L = (uint8_t)UBRR_VALUE;
  UCSR0C = 0x06;       // Set frame format: 8data, 1stop bit
  UCSR0B |= (1 << RXEN0) | (1 << TXEN0);   // TX y RX habilitados

  //creación de la queue
  glob = xQueueCreate(6, sizeof(int32_t));

  // Renglones en alta impedancia
  MakeInputPin(DDRB, PB3); WriteOutputPinHigh(PORTB, PB3);
  MakeInputPin(DDRB, PB2); WriteOutputPinHigh(PORTB, PB2);
  MakeInputPin(DDRB, PB1); WriteOutputPinHigh(PORTB, PB1);
  MakeInputPin(DDRB, PB0); WriteOutputPinHigh(PORTB, PB0);

  // Columnas en pullup
  MakeInputPin(DDRD, PD7); EnablePullUp(PORTD, PD7);
  MakeInputPin(DDRD, PD6); EnablePullUp(PORTD, PD6);
  MakeInputPin(DDRD, PD5); EnablePullUp(PORTD, PD5);
  MakeInputPin(DDRD, PD4); EnablePullUp(PORTD, PD4);
}

void clasificacion(void * pvParameters)
{
  char value;
  BaseType_t qStatus;
  const TickType_t xTicksToWait = pdMS_TO_TICKS(100);
  while (1)
  {
    qStatus = xQueueReceive(glob, &value, xTicksToWait);
    if(qStatus == pdPASS){
      if (value != 'A' && value != 'B' && value != 'C' && value != 'D' && value != '#')
      {
        while (value != '*' && value!='n') {
          qStatus = xQueueReceive(glob, &value, xTicksToWait);
          if(qStatus == pdPASS){
            if (value != '*'){
              sprintf(mybuffer, "%c", value);
              USART_Transmit_String((unsigned char *)mybuffer);
            }else{
              sprintf(mybuffer, "\n");
              USART_Transmit_String((unsigned char *)mybuffer);
            }
          }
        }
      }else{
        sprintf(mybuffer, "%c\n", value);
        USART_Transmit_String((unsigned char *)mybuffer);
      }
    }
    vTaskDelay(pdMS_TO_TICKS(250));
  }
}

char button_read(void * pvParameters)
{
  char key = 'n';
  BaseType_t qStatus;
  const TickType_t xTicksToWait = pdMS_TO_TICKS(100);
  while (1)
  {
    key = readKeypad();
    if (key!='n'){xQueueSend(glob, &key, xTicksToWait);}
    _delay_ms(period);
  }
}

char readKeypad()
{
  // Barrido de renglones
  //renglón 1
  MakeOutputPin(DDRB, PB3);
  WriteOutputPinLow(PORTB, PB3);
  _delay_ms(period);
  if(ReadInputPin(PIND, PD7) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD7) == 0);
    return '1';
  }
  if(ReadInputPin(PIND, PD6) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD6) == 0);
    return '2';
  }
  if(ReadInputPin(PIND, PD5) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD5) == 0);
    return '3';
  }
  if(ReadInputPin(PIND, PD4) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD4) == 0);
    return 'A';
  }
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB3);
  MakeInputPin(DDRB, PB3);
  //renglón 2
  MakeOutputPin(DDRB, PB2);
  WriteOutputPinLow(PORTB, PB2);
  _delay_ms(period);
  if(ReadInputPin(PIND, PD7) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD7) == 0);
    return '4';
  }
  if(ReadInputPin(PIND, PD6) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD6) == 0);
    return '5';
  }
  if(ReadInputPin(PIND, PD5) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD5) == 0);
    return '6';
  }
  if(ReadInputPin(PIND, PD4) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD4) == 0);
    return 'B';
  }
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB2);
  MakeInputPin(DDRB, PB2);
  //renglón 3
  MakeOutputPin(DDRB, PB1);
  WriteOutputPinLow(PORTB, PB1);
  _delay_ms(period);
  if(ReadInputPin(PIND, PD7) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD7) == 0);
    return '7';
  }
  if(ReadInputPin(PIND, PD6) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD6) == 0);
    return '8';
  }
  if(ReadInputPin(PIND, PD5) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD5) == 0);
    return '9';
  }
  if(ReadInputPin(PIND, PD4) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD4) == 0);
    return 'C';
  }
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB1);
  MakeInputPin(DDRB, PB1);
  //renglón 4
  MakeOutputPin(DDRB, PB0);
  WriteOutputPinLow(PORTB, PB0);
  _delay_ms(period);
  if(ReadInputPin(PIND, PD7) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD7) == 0);
    return '*';
  }
  if(ReadInputPin(PIND, PD6) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD6) == 0);
    return '0';
  }
  if(ReadInputPin(PIND, PD5) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD5) == 0);
    return '#';
  }
  if(ReadInputPin(PIND, PD4) == 0)
  {
    _delay_ms(period);
    while(ReadInputPin(PIND, PD4) == 0);
    return 'D';
  }
  // Regresa el renglón a alta impedancia
  WriteOutputPinHigh(PORTB, PB0);
  MakeInputPin(DDRB, PB0);
  //no se detectó tecla
  return 'n';
}

//////////funciones de transmisión del UART///////////////

void USART_Transmit(unsigned char data)
{
  //wait for empty transmit buffer
  while (!(UCSR0A & (1 << UDRE0)));

  //put data into buffer, send data
  UDR0 = data;
}

void USART_Transmit_String(unsigned char * pdata)
{
  unsigned char i;
  //calculate string length
  unsigned char len = strlen(pdata);

  //transmit byte for byte
  for (i = 0; i < len; i++)
  {
    //wait for empty transmit buffer
    while (!(UCSR0A & (1 << UDRE0)));
    //put data into buffer, send data
    UDR0 = pdata[i];
  }
}
//////////////////////////////////////////////////////////////

void loop(){}

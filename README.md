# rele-reled.py
rele

<img width="396" height="225" alt="imagen" src="https://github.com/user-attachments/assets/34022c3b-0b43-4bd2-b659-f5e60394b027" />

![WhatsApp Image 2026-04-13 at 9 05 59 AM](https://github.com/user-attachments/assets/e246bc4a-a62f-4c69-9e76-cdc2626ed49b)

USANDO PUERTO SERIAL SOLO ESTA ACTIVO EL PIN 13

El Problema de Fondo: SoftwareSerial y HardwareSerial

Tu código actual probablemente usa SoftwareSerial para comunicarse con el ESP8266. El problema es que esta librería tiene limitaciones importantes en el Arduino Mega :

    Solo funciona en pines específicos: En el Mega, SoftwareSerial solo puede recibir datos en un grupo muy limitado de pines. El pin 13 está en esa lista, pero la mayoría de los otros (como el 44 o 46 que mencionaste) no lo están .

    Es lento y consume recursos: SoftwareSerial emula la comunicación serie por software, lo que ralentiza tu programa y puede causar errores, especialmente si usas la velocidad de 115200 baudios que suelen usar estos módulos .

✅ La Solución Definitiva: Usar los Puertos Serie Hardware del Mega

El Arduino Mega 2560 tiene una ventaja enorme sobre la mayoría de las placas: posee 4 puertos serie de hardware (UARTs) . Usarlos es la solución ideal porque son mucho más rápidos, fiables y no interfieren con la carga de tus sketches.

Para ello, debes usar los pines dedicados:

    Serial1: Usa los pines 19 (RX) y 18 (TX).

    Serial2: Usa los pines 17 (RX) y 16 (TX).

    Serial3: Usa los pines 15 (RX) y 14 (TX) .

¿Cómo implementarlo?

    Conecta el ESP8266 a uno de estos puertos. Por ejemplo, si eliges Serial1:

        TX del ESP8266 -> Pin 19 (RX) del Mega.

        RX del ESP8266 -> Pin 18 (TX) del Mega.

    Modifica tu código. Es muy sencillo. Debes cambiar la línea donde creas tu objeto SoftwareSerial por una línea que inicialice el puerto hardware correspondiente.

    Así lo tienes probablemente (SoftwareSerial):
    cpp

    #include <SoftwareSerial.h>
    SoftwareSerial EspSerial(13, 12); // RX, TX

    Así debería ser (HardwareSerial):
    cpp

    // ¡No necesitas incluir la librería SoftwareSerial!

    // Usa Serial1, Serial2 o Serial3 según las conexiones que hayas hecho.
    #define EspSerial Serial1

    Luego, en el setup(), solo tienes que iniciar el puerto con la velocidad adecuada (ej. 115200):
    cpp

    void setup() {
      Serial.begin(9600); // Para el monitor serie (USB)
      EspSerial.begin(115200); // Para comunicarte con el ESP8266

      // ... el resto de tu configuración
    }

⚠️ Punto de Atención: Voltaje (5V vs 3.3V)

El Arduino Mega funciona a 5V, mientras que el ESP8266 (especialmente el modelo ESP-01) funciona a 3.3V en sus pines de datos . Aunque a veces funcione, conectar directamente el pin TX del Mega (5V) al pin RX del ESP8266 (3.3V) puede dañar el módulo WiFi a largo plazo .

Para una conexión segura, debes reducir el voltaje en esa línea. Un divisor de voltaje con dos resistencias (por ejemplo, una de 1kΩ y otra de 2kΩ) es la solución más simple y económica .

Esquema de conexión corregido y seguro:
Pin del ESP8266	Conéctalo a...	Consideración importante
VCC	3.3V del Mega	Asegura una fuente de corriente estable.
GND	GND del Mega	Conectar tierras.
CH_PD (EN)	3.3V del Mega	Habilita el módulo.
TX	Pin RX del Mega (ej. 19)	Conexión directa (3.3V -> 5V es seguro).
RX	Pin TX del Mega (ej. 18)	Usa un divisor de voltaje (5V -> 3.3V).
📝 Resumen de Acción para Solucionarlo

    Deja de usar SoftwareSerial. Es la fuente principal de tus problemas .

    Conecta el ESP8266 a los pines de Serial1, Serial2 o Serial3 de tu Arduino Mega .

    Modifica tu código para usar Serial1 (o el que hayas elegido) en lugar de SoftwareSerial.

    Protege tu ESP8266 añadiendo un divisor de tensión en la línea TX del Mega .

Siguiendo estos pasos, podrás usar casi cualquier pin para otros sensores o actuadores, y tu conexión WiFi será mucho más estable y rápida. Si te surge alguna duda al modificar el código, compártelo y lo vemos


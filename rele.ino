const int RELAY_PIN = 13;
String comando = "";

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  Serial.begin(9600);
  
  // Mensaje de inicio - importante para verificar comunicación
  Serial.println("INICIO: Arduino listo");
  Serial.println("Comandos: RELAY_ON, RELAY_OFF, STATUS");
}

void loop() {
  // Leer comandos
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      procesarComando(comando);
      comando = "";
    } else if (c != '\r') {
      comando += c;
    }
  }
}

void procesarComando(String cmd) {
  cmd.trim();
  cmd.toUpperCase();
  
  // Enviar confirmación de recepción
  Serial.print("COMANDO_RECIBIDO: ");
  Serial.println(cmd);
  
  if (cmd == "RELAY_ON") {
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("RESPUESTA: RELAY_ON");
    Serial.println("RELE_ACTIVADO");
  }
  else if (cmd == "RELAY_OFF") {
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("RESPUESTA: RELAY_OFF");
    Serial.println("RELE_DESACTIVADO");
  }
  else if (cmd == "STATUS") {
    if (digitalRead(RELAY_PIN) == HIGH) {
      Serial.println("STATUS: ACTIVADO");
    } else {
      Serial.println("STATUS: DESACTIVADO");
    }
  }
  else if (cmd != "") {
    Serial.println("ERROR: Comando desconocido");
  }
}

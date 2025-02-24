#include "serial_processor.h"
#include "motor_control.h"
#include <stdlib.h>
#include <string.h>


int receivedData[MAX_VALUES] = {0};
int velocidade = 0;
int angulacao = 0;
int pessoa = 0;
int semaforo = 0;

void setupSerialProcessor() {
    Serial.begin(115200);      
    pinMode(LED_PIN, OUTPUT);     
}

void processData(char *data) {
    char *token = strtok(data, ",");
    int count = 0;

    while (token != NULL && count < MAX_VALUES) {
        receivedData[count] = atoi(token);
        token = strtok(NULL, ",");
        count++;
    }

    // Se houver ao menos 4 valores, atualiza as variáveis correspondentes
    if (count >= 4) {
        velocidade = receivedData[0];
        angulacao = receivedData[1];
        pessoa = receivedData[2];
        semaforo = receivedData[3];
    }

    if (pessoa == 1) {
        digitalWrite(LED_PIN, HIGH); 
        brakeMotors(); 
    } else {
        digitalWrite(LED_PIN, LOW);   
        setMotorSpeed(velocidade, velocidade);
    }
}

// Função para atualizar os dados recebidos via Serial
void updateSerialInput() {
    static char inputBuffer[BUFFER_SIZE];
    static byte index = 0;
    
    
    while (Serial.available()) {
        char receivedChar = Serial.read();
        
        if (receivedChar == '#') {  // Delimitador de fim de mensagem
            inputBuffer[index] = '\0';  // Finaliza a string
            processData(inputBuffer);   // Processa os dados recebidos
            index = 0;                  // Reseta o índice para a próxima mensagem
        } 
        else if (index < BUFFER_SIZE - 1) {
            inputBuffer[index++] = receivedChar;
        }
    }
}

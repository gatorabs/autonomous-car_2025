#define BUFFER_SIZE 32   // Tamanho máximo do buffer de entrada
#define MAX_VALUES 10    // Número máximo de valores esperados
#define LED_PIN 13       

int receivedData[MAX_VALUES] = {0};


int velocidade = 0;
int angulacao = 0;
int pessoa = 0;
int semaforo = 0;

void setup() {
    Serial.begin(115200);  
    pinMode(LED_PIN, OUTPUT);  
}

void loop() {
    static char inputBuffer[BUFFER_SIZE];
    static byte index = 0;
    
    while (Serial.available()) {
        char receivedChar = Serial.read();
        
        if (receivedChar == '#') {  // Final da mensagem
            inputBuffer[index] = '\0';  // Termina a string
            processData(inputBuffer);   // Processa os dados recebidos
            index = 0;  // Reseta o índice para a próxima leitura
        } 
        else if (index < BUFFER_SIZE - 1) {
            inputBuffer[index++] = receivedChar;
        }
    }
}

void processData(char *data) {
    char *token = strtok(data, ",");
    int count = 0;

    while (token != NULL && count < MAX_VALUES) {
        receivedData[count] = atoi(token);
        token = strtok(NULL, ",");
        count++;
    }

    
    if (count >= 4) {
        velocidade = receivedData[0];
        angulacao = receivedData[1];
        pessoa = receivedData[2];
        semaforo = receivedData[3];
    }



    // Controle do LED interno com base no valor de "pessoa"
    if (pessoa == 1) {
        digitalWrite(LED_PIN, HIGH);  // Acende o LED
    } else if (pessoa == 0) {
        digitalWrite(LED_PIN, LOW);   // Apaga o LED
    }
}

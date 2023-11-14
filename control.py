import machine
import utime

class UARTReceiver:
    def __init__(self, uart_num, baud_rate, tx_pin, rx_pin):
        self.uart = machine.UART(uart_num, baud_rate, tx=tx_pin, rx=rx_pin)

    def start_receiving(self):
        while True:
            if self.uart.any():
                received_data = self.uart.readline()
                if received_data:
                    decoded_data = received_data.decode('utf-8').strip()
                    print("Received:", decoded_data)
                    # Aquí puedes agregar la lógica para procesar los datos recibidos
            utime.sleep(0.1)  # Puedes ajustar este valor según tus necesidades

def main():
    # Configuración del puerto UART
    uart_num = 0  # Número del puerto UART que estás utilizando
    baud_rate = 9600  # Velocidad de baudios
    tx_pin = machine.Pin(0)  # Reemplaza el número del pin con el que estás utilizando para TX
    rx_pin = machine.Pin(1)  # Reemplaza el número del pin con el que estás utilizando para RX

    uart_receiver = UARTReceiver(uart_num, baud_rate, tx_pin, rx_pin)
    uart_receiver.start_receiving()

if __name__ == "__main__":
    main()

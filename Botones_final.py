import RPi.GPIO as GPIO
import time

# Definir los pines de los semáforos
#Semaforo 1
rojo_pin = 2
amarillo_pin = 3
verde_pin = 4

#Semaforo 2
rojo_pin = 14
amarillo_pin = 15
verde_pin = 18

#Semaforo 3
rojo_pin = 17
amarillo_pin = 27
verde_pin = 22

#Semaforo 4
rojo_pin = 23
amarillo_pin = 24
verde_pin = 25

# Definir los pines de los botones
boton_norte_pin = 12
boton_sur_pin = 16
boton_este_pin = 20
boton_oeste_pin = 21

# Variable global para contar los automóviles
# contador_automoviles = 0
contador_autos_norte = 0
contador_autos_sur = 0
contador_autos_este = 0
contador_autos_oeste = 0

# Configurar los pines de los semáforos y los botones
GPIO.setmode(GPIO.BCM)
GPIO.setup(rojo_pin, GPIO.OUT)
GPIO.setup(amarillo_pin, GPIO.OUT)
GPIO.setup(verde_pin, GPIO.OUT)
GPIO.setup(boton_norte_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_sur_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_este_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_oeste_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Función para cambiar el color del semáforo
def cambiar_semaforo(color):
    GPIO.output(rojo_pin, GPIO.LOW)
    GPIO.output(amarillo_pin, GPIO.LOW)
    GPIO.output(verde_pin, GPIO.LOW)

    if color == 'rojo':
        GPIO.output(rojo_pin, GPIO.HIGH)
    elif color == 'amarillo':
        GPIO.output(amarillo_pin, GPIO.HIGH)
    elif color == 'verde':
        GPIO.output(verde_pin, GPIO.HIGH)

# Función para contar los automóviles y cambiar el semáforo
def contar_automoviles(pin):
    global contador_automoviles

    # Aumentar el contador de automóviles
    contador_automoviles += 1

    # Calcular el lado con más automóviles
    lado = ''
    if contador_automoviles % 2 == 0:
        lado = 'este/oeste'
    else:
        lado = 'norte/sur'

    # Cambiar el color del semáforo según el lado con más automóviles
    if lado == 'este/oeste':
        cambiar_semaforo('verde')
    else:
        cambiar_semaforo('rojo')

    print("Contador de automóviles:", contador_automoviles)
    print("Lado con más automóviles:", lado)

# Configurar las interrupciones para los botones
GPIO.add_event_detect(boton_norte_pin, GPIO.FALLING, callback=contar_automoviles_norte, bouncetime=3000)
GPIO.add_event_detect(boton_sur_pin, GPIO.FALLING, callback=contar_automoviles_sur, bouncetime=3000)
GPIO.add_event_detect(boton_este_pin, GPIO.FALLING, callback=contar_automoviles_este, bouncetime=3000)
GPIO.add_event_detect(boton_oeste_pin, GPIO.FALLING, callback=contar_automoviles_oeste, bouncetime=3000)

try:
    while True:
        # Realizar otras tareas aquí si es necesario
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

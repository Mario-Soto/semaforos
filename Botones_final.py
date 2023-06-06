import RPi.GPIO as GPIO
import time

direcciones = ['norte', 'sur', 'este', 'oeste']
sentidos = {
    0: ['norte', 'sur'],
    1: ['este', 'oeste']
}

# Definir los pines de los semáforos
semaforos_pin = {
    'norte': {
        'rojo': 2,
        'amarillo': 3,
        'verde': 4
    },
    'sur': {
        'rojo': 17,
        'amarillo': 27,
        'verde': 22
    },
    'este': {
        'rojo': 14,
        'amarillo': 15,
        'verde': 18
    },
    'oeste': {
        'rojo': 23,
        'amarillo': 24,
        'verde': 25
    }
}

semaforos_color = {
    0: 'rojo',
    1: 'verde',
}

# Definir los pines de los botones
botones_pin = {
    'norte': 12,
    'sur': 16,
    'este': 20,
    'oeste': 21
}

# Variable global para contar los automóviles
# contador_automoviles = 0
contador_autos = {
    'norte': 0,
    'sur': 0,
    'este': 0,
    'oeste': 0
}

# Configurar los pines de los semáforos y los botones
GPIO.setmode(GPIO.BCM)
for direccion in direcciones:
    for color in semaforos_pin[direccion]:
        GPIO.setup(semaforos_pin[direccion][color], GPIO.OUT)
    GPIO.setup(botones_pin[direccion], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Función para cambiar el color del semáforo
def cambiar_semaforo(sentido, color):
    if color == 'amarillo':
        semaforos_color[sentido] = color
        return
    
    # Cambiar el color del semáforo
    color_contrario = 'rojo' if color == 'verde' else 'verde'
    sentido_contrario = 0 if sentido == 1 else 1
    semaforos_color[sentido] = color
    semaforos_color[sentido_contrario] = color_contrario

    actualizar_semaforos()

def actualizar_semaforos():
    # Apagar todos los semáforos
    for direccion in semaforos_pin:
        for color in semaforos_pin[direccion]:
            GPIO.output(semaforos_pin[direccion][color], GPIO.LOW)
    
    # Encender los semáforos según el color
    for sentido in semaforos_color:
        color = semaforos_color[sentido]
        direcciones_seleccionadas = sentidos[sentido]

        for direccion in direcciones_seleccionadas:
            for color_seleccionado in semaforos_pin[direccion]:
                if color_seleccionado == color:
                    GPIO.output(semaforos_pin[direccion][color], GPIO.HIGH)

# Función para contar los automóviles y cambiar el semáforo
def contar_automoviles(direccion):
    contador_autos[direccion] += 1
    print('Contador de autos en {}: {}'.format(direccion, contador_autos[direccion]))

def semaforo_verde():
    for sentido in semaforos_color:
        color = semaforos_color[sentido]
        if color == 'verde':
            return sentido
    return None

# Configurar las interrupciones para los botones
for direccion in direcciones:
    GPIO.add_event_detect(botones_pin[direccion], GPIO.FALLING, callback=contar_automoviles(direccion), bouncetime=3000)

def avanzar_autos():
    sentido_verde = semaforo_verde()
    if sentido_verde is None:
        return
    
    for direccion in sentidos[sentido_verde]:
        if contador_autos[direccion] > 0:
            contador_autos[direccion] -= 1
            print('Contador de autos en {}: {}'.format(direccion, contador_autos[direccion]))

cambio_semaforo = False

def cambiar_semaforo_cantidad_autos():
    semaforo_activo = semaforo_verde()
    if semaforo_activo is None:
        return
    global cambio_semaforo
    max_autos_activo = max(contador_autos[direccion] for direccion in sentidos[semaforo_activo])
    semaforo_inactivo = 0 if semaforo_activo == 1 else 1
    max_autos_inactivo = max(contador_autos[direccion] for direccion in sentidos[semaforo_inactivo])

    diferencia_autos = max_autos_activo - max_autos_inactivo

    if diferencia_autos >= 0:
        return
    elif max_autos_activo == 0:
        cambio_semaforo = True
    elif diferencia_autos >= -2:
        cambio_semaforo = False
    else:
        cambio_semaforo = True

def continuar_proceso():
    avanzar_autos()
    cambiar_semaforo_cantidad_autos()

def proceso_cambiar_semaforo(sentido_verde):
    cambiar_semaforo(sentido_verde, 'amarillo')
    time.sleep(1)
    cambiar_semaforo(sentido_verde, 'rojo')

# Ciclo principal
try:
    veces = 0
    while True:
        # Realizar otras tareas aquí si es necesario
        time.sleep(1)
        continuar_proceso()
        sentido_verde = semaforo_verde()
        if cambio_semaforo:
            proceso_cambiar_semaforo(sentido_verde)
            veces = 0
            continue
        veces += 1
        if veces == 5 and sentido_verde is not None:
            proceso_cambiar_semaforo(sentido_verde)
            veces = 0
except KeyboardInterrupt:
    GPIO.cleanup()

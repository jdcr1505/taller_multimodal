# 1.1

**Imagen:** 01_circuito_led.JPG

**Pregunta:** Observa la imagen e identifica los componentes electrónicos presentes. Explica cuál es la función de cada uno y cómo interactúan para encender el LED.

**Respuesta (qwen/qwen3.8-27b):**

## Componentes electrónicos presentes

Al observar la imagen (y sus ampliaciones) se distinguen **cinco elementos** que forman un circuito básico de encendido de un LED:

| # | Componente | Aspecto en la imagen |
|---|-----------|----------------------|
| 1 | **Pila de 9 V** | Batería rectangular negra/verde con el símbolo **“+”** y las leyendas *“WARNING: Install correctly (+/−). Do not charge”* y *“Made in USA”*. |
| 2 | **LED (diodo emisor de luz)** | Componente blanco translúcido con forma de gota y **dos patas metálicas** (una más larga = ánodo, una más corta = cátodo). Está **encendido**. |
| 3 | **Resistor** | Pequeño cilindro beige con **bandas de colores** (código de valor) y dos patas dobladas en “L” para insertarse en la protoboard. |
| 4 | **Cables de conexión** | Un cable **rojo** y uno **negro** con los extremos pelados (cobre al descubierto) que se clavan en los orificios de la protoboard. |
| 5 | **Protoboard (placa de prototipado)** | Base gris con rejilla de agujeros sobre una suela azul; permite armar el circuito **sin soldar**. |

---

## Función de cada componente

1. **Pila de 9 V (fuente de alimentación):** Almacena energía química y la convierte en una **diferencia de potencial (voltaje) de 9 V** entre sus terminales positivo (+) y negativo (−). Es el “motor” que empuja los electrones por el circuito.

2. **LED (carga / indicador luminoso):** Es un **diodo semiconductor** que solo conduce en un sentido (de ánodo a cátodo). Cuando por él circula corriente en el sentido correcto, los electrones recombinan con huecos en la unión y liberan energía en forma de **fotones → luz visible** (en este caso, luz blanca).

3. **Resistor (limitador de corriente):** Su función es **reducir la intensidad de corriente** que llega al LED a un valor seguro (típicamente 10–20 mA). Sin él, los 9 V de la pila harían circular una corriente excesiva que **quemaría el LED en milisegundos**. Su valor se lee por las bandas de color (ley de Ohm: R = (V_fuente − V_LED) / I_LED).

4. **Cables rojo y negro (conductores):** Son “caminos” de baja resistencia que **transportan la corriente** entre la pila, el resistor y el LED. Por convención, el rojo va al polo positivo y el negro al negativo.

5. **Protoboard (medio de interconexión):** Sus pistas internas (en forma de “U” bajo cada fila de agujeros) **unen eléctricamente** los terminales que se insertan en el mismo grupo, permitiendo armar y desarmar el circuito sin soldadura.

---

## Cómo interactúan para encender el LED (flujo del circuito)

El circuito es una **malla en serie** que parte y termina en la pila:

1. El **polo positivo (+)** de la pila de 9 V se conecta por el **cable rojo** a un punto de la protoboard.
2. Desde ese punto, la corriente pasa por el **resistor**, que “frena” la intensidad hasta el valor adecuado para el LED.
3. La corriente sale del resistor y entra por el **ánodo** (pata más larga) del **LED**.
4. Atraviesa la unión del diodo (donde se genera la luz) y sale por el **cátodo** (pata más corta).
5. Desde el cátodo, el **cable negro** devuelve la corriente al **polo negativo (−)** de la pila, **cerrando el circuito**.

Al estar el lazo cerrado y con la polaridad correcta (ánodo a +, cátodo a −), fluye una corriente limitada por el resistor y el LED **emite luz**, tal como se ve encendido en la imagen. Si se invirtiera la polaridad del LED o se quitara el resistor, el LED no encendería o se dañaría, respectivamente.

> **En resumen:** la pila *provee* el voltaje, el resistor *protege* limitando la corriente, el LED *convierte* esa corriente en luz, los cables *conducen* la corriente y la protoboard *une* todo sin soldar. Juntos forman el circuito en serie mínimo para encender un LED de forma segura.

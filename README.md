# Super Mario Bros 2D - Motor Completo de Plataformas en Python (Pygame-CE)

Un motor de videojuego de plataformas en 2D modular y de producción, inspirado en el clásico **Super Mario Bros (World 1-1)**, programado con físicas reales de sub-píxel, colisiones AABB separadas por ejes, cinemática de victoria y audio retro 8-bit sintetizado proceduralmente.

---

## 🕹️ Controles del Juego

| Acción | Teclas Primarias | Teclas Alternativas |
|---|---|---|
| **Mover a la izquierda / derecha** | `A` / `D` | `Flecha Izquierda` / `Flecha Derecha` |
| **Salto Variable** | `Espacio` | `W` / `Flecha Arriba` |
| **Correr (Sprint) / Disparar** | `Shift Izquierdo` | — |
| **Agacharse** | `S` | `Flecha Abajo` |
| **Pausa** | `ESC` | `P` |
| **Reintentar / Reiniciar** | `R` / `Enter` | — |
| **Alternar Super Mario (Debug)** | `B` | — |

---

## ⚙️ Características y Mecánicas Implementadas

1. **Físicas y Player Controller:**
   * **Inercia y Fricción:** Aceleración progresiva con derrape (`SKID_FRICTION`) al cambiar de sentido en carrera.
   * **Salto Variable:** Cuanto más tiempo sostengas la tecla de salto, más alto salta Mario. Al soltar la tecla, corta el ascenso para control milimétrico.
   * **Resolución de Colisiones AABB:** Detección y resolución separada en ejes X e Y para evitar bugs de atravesar paredes.
   * **Cámara Unidireccional NES:** Avance horizontal suave hacia adelante que no permite retroceder más allá del margen izquierdo.

2. **Bloques e Interacciones:**
   * **Bloques Misteriosos `[?]`:** Al golpearlos desde abajo, rebotan verticalmente, expulsan monedas saltarinas o champiñones y se transforman en bloques usados.
   * **Ladrillos Destructibles:** Rebotan si Mario es pequeño; estallan en 4 fragmentos con físicas de gravedad si Mario está en modo Super.
   * **Monedas Flotantes:** Monedas animadas girando en el aire recolectables por contacto.

3. **Sistema de Enemigos (Goomba y Koopa Troopa):**
   * **IA de Patrulla:** Movimiento horizontal autónomo con rebote contra tuberías, muros y fosos.
   * **Mecánica de Stomp:** Salto sobre la cabeza de Goombas para aplastarlos (+100 pts con rebote hacia arriba para Mario).
   * **Koopa Shell:** Pisotón repliega a Koopa en su caparazón; al patearlo sale disparado a 380 px/s rebotando en paredes y eliminando a cualquier enemigo a su paso.
   * **Daño e Invulnerabilidad:** Pérdida de estado Super o reducción de vidas con 2.5 segundos de inmunidad y parpadeo visual (i-frames).

4. **Power-Ups y Proyectiles:**
   * **Champiñón Rojo:** Emerge verticalmente de bloques `[?]` y recorre el suelo hacia la derecha. Al recogerlo, Mario crece a 48 px de altura con animación de crecimiento.
   * **Bolas de Fuego:** Al presionar `Shift Izquierdo` en estado Super Mario, lanza proyectiles que rebotan parabólicamente contra el suelo y eliminan enemigos a distancia.

5. **Meta, Cinemática y HUD:**
   * **Asta de Bandera (Flagpole):** Al tocar el mástil, se bloquea el control, Mario y la bandera descienden al compás, Mario salta a la derecha y camina automáticamente hacia el interior del Castillo.
   * **Temporizador:** Cuenta atrás de 400 segundos; al completarse el nivel, el tiempo remanente se suma como bonificación de puntuación.
   * **HUD Completo:** Puntuación (`MARIO`), Contador de Monedas (`COINS`), Mundo (`WORLD 1-1`), Temporizador (`TIME`) y Contador de Vidas (`LIVES`).
   * **Audio 8-Bit Procedural:** Sintetizador de ondas en memoria (sin archivos externos) para saltos, monedas, pisotones, rotura de ladrillos, bolas de fuego y fanfarria de victoria.

---

## 🚀 Requisitos e Instalación

1. Asegúrate de tener Python 3.10 o superior (o el lanzador `py` en Windows).
2. Instala las dependencias:
   ```bash
   py -m pip install -r requirements.txt
   ```
3. Ejecuta el juego:
   ```bash
   py main.py
   ```

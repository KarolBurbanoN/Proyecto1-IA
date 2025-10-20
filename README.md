# Proyecto1-IA

**Fecha:** 18/10/2025

**Curso:** Inteligencia Artificial

---

## 👥 Integrantes del Grupo
| Nombre Completo                 | Código  | Rol          | Correo Electrónico                                |
|---------------------------------|---------|-------------|--------------------------------------------------|
| Verónica Lorena Mujica Gavidia  | 2359406 | Colaboradora | veronica.mujica@correounivalle.edu.co          |
| Jeidy Nicol Murillo Murillo     | 2359310 | Colaboradora | jeidy.murillo@correounivalle.edu.co            |
| Karol Tatiana Burbano Nasner    | 2359305 | Colaboradora | karol.burbano@correounivalle.edu               |
| Sebastian Castro Rengifo        | 2359435 | Colaborador  | sebastian.castro.rengifo@correounivalle.edu.co |

---

## 📌 Descripción del Taller

Primer proyecto del curso de Inteligencia Artificial enfocado en la **búsqueda de caminos en entornos discretos**, utilizando algoritmos como **Beam Search** y **Dynamic Weighted A*** para que una hormiga encuentre un hongo evitando obstáculos.

Se busca desarrollar:

- Simulación de entornos con obstáculos (venenos) y objetivos (hongos).  
- Implementación de heurísticas para optimizar la búsqueda de caminos.  
- Visualización interactiva mediante **interfaz gráfica en Python** con `CustomTkinter`.  
- Animación de la hormiga recorriendo el camino hasta el objetivo.

---

## 🎯 Objetivos

### General
- Implementar y comparar algoritmos de búsqueda informada para resolver un problema de búsqueda de caminos en un entorno controlado.

### Específicos
- Diseñar un ambiente simulado con posiciones iniciales y metas.  
- Implementar **Beam Search** y **Dynamic Weighted A*** con heurísticas apropiadas.  
- Desarrollar una interfaz gráfica que permita visualizar el entorno y la animación de la solución.  
- Analizar y comparar el desempeño de los algoritmos en distintos escenarios.

---

## 🛠 Herramientas y Tecnologías

- **Python**  
- **CustomTkinter** para interfaz gráfica  
- **PIL / Pillow** para manejo de imágenes  
- Librerías estándar de Python: `heapq`, `random`, `time`  

---

## 🔍 Algoritmos Implementados

1. **Beam Search**  
   - Búsqueda heurística limitada por un ancho de haz (`beam width`).  
   - Explora los nodos más prometedores según la heurística Manhattan.

2. **Dynamic Weighted A***  
   - Variante de A* con peso dinámico ajustable (`epsilon`) que equilibra costo y heurística.  
   - Permite encontrar caminos más eficientes en entornos con obstáculos.

---


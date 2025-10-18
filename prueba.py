"""
from ambiente import Ambiente
from busquedas import beam_search

amb = Ambiente(filas=8, columnas=8, num_venenos=8)
amb.mostrar()

camino = beam_search(amb.matriz, amb.pos_hormiga, amb.pos_hongo, beta=3)

if camino:
    print("Camino encontrado:")
    print(camino)
else:
    print("No se encontró camino 😢")
"""

from ambiente import Ambiente
from busquedas import dynamic_weighted_a_star

amb = Ambiente(filas=8, columnas=8, num_venenos=10)
amb.mostrar()

camino = dynamic_weighted_a_star(amb.matriz, amb.pos_hormiga, amb.pos_hongo, epsilon=2.0)

if camino:
    print("Camino encontrado (Dynamic Weighted A*):")
    print(camino)
else:
    print("No se encontró camino 😢")


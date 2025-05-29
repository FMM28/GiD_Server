from gid import Gid
from modelo import Obj
from time import time

inicio = time()

gid = Gid()
obj = Obj()

obj.leerModelo("banca.obj")

for i,cara in enumerate(obj.caras):
    gid.crearPoligono(obj.coordenasCara(i))
    
fin = time() - inicio
    
print("Tiempo:",fin)
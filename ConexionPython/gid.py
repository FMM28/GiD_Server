from conexion import ejecutar_gid

class Gid():
    def __init__(self):
        self.puntos = []
        self.lineas = []
        self.superficies = []
        
    def findPunto(self,punto:tuple):
        return self.puntos.index(punto) if punto in self.puntos else -1
    
    def findLinea(self,linea:tuple):
        return self.lineas.index(linea) if linea in self.lineas else -1
    
    def findSuperfice(self,superficie:tuple):
        return self.superficies.index(superficie) if superficie in self.superficies else -1
    
    def crearLinea(self,punto1:tuple,punto2:tuple):
        if punto1 == punto2:
            return print("No puedes crear una linea si ambos puntos son el mismo")
        
        if(self.findLinea((punto1,punto2)) != -1):
            return print("Esta linea ya existe - Punto 1:",punto1,"Punto 2:",punto2)
        
        self.lineas.append((punto1,punto2))
        
        instruccion = "Mescape%20Geometry%20Create%20Line%20"+str(punto1[0])+","+str(punto1[1])+","+str(punto1[2])+"%20"
        
        if(self.findPunto(punto1) == -1):
            self.puntos.append(punto1)
        else:
            instruccion+="old%20"
            
        instruccion+=str(punto2[0])+","+str(punto2[1])+","+str(punto2[2])+"%20"
            
        if(self.findPunto(punto2) == -1):
            self.puntos.append(punto2)
        else:
            instruccion+="old%20"
        
        instruccion+="escape%20escape"
        
        ejecutar_gid(instruccion)
        
        return self.findLinea((punto1,punto2))
        
    def crearSuperficie(self, contorno: tuple):
        if self.findSuperfice(contorno) != -1:
            print(f"Esta superficie ya existe: {contorno}")
            return

        for linea in contorno:
            if self.findLinea(linea) == -1:
                print(f"Línea no existe: {linea}")
                return
        
        ctn = []
        
        for punto1,punto2 in contorno:
            ctn.extend([punto1,punto2])
        
        ctn_tmp = []
        
        for punto in ctn:
            ctn_tmp.remove(punto) if punto in ctn_tmp else ctn_tmp.append(punto)
            
        if len(ctn_tmp)!=0:
            print("El contorno no es continuo",contorno)

        comandos = []
        for linea in contorno:
            idx_linea = self.findLinea(linea) + 1
            comandos.append(str(idx_linea))
        
        instruccion = "Mescape%20Geometry%20Create%20NurbsSurface%20" + "%20".join(comandos) + "%20escape%20escape"
        
        self.superficies.append(contorno)
        ejecutar_gid(instruccion)       
        
    def crearPoligono(self,puntos:list):
        if len(puntos) < 3:
            print("Error: Un polígono necesita al menos 3 puntos")
            return

        if puntos[0] != puntos[-1]:
            puntos = puntos + [puntos[0]]
        
        contorno = []
        
        for i in range(len(puntos)-1):
            p1 = puntos[i]
            p2 = puntos[i+1]
            
            linea_normal = (p1, p2)
            linea_inversa = (p2, p1)
            
            if self.findLinea(linea_normal) == -1 and self.findLinea(linea_inversa) == -1:
                self.crearLinea(p1, p2)
                contorno.append(linea_normal)
            else:
                if self.findLinea(linea_normal) != -1:
                    contorno.append(linea_normal)
                else:
                    contorno.append(linea_inversa)
        self.crearSuperficie(tuple(contorno))
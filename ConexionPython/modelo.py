class Obj():
    def __init__(self):
        self.vertices = []
        self.caras = []
        
    def leerModelo(self,ruta:str):
        try:
            with open(ruta, 'r') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    
                    if not linea or linea.startswith('#'):
                        continue
                        
                    partes = linea.split()
                    tipo = partes[0]
                    
                    if tipo == 'v':
                        vertice = tuple(map(float, partes[1:4]))
                        self.vertices.append(vertice)
                        
                    elif tipo == 'f':
                        cara = []
                        for parte in partes[1:]:
                            vert_id = parte.split('/')[0]
                            try:
                                indice_vert = int(vert_id) - 1
                                cara.append(indice_vert)
                            except (ValueError, IndexError):
                                continue
                        
                        if len(cara) >= 3:
                            self.caras.append(tuple(cara))
                            
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta}")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    
    def coordenasCara(self,cara_idx:int):
        cara = self.caras[cara_idx]
        vertice = [self.vertices[i] for i in cara]
        return vertice
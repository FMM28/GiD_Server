import requests

def ejecutar_gid(instruccion:str):
    instruccion.replace(" ","%20")
    instruccion = "http://localhost:8888/gid_process/"+instruccion
    try:
        response = requests.get(instruccion)
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")
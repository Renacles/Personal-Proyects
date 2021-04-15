# This is a simple program that decrypts the Cesar encription algorithm through brute force.

from random import *

def Cesar(texto, llave):
    tEncriptado = ""
    for letra in texto:
        if letra.isupper():
            asc = ord(letra)
            asc = ((asc + llave - 65) % 26) + 65
            tEncriptado = tEncriptado + chr(asc)
        elif letra.islower():
            asc = ord(letra)
            asc = ((asc + llave - 97) % 26) + 97
            tEncriptado = tEncriptado + chr(asc)
        else:
            tEncriptado = tEncriptado + letra
    return tEncriptado

def GenerarLlave():
    llave = randint(1,26)
    return llave

def Main():
    nombreArch = input("Ingresar el nombre del archivo: ")
    direccion = "C:\\Users\\ramir\Documents\Programacion\Cripto\Cesar\Textos\\" + nombreArch +".txt"
    archTexto = open(direccion, "r")
    texto = archTexto.read()
    archTexto.close()
    llave = GenerarLlave()
    print(llave)
    tEncriptado = Cesar(texto, llave)
    nombreEncriptado = "C:\\Users\\ramir\Documents\Programacion\Cripto\Cesar\Textos\\" + nombreArch + "(encriptado).txt"
    archEncriptado = open(nombreEncriptado, "w")
    archEncriptado.write(tEncriptado)
    archEncriptado.close()

Main()



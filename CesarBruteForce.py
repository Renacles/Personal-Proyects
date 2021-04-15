def DesencriptarCesar(texto):
    tDesencriptado= ""
    for llave in range(1,26):
        tDesencriptado = tDesencriptado + "\n" + "Intento numero:" + str(llave) + "\n"
        for letra in texto:
            if letra.isupper():
                asc = ord(letra)
                asc = ((asc + llave - 65) % 26) + 65
                tDesencriptado = tDesencriptado + chr(asc)
            elif letra.islower():
                asc = ord(letra)
                asc = ((asc + llave - 97) % 26) + 97
                tDesencriptado = tDesencriptado + chr(asc)
            else:
                tDesencriptado = tDesencriptado + letra
        tDesencriptado = tDesencriptado + "\n"
    return tDesencriptado

def Main():
    nombreArch = input("Ingresar el nombre del archivo: ")
    direccion = "C:\\Users\\ramir\Documents\Programacion\Cripto\Cesar\Textos\\" + nombreArch +".txt"
    archTexto = open(direccion, "r")
    texto = archTexto.read()
    archTexto.close()
    tDesencriptado = DesencriptarCesar(texto)
    nombreDesencriptado = "C:\\Users\\ramir\Documents\Programacion\Cripto\Cesar\Textos\\" + nombreArch + "(desencriptado).txt"
    archDesencriptado = open(nombreDesencriptado, "w")
    archDesencriptado.write(tDesencriptado)
    archDesencriptado.close()

Main()
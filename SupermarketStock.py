import pickle
from datetime import date

def AgregarProducto(clave, descripcion, tipoProducto, precio):
    #Agrega un producto al diccionario, no agrega ningun articulo, por lo tanto el stock es 0.
    try:
        with open("Productos","rb") as Productos:
            dicProductos = pickle.load(Productos)
    except FileNotFoundError:
        dicProductos = {}
    except EOFError:
        dicProductos = {}
    if clave in dicProductos:
        print("El producto ya existe.")
    else:
        dicDatosP = {"descripcion": descripcion,
                     "tipo": tipoProducto,
                     "precio": precio,
                     "stock": 0
                     }
        dicProductos[clave] = dicDatosP
        print(f"El producto {clave} fue agregado.")
    with open("Productos","wb") as Productos:
        pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    return 0

def ExisteProducto(clave):
    try:
        with open("Productos", "rb") as Productos:
            dicProductos = pickle.load(Productos)
            existe = False
            for key in dicProductos:
                if key == clave:
                    existe = True
        with open("Productos","wb") as Productos:
            pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    except FileNotFoundError:
        existe = False
    except EOFError:
        existe = False
    return existe

def AgregarArticulo(tipo, vencimiento):
    #Agrega un articulo unico al diccionario
    if ExisteProducto(tipo):
        try:
            with open("Articulos", "rb") as Articulos:
                dicArticulos = pickle.load(Articulos)
                if bool(dicArticulos):
                    clave = list(dicArticulos)[-1] + 1
                else:
                    clave = 1
        except FileNotFoundError:
            dicArticulos = {}
            clave = 1
        except EOFError:
            dicArticulos = {}
            clave = 1
        Articulo = {"tipo":tipo,
                    "vencimiento":vencimiento,
                    #aaaa-mm-dd
                    "vendido":False
                    }
        dicArticulos[clave] = Articulo
        print(f"El articulo {clave} ha sido agregado.")
        with open("Articulos", "wb") as Articulos:
            pickle.dump(dicArticulos, Articulos, pickle.HIGHEST_PROTOCOL)
        ActualizarStockIndividual(tipo, 1)
    else:
        print("El producto no existe.")

def EliminarProducto(clave):
    #Antes de eliminar el producto elimina cualquier articulo que sea de ese tipo
    if ExisteProducto(clave):
        with open("Articulos","rb") as Articulos:
            dicArticulos = pickle.load(Articulos)
        for key in list(dicArticulos.keys()):
            if dicArticulos[key]["tipo"] == clave:
                dicArticulos.pop(key)
        with open("Articulos","wb") as Articulos:
            pickle.dump(dicArticulos, Articulos, pickle.HIGHEST_PROTOCOL)
        with open("Productos","rb") as Productos:
            dicProductos = pickle.load(Productos)
        dicProductos.pop(clave)
        with open("Productos", "wb") as Productos:
            pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    else:
        print("El producto no existe.")

def AgregarLote(tipo, vencimiento, cantidad):
    #Agrega un numero dado de articulos identicos con la misma fecha de vencimiento
    #Utilizado para rellenar el stock del supermercado
    if ExisteProducto(tipo):
        with open("Articulos", "rb") as Articulos:
            dicArticulos = pickle.load(Articulos)
            if bool(dicArticulos):
                clave = list(dicArticulos)[-1] + 1
            else:
                clave = 1
        for i in range(0, cantidad):
            Articulo = {"tipo": tipo,
                        "vencimiento": vencimiento,
                        "vendido": False
                        }
            dicArticulos[clave + i] = Articulo
        with open("Articulos", "wb") as Articulos:
            pickle.dump(dicArticulos, Articulos, pickle.HIGHEST_PROTOCOL)
        ActualizarStockIndividual(tipo, cantidad)
    else:
        print("El producto no existe.")

def ActualizarStockIndividual(producto, cantidad):
    with open("Productos", "rb") as Productos:
        dicProductos = pickle.load(Productos)
    dicProductos[producto]["stock"] = dicProductos[producto]["stock"] + cantidad
    with open("Productos", "wb") as Productos:
        pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)

def MostrarProductos():
    try:
        with open("Productos", "rb") as Productos:
            dicProductos = pickle.load(Productos)
        print("-  Producto  | Categoria | Precio     | Stock   | Descripcion")
        for key in dicProductos:
            print("- ", key, " "*(8-len(str(key))),
                  "|", dicProductos[key]["tipo"]," "*(8-len(dicProductos[key]["tipo"])),
                  "| $", dicProductos[key]["precio"], " "*(7-len(str(dicProductos[key]["precio"]))),
                  "|", dicProductos[key]["stock"], " "*(6-len(str(dicProductos[key]["stock"]))),
                  "|", dicProductos[key]["descripcion"])
        with open("Productos", "wb") as Productos:
            pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    except FileNotFoundError:
        print("No existen productos.")

def CambiarPrecio(producto, porcentaje):
    if ExisteProducto(producto):
        with open("Productos", "rb") as Productos:
            dicProductos = pickle.load(Productos)
        nuevoPrecio = round(dicProductos[producto]["precio"] * (1+porcentaje/100), 2)
        dicProductos[producto]["precio"] = nuevoPrecio
        print(f"El precio de {producto} fue cambiado, ahora es {nuevoPrecio}")
        with open("Productos", "wb") as Productos:
            pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    else:
        print("No existe el producto.")

def InterfazVenta():
    loop = 1
    productos = []
    cantidades = []
    precio = 0
    while loop == 1:
        yaSolicitado = False
        producto = int(input("Ingrese el codigo de producto a vender: "))
        cantidad = int(input("Ingrese la cantidad: "))
        yaSolicitado = False
        for i in range(len(productos)):
            if producto == productos[i]:
                yaSolicitado = True
                posicion = i
        if yaSolicitado:
            if HayStock(producto, cantidad + cantidades[posicion]):
                cantidades[posicion] += cantidad
            else:
                print("No alcanza el Stock.")
        else:
            if ExisteProducto(producto):
                if HayStock(producto, cantidad):
                    productos.append(producto)
                    cantidades.append(cantidad)
                else:
                    print("No alcanza el Stock.")
            else:
                print("No existe el producto.")
        loop = int(input("Ingrese 1 para agregar mas productos o 0 para continuar:"))
    lenproductos = len(productos)
    for i in range(0, lenproductos):
        precio += RealizarVenta(productos[i], cantidades[i])
        precio = round(precio, 2)
        ActualizarStockIndividual(productos[i], - cantidades[i])
    print(f"\nTotal: ${precio}")
    RevisarStock()
    correcto = 0
    while correcto == 0:
        delivery = input("Desea solicitar un delivery?: ")
        if delivery == "si" or delivery == "no":
            correcto = 1
        else:
            print("Valor incorrecto, por favor intente denuevo.")
    if delivery == "si":
        precioDelivery = SolicitarDelivery(productos, cantidades)
    else:
        precioDelivery = 0
    Pagar(precio, precioDelivery, productos, cantidades)

def SolicitarDelivery(productos, cantidades):
    try:
        with open("Delivery","rb") as Delivery:
            deliveries = pickle.load(Delivery)
            codigoDelivery = list(deliveries)[-1] + 1
    except FileNotFoundError:
        deliveries = {}
        codigoDelivery = 1
    nombreCliente = input("Ingresar el nombre del cliente: ")
    horaDeEnvio = -1
    while horaDeEnvio < 0 or horaDeEnvio > 24:
        horaDeEnvio = int(input("Ingresar la hora de envio: "))
    direccion = input("Ingrese la direccion (formato 'calle-numero-departamento'): ")
    delivery = {"Cliente": nombreCliente,
                "horario": horaDeEnvio,
                "recibido": False,
                "direccion": direccion,
                "productos": productos,
                "cantidades": cantidades
                }
    deliveries[codigoDelivery] = delivery
    with open("Delivery", "wb") as Delivery:
        pickle.dump(deliveries, Delivery, pickle.HIGHEST_PROTOCOL)
    precioDeDelivery = 20 + sum(cantidades)
    return precioDeDelivery

def Pagar(precio, precioDelivery, productos, cantidades):
    correcto = False
    try:
        with open("Transacciones","rb") as Transac:
            dicTransac = pickle.load(Transac)
            codigo = list(dicTransac)[-1] + 1
    except FileNotFoundError:
        dicTransac = {}
        codigo = 1

    if precioDelivery == 0:
        delivery = False
    else:
        delivery = True
    while not correcto:
        metodoDePago = input("Ingresar el metodo de pago (tarjeta o efectivo): ")
        if metodoDePago == "tarjeta" or metodoDePago == "efectivo":
            correcto = True
    precio = precioDelivery + precio
    transaccion = {"metodo": metodoDePago,
                   "monto": precio,
                   "fecha": Fecha(),
                   "productos": productos,
                   "cantidades": cantidades,
                   "conDelivery": delivery
                   }
    if metodoDePago == "efectivo":
        fin = False
        while fin == False:
            monto = float(input(f"Insertar el monto recibido, el monto a pagar es {precio}: "))
            if monto > precio:
                vuelto = round(monto - precio, 2)
                print(f"El vuelto es: {vuelto}, fin de la transaccion")
                fin = True
            elif monto == precio:
                print("Pagado con monto exacto, fin de la transaccion.")
                fin = True
            else:
                print("Monto insuficiente, por favor intentar denuevo.")
    if metodoDePago == "tarjeta":
        # Esto debe conectar con un sistema de procesamiento de tarjetas
        print("Pagado con tarjeta, fin de la transaccion.")
    dicTransac[codigo] = transaccion
    with open("Transacciones", "wb") as Transac:
        pickle.dump(dicTransac, Transac, pickle.HIGHEST_PROTOCOL)
    return codigo

def HayStock(producto, cantidad):
    with open("Productos", "rb") as Productos:
        dicProductos = pickle.load(Productos)
    with open("Productos", "wb") as Productos:
        pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    if cantidad > dicProductos[producto]["stock"]:
        return False
    else:
        return True

def Fecha():
    fecha = date.today()
    return fecha.year*10000 + fecha.month*100 + fecha.day

def RealizarVenta(producto, cantidad):
    error = False
    try:
        with open("Productos", "rb") as Productos:
            dicProductos = pickle.load(Productos)
    except FileNotFoundError:
        print("No existen productos para vender.")
        error = True
    try:
        with open("Articulos", "rb") as Articulos:
            dicArticulos = pickle.load(Articulos)
    except FileNotFoundError:
        print("No existe stock.")
        error = True
    cantidad2 = cantidad
    if error == False:
        valor = dicProductos[producto]["precio"]
        precio = valor * cantidad
        descuento = 0
        for articulo in dicArticulos:
            if cantidad > 0 and dicArticulos[articulo]["tipo"] == producto and not dicArticulos[articulo]["vendido"]:
                dicArticulos[articulo]["vendido"] = True
                cantidad -= 1
                if dicArticulos[articulo]["vencimiento"] - Fecha() < 7:
                    descuento +=  valor/10
        with open("Productos", "wb") as Productos:
            pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
        with open("Articulos", "wb") as Articulos:
            pickle.dump(dicArticulos, Articulos, pickle.HIGHEST_PROTOCOL)
        precio = round(precio, 2)
        descuento = round(descuento, 2)
        print(f"Producto: {producto} | Cantidad: {cantidad2} | Precio: {precio} | Descuento: {descuento} | Precio final: {precio - descuento}")
        return precio - descuento
    else:
        return 0

def EliminarVencidos():
    productosEliminados = []
    cantidades = []
    error = False
    try:
        with open("Articulos", "rb") as Articulos:
            dicArticulos = pickle.load(Articulos)
    except FileNotFoundError:
        print("No hay articulos para eliminar.")
        error = True
    if error == False:
        for articulo in dicArticulos:
            if dicArticulos[articulo]["vencimiento"] < Fecha():
                posicion = 0
                existe = False
                for producto in productosEliminados:
                    if producto == dicArticulos[articulo]["tipo"]:
                        cantidades[posicion] += 1
                        existe = True
                    posicion += 1
                    if existe == False:
                        productosEliminados.append(dicArticulos[articulo]["tipo"])
                        cantidades.append(1)
                dicArticulos.pop(articulo)
        with open("Articulos", "wb") as Articulos:
            pickle.dump(dicArticulos, Articulos, pickle.HIGHEST_PROTOCOL)
        with open("Productos", "rb") as Productos:
            dicProductos = pickle.load(Productos)
        for i in range(len(productosEliminados)):
            producto = productosEliminados[i]
            cantidad = cantidades[i]
            dicProductos[producto]["stock"] -= cantidad
        with open("Productos", "wb") as Productos:
            pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
        RevisarStock()

def RevisarStock():
    stockMinimo = 10
    with open("Productos", "rb") as Productos:
        dicProductos = pickle.load(Productos)
    try:
        with open("SolicitudesStock", "rb") as SolicitudesStock:
            listSolicitudes = pickle.load(SolicitudesStock)
            existenSolicitudes = True
    except FileNotFoundError:
        existenSolicitudes = False
    aSolicitar= []
    for key in dicProductos:
        if int(dicProductos[key]["stock"]) < stockMinimo:
            if existenSolicitudes:
                if key not in listSolicitudes:
                    aSolicitar.append(key)
            else:
                aSolicitar.append(key)
    with open("Productos", "wb") as Productos:
        pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    if existenSolicitudes:
        with open("SolicitudesStock", "wb") as SolicitudesStock:
            pickle.dump(listSolicitudes, SolicitudesStock, pickle.HIGHEST_PROTOCOL)
    if len(aSolicitar) > 0:
        SolicitarNuevoStock(aSolicitar)

def SolicitarNuevoStock(productos):
    try:
        with open("SolicitudesStock", "rb") as SolicitudesStock:
            listSolicitudes = pickle.load(SolicitudesStock)
    except FileNotFoundError:
        listSolicitudes = []
    with open("Productos", "rb") as Productos:
        dicProductos = pickle.load(Productos)
    fecha = Fecha()
    for p in productos:
        if p not in listSolicitudes:
            solicitud = p
            listSolicitudes.append(solicitud)
            print(f'Advertencia: El producto {p}, descripcion: {dicProductos[p]["descripcion"]}, tiene poco stock, se realizo la solicitud de reposicion.')
    with open("SolicitudesStock", "wb") as SolicitudesStock:
        pickle.dump(listSolicitudes, SolicitudesStock, pickle.HIGHEST_PROTOCOL)
    with open("Productos", "wb") as Productos:
        pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)

def ProductoMasVendido(tipo=""):
    try:
        with open("Transacciones","rb") as Transac:
            dicTransac = pickle.load(Transac)
        with open("Productos","rb") as Productos:
            dicProductos = pickle.load(Productos)
        ventas = {}
        if tipo == "":
            for venta in dicTransac:
                for i in range(0,len(dicTransac[venta]["productos"])):
                    if dicTransac[venta]["productos"][i] in dicProductos:
                        producto = dicTransac[venta]["productos"][i]
                        cantidad = dicTransac[venta]["cantidades"][i]
                        if producto in ventas.keys():
                            ventas[producto] = ventas[producto] + cantidad
                        else:
                            ventas[producto] = cantidad
            with open("Transacciones", "wb") as Transac:
                pickle.dump(dicTransac, Transac, pickle.HIGHEST_PROTOCOL)
            ventasMaximas = 0
            productoMasVendido = "Ninguno"
            for key in ventas:
                if ventas[key] > ventasMaximas:
                    productoMasVendido = key
                    ventasMaximas = ventas[key]
            if productoMasVendido != "Ninguno":
                print(f"El producto mas vendido es {productoMasVendido}, {dicProductos[productoMasVendido]['descripcion']}, con {ventas[productoMasVendido]} ventas.")
            else:
                print("No se vendio ningun producto.")
        else:
            for venta in dicTransac:

                for i in range(0,len(dicTransac[venta]["productos"])):
                    if dicTransac[venta]["productos"][i] in dicProductos:
                        producto = dicTransac[venta]["productos"][i]
                        cantidad = dicTransac[venta]["cantidades"][i]
                        if dicProductos[producto]["tipo"] == tipo:
                            if producto in ventas.keys():
                                ventas[producto] = ventas[producto] + cantidad
                            else:
                                ventas[producto] = cantidad
            with open("Transacciones", "wb") as Transac:
                pickle.dump(dicTransac, Transac, pickle.HIGHEST_PROTOCOL)
            ventasMaximas = 0
            productoMasVendido = "Ninguno"
            for key in ventas:
                if ventas[key] > ventasMaximas:
                    productoMasVendido = key
                    ventasMaximas = ventas[key]
            if productoMasVendido != "Ninguno":
                print(f"El producto mas vendido de tipo {tipo} es {productoMasVendido}, {dicProductos[productoMasVendido]['descripcion']}, con {ventas[productoMasVendido]} ventas.")
            else:
                print("No se vendio ningun producto de ese tipo.")
        with open("Productos", "wb") as Productos:
            pickle.dump(dicProductos, Productos, pickle.HIGHEST_PROTOCOL)
    except FileNotFoundError:
        print("No hay ventas.")

def Main():
    print("Bienvenido.")
    funcion = 1
    while funcion != 0:
        funcion = int(input("Por favor ingrese la funcion a la que quiere acceder, sus opciones son: \n 1- Agregar Producto \n 2- Eliminar Producto \n 3- Agregar Articulo (Requiere la existencia del producto)"
                        "\n 4- Agregar lote de articulos (Requiere la existencia del producto) \n 5- Mostrar informacion de productos \n 6- Cambiar precio de un producto \n 7- Realizar una venta"
                        "\n 8- Mostrar producto mas vendido \n 9- Mostrar producto mas vendido de una categoria \n En caso de querer terminar la operacion por favor ingresar 0. \n Ingrese una opcion:  "))
        if funcion == 1:
            clave = int(input("Ingrese el identificador del producto: "))
            descripcion = input("Ingrese una descripcion del producto: ")
            tipo = input("Ingrese la categoria del producto: ")
            precio = float(input("Ingrese el precio unitario del producto: "))
            AgregarProducto(clave, descripcion, tipo, precio)
        elif funcion == 2:
            clave = int(input("Ingrese el producto que desea eliminar: "))
            EliminarProducto(clave)
        elif funcion == 3:
            tipo = int(input("Ingrese a que producto pertenece: "))
            vencimiento = int(input("Ingrese la fecha de vencimiento (formato AAAAMMDD): "))
            AgregarArticulo(tipo, vencimiento)
        elif funcion == 4:
            tipo = int(input("Ingrese a que producto pertenece: "))
            vencimiento = int(input("Ingrese la fecha de vencimiento (formato AAAAMMDD): "))
            cantidad = int(input("Ingrese la cantidad de articulos a agregar: "))
            AgregarLote(tipo, vencimiento, cantidad)
        elif funcion == 5:
            MostrarProductos()
        elif funcion == 6:
            producto = int(input("Ingrese el identificador del producto: "))
            porcentaje = float(input("Ingrese el porcentaje (negativo para disminuir el precio): "))
            CambiarPrecio(producto, porcentaje)
        elif funcion == 7:
            InterfazVenta()
        elif funcion == 8:
            ProductoMasVendido()
        elif funcion == 9:
            categoria = input("Ingrese la categoria de producto: ")
            ProductoMasVendido(categoria)
        print("")
    print("Apagando...")
Main()
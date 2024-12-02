import sqlite3

# Conexión a la base de datos SQLite
conexion = sqlite3.connect('db_elerizo')
cursorDB = conexion.cursor()

# Función para verificar la existencia de una tabla y crearla si no existe
def tablaExiste(nombre_tabla, query_creacion):
    cursorDB.execute(
        '''SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=?''', (nombre_tabla,))
    if cursorDB.fetchone()[0] == 0:
        cursorDB.execute(query_creacion)
        conexion.commit()

# CREACIÓN DE TABLAS

# Tabla PRODUCTO
tablaExiste(
    'PRODUCTO',
    '''CREATE TABLE PRODUCTO(
        IDT INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMBRE TEXT NOT NULL,
        DESCRIPCION TEXT NOT NULL,
        PRECIO REAL NOT NULL
    )'''
)

# Tabla CLIENTES
tablaExiste(
    'CLIENTES',
    '''CREATE TABLE CLIENTES(
        IDC INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMBRE TEXT NOT NULL,
        TELEFONO TEXT NOT NULL,
        DIRECCION TEXT NOT NULL
    )'''
)

# Tabla PEDIDOS
tablaExiste(
    'PEDIDOS',
    '''CREATE TABLE PEDIDOS(
        IDP INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_CLIENTE INTEGER NOT NULL,
        ID_PRODUCTO INTEGER NOT NULL,
        FECHA DATE NOT NULL,
        NOTA TEXT,
        CANTIDAD INTEGER NOT NULL,
        TOTAL REAL NOT NULL,
        FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(IDC),
        FOREIGN KEY (ID_PRODUCTO) REFERENCES PRODUCTO(IDT)
    )'''
)

# Función para insertar datos en la tabla PRODUCTO
def insertarProducto(nombre, descripcion, precio):
    cursorDB.execute(
        '''INSERT INTO PRODUCTO (NOMBRE, DESCRIPCION, PRECIO)
           VALUES (?, ?, ?)''',
        (nombre, descripcion, precio)
    )
    conexion.commit()

# Función para insertar datos en la tabla CLIENTES
def insertarCliente(nombre, telefono, direccion):
    cursorDB.execute(
        '''INSERT INTO CLIENTES (NOMBRE, TELEFONO, DIRECCION)
           VALUES (?, ?, ?)''',
        (nombre, telefono, direccion)
    )
    conexion.commit()

# Función para insertar datos en la tabla PEDIDOS
def insertarPedido(id_cliente, id_producto, fecha, cantidad, nota):
    cursorDB.execute('SELECT PRECIO FROM PRODUCTO WHERE IDT = ?', (id_producto,))
    precio = cursorDB.fetchone()
    
    if precio is None:
        print("Producto no encontrado")
        return
    
    total = precio[0] * cantidad
    cursorDB.execute(
        '''INSERT INTO PEDIDOS (ID_CLIENTE, ID_PRODUCTO, FECHA, NOTA, CANTIDAD, TOTAL)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (id_cliente, id_producto, fecha, nota, cantidad, total)
    )
    conexion.commit()

# INSERCIÓN DE DATOS DE PRUEBA

# Datos de productos
productos = [
    ('Hamburguesa Sencilla', 'carne de res, jamon, queso amarillo y asadero, jitomate, cebolla asada, lechuga, tocino, aguacate, chile envinagre y aderezos', 65),
    ('Hamburguesa Hawaiana', 'carne de res, jamon, queso amarillo y asadero, jitomate, cebolla asada, lechuga, tocino, aguacate, chile envinagre, aderezos y piña', 75),
    ('Hamburguesa Doble', 'doble carne de res, doble jamon, doble queso amarillo, queso asadero, jitomate, cebolla asada, lechuga, tocino, aguacate, chile envinagre y aderezos', 85),
    ('Hamburguesa Salchicha', 'carne de res, jamon, queso amarillo y asadero, jitomate, cebolla asada, lechuga, tocino, aguacate, chile envinagre, salchicha y aderezos', 75),
    ('Hotdog', 'salchicha, tocino, jitomate, cebolla asada y cruda, chile envinagre y aderezos', 28),
    ('Hotdog Duo', 'dos hotdogs con salchicha, tocino, jitomate, cebolla asada y cruda, chile envinagre y aderezos', 55),
    ('Hotdog Trio', 'tres hotdogs con salchicha, tocino, jitomate, cebolla asada y cruda, chile envinagre y aderezos', 75),
    ('Malteada', 'leche, azucar, hielo triturado, sabor de platano, chocolate y fresa', 20),
    ('Papas a la Francesa',	'papas a la francesa con aderezos',	35)
]
for producto in productos:
    insertarProducto(*producto)

# Datos de clientes
clientes = [
    ('Bryan Alfredo Ojeda Vázquez', '4641976064', 'Atletismo 228, El Deportivo'),
    ('Josué Moisés Martínez Gutiérrez', '4641392238', 'De Los Virreyes 325, Las Estancias'),
    ('Yadira Ramírez Gutiérrez', '4641084901', 'Diego de Bengala 201, Las Estancias'),
    ('Andrea Torres Argüello', '4646542109',	'Privada Los Olivos 23, Residencial'),
    ('Linette Mar Leal',	'4641659018', 'Valle de Anahuac 209, Villas del Valle'),
    ('Juan Martín Dimas Pérez', '4641671171', 'C.4 7, Ampliación Bellavista'),
    ('Mariana Reyes Mata', '4641179416',	'Juan Escutia 413, El Durazno'),
    ('Nadia Alexa Figueroa Villegas', '4641651886', 'Jorge Maldonada 227, Villas 400'),
    ('María Luisa Aguilar Pérez', '4427424939', 'Granja San Juan S/N, Santo Domingo'),
    ('David Arevalo Negrete', '4641816310', 'Estancia de Valtierra Sur 301, Las Estancias'),
    ('Raúl Antonio Rodríguez Guerrero', '4641571462', 'De Los Deportes 503, El Deportivo'),
    ('Paulina Natalia Martínez Gutiérrez', '4646524603',	'De Los Virreyes 325, Las Estancias'),
    ('Dayan Fernanda Vallejo Hernández',	'4641065430', 'Nogal 117, El Cerrito'),
    ('Eric Tomé Rodríguez', '8712207506', 'Nootka 153, Cipreses'),
    ('Sebastián Alejandro Dimas Pérez', '4641169718', 'C.4 7, Ampliación Bellavista'),
    ('Alondra Zárate Calderón', '4641568069', 'De Los Deportes 405, El Deportivo'),
    ('María Fernanda Mosqueda Gutiérrez', '4622330863', 'Benito Juárez 167'),
    ('Perla Estefania Castro Lucero', '4642147558', 'Calle Álvaro Obregón 412, Guadalupe'),
    ('Jared Israel Martínez Gutiérrez', '4641163901', 'De Los Virreyes 325, Las Estancias'),
    ('Maria José Jimenez Rosas',	'4645662891', 'De Los Virreyes 322, Las Estancias'),
    ('Alexa Marcela Jiménez Rosas', '4647520393', 'De Los Virreyes 322, Las Estancias'),
    ('Juana María Gutiérrez Cervantes', '4646546050', 'De Los Virreyes 325, Las Estancias'),
    ('José Gerardo Martínez Rico', '4641175658',	'De Los Virreyes 325, Las Estancias'),
    ('Andreyev Mar Leal', '4641044687', 'Héroes de Cananea 408, La Obrera'),
    ('Adrián Tomé Rodríguez', '8711589025', 'Nootka 153, Cipreses'),
    ('Martín Iván Rosas Silva', '4641190277', 'Huizache 109, El Pirul'),
    ('Luz Mariana Jiménez Rosas', '4646523932', 'De Los Virreyes 322, Las Estancias'),
    ('Ma Mercedes Cervantes Ramiréz', '4646903562', 'Privada Cortazar 119, Guanajuato'),
    ('Consuelo Graciela Rico Salinas', '4641260496', 'Juaréz 1131, Nativitas'),
    ('Alma Rebeca Nateras Martínez', '4641191138', 'Hinoki 128, Cipreses'),
    ('Ramona Silva Navarrete', '4641109337',	'Monte Altaí 222, Infonavit 3'),
    ('Ma de la Luz Jesús Martínez Rico', '4646416038', 'Azteca 103, Zacamixtle'),
    ('Miriam Giselle Martínez Ramírez', '4641312113', 'Laguna Tenerife 404, Soto Inés'),
    ('Jesús Rubén Ramírez', '4641060079', 'Jasminez 221, San José'),
    ('Luis Fernando Ramírez Gómez', '4641234567', 'Calle Hidalgo 123, Zona Centro'),
    ('Ana Sofía Torres Martínez', '4649876543', 'Avenida Faja de Oro 456, El Pirul'),
    ('Carlos Eduardo Hernández López', '4642345678',	'Privada Las Flores 78, Las Reynas'),
    ('María Isabel García Rodríguez', '4648765432', 'Calle Obregón 321, Zona Centro'),
    ('Juan Pablo Pérez Sánchez', '4643456789', 'Avenida Cazadora 910, Bellavista'),
    ('Claudia Patricia Rojas Castillo', '4647654321', 'Calle Álvaro Obregón 567, San Roque'),
    ('José Antonio Morales Vargas', '4644567890', 'Calle Allende 89, Zona Centro'),
    ('Daniela Fernanda Ortiz Ruiz', '4646543210', 'Boulevard Valle de Santiago 234, La Gloria'),
    ('Miguel Ángel Martínez Herrera', '4645678901', 'Calle Francisco I. Madero 876, Guanajuato'),
    ('Laura Alejandra Fernández Castro',	'4645432109', 'Calle Miguel Hidalgo 678,  San Pedro'),
    ('Santiago Andrés Gómez Villalba', '4646789012',	'Avenida Lázaro Cárdenas 342, Nativitas'),
    ('Valeria Natalia Castro Jiménez', '4644321098',	'Calle Zaragoza 105, San Antonio'),
    ('Ricardo Manuel Torres Álvarez', '4647890123', 'Avenida Insurgentes 456, Ampliación San José'),
    ('Camila Soledad Vargas Peña', '4643210987',	'Calle Guerrero 234, El Monte'),
    ('Francisco Javier Romero Ramírez', '4648901234', 'Privada Olmos 89, Arboledas'),
    ('Gabriela Estefanía Cruz Morales', '4642109876', 'Calle Morelos 678, Santa María'),
    ('Fernando Adrián Navarro Delgado', '4649012345', 'Avenida Revolución 1234, Valle de Santiago'),
    ('Lucía Margarita Salas Díaz', '4641098765',	'Calle Benito Juárez 345, El Carmen'),
    ('Jorge Emilio López Camacho', '4640123456',	'Callejón Los Sauces 101, Villa Salamanca'),
    ('Diana Carolina Sánchez Flores', '4640987654', 'Calle Independencia 678,  Primavera'),
    ('Rodrigo Sebastián Muñoz Paredes', '4641357924', 'Callejón El Sol 98, Las Granjas'),
    ('Paola Andrea Vega Acosta',	'4642468135', 'Avenida Vergel 345, La Providencia'),
    ('Alejandro Tomás Gutiérrez Méndez',	'4643579246', 'Calle Constitución 210, Zona Centro'),
    ('Carolina Mariana Ramos Velázquez',	'4644681357', 'Callejón La Luz 678, Jardines de San Pedro'),
    ('Iván Gabriel Medina Cortés', '4645792468',	'Calle Pípila 456, Rinconada'),
    ('Mariana Alejandra Paredes Luna', '4646803579',	'Avenida Delicias 345, San Antonio'),
    ('Enrique Daniel Cárdenas Orozco', '4647914680',	'Callejón El Rosario 102, Lomas del Prado'),
    ('Victoria Elena Sandoval Fuentes', '4648025791', 'Calle Hidalgo 245, Zona Centro'),
    ('David Alfonso Chávez Ortiz', '4649136802',	'Avenida Faja de Oro 1325, Bellavista'),
    ('Sofía Milena Aguilar Pérez', '4640247913',	'Calle Insurgentes 567, San Pedro'),
    ('Jhocelyn Andrea Miranda Giron', '4641695059', 'Estancia de las Palomas 500, Villas de Las Estancias')
]
for cliente in clientes:
    insertarCliente(*cliente)

# Datos de pedidos
pedidos = [
    (1, 1, '2024-05-03', 2, 'Sin cebolla'),
    (5, 4, '2024-05-07', 1, 'Extra aderezo'),
    (8, 9, '2024-05-10', 1, 'Entregar antes de las 8'),
    (12, 6, '2024-05-12', 1, 'Sin chile'),
    (3, 7, '2024-05-15', 1, 'Con mucha cebolla'),
    (9, 2, '2024-05-18', 2, 'Agregar jalapeños'),
    (14, 3, '2024-05-20', 1, 'Sin jitomate'),
    (17, 8, '2024-05-23', 3, 'Sabor chocolate'),
    (19, 5, '2024-05-26', 1, 'Agregar queso extra'),
    (2, 2, '2024-5-28', 2, 'Sin aderezos'),
    (6, 1, '2024-06-01', 1, 'Sin tocino'),
    (23, 6, '2024-06-03', 1, 'Con doble aderezo'),
    (22, 4, '2024-06-05', 3, 'Agregar aguacate extra'),
    (15, 3, '2024-06-07', 1, 'Sin jitomate'),
    (16, 8, '2024-06-10', 1, 'Sabor fresa'),
    (4, 1, '2024-06-12', 2, 'Sin aderezos'),
    (29, 7, '2024-06-14', 1, 'Con tocino extra'),
    (30, 2, '2024-06-17', 1, 'Sin chile'),
    (18, 5, '2024-06-19', 1, 'Agregar salsa especial'),
    (10, 6, '2024-06-21', 2, 'Con jalapeños extras'),
    (7, 3, '2024-06-25', 1, 'Sin aguacate'),
    (25, 9, '2024-06-27', 2, 'Extra aderezo'),
    (11, 1, '2024-07-01', 3, 'Sin jitomate'),
    (20, 4, '2024-07-01', 2, 'Agregar tocino extra'),
    (31, 8, '2024-07-05', 1, 'Sabor plátano'),
    (32, 7, '2024-07-07', 1, 'Sin salsa'),
    (24, 2, '2024-07-10', 2, 'Con queso extra'),
    (26, 6, '2024-07-12', 3, 'Sin chile'),
    (5, 5, '2024-07-14', 1, 'Agregar aderezo especial'),
    (9, 1, '2024-07-16', 1, 'Sin cebolla'),
    (8, 3, '2024-07-18', 1, 'Con aguacate extra'),
    (2, 7, '2024-07-20', 2, 'Extra tocino'),
    (21, 4, '2024-07-22', 3, 'Sin jitomate'),
    (16, 2, '2024-07-24', 1, 'Agregar aderezo picante'),
    (3, 9, '2024-07-26', 1, 'Con salsa especial'),
    (4, 5, '2024-07-28', 2, 'Agregar tocino'),
    (18, 6, '2024-08-01', 2, 'Sin chile'),
    (19, 8, '2024-08-03', 1, 'Sabor chocolate'),
    (12, 3, '2024-08-05', 3, 'Sin jitomate'),
    (14, 1, '2024-08-08', 1, 'Sin aderezo'),
    (15, 7, '2024-08-10', 1, 'Sin salsa'),
    (13, 2, '2024-08-12', 3, 'Agregar jalapeños'),
    (17, 4, '2024-08-14', 2, 'Sin cebolla'),
    (10, 5, '2024-08-16', 1, 'Extra aderezo'),
    (11, 6, '2024-08-18', 2, 'Con tocino extra'),
    (22, 8, '2024-08-20', 2, 'Sabor fresa'),
    (23, 9, '2024-08-22', 1, 'Sin aderezo'),
    (28, 1, '2024-08-24', 1, 'Agregar queso extra'),
    (30, 3, '2024-08-26', 2, 'Sin chile'),
    (32, 4, '2024-08-28', 1, 'Sin jitomate'),
    (24, 7, '2024-09-01', 2, 'Sin salsa'),
    (26, 5, '2024-09-03', 3, 'Agregar aderezo picante'),
    (25, 2, '2024-09-05', 2, 'Con queso extra'),
    (7, 9, '2024-09-07', 1, 'Agregar tocino'),
    (8, 8, '2024-09-10', 1, 'Sabor plátano'),
    (10, 3, '2024-09-12', 1, 'Sin aguacate'),
    (11, 1, '2024-09-14', 1, 'Sin cebolla'),
    (17, 6, '2024-09-16', 1, 'Con jalapeños extras'),
    (20, 4, '2024-09-18', 2, 'Sin jitomate'),
    (22, 7, '2024-09-20', 1, 'Con salsa especial'),
    (2, 5, '2024-09-22', 1, 'Sin cebolla'),
    (4, 1, '2024-09-24', 2, 'Sin jitomate'),
    (6, 3, '2024-09-26', 1, 'Con doble queso'),
    (7, 4, '2024-09-28', 3, 'Extra aguacate'),
    (9, 7, '2024-10-01', 1, 'Sin aderezo'),
    (10, 2, '2024-10-03', 2, 'Con tocino extra'),
    (12, 6, '2024-10-05', 1, 'Sin chile'),
    (14, 8, '2024-10-07', 2, 'Sabor chocolate'),
    (15, 9, '2024-10-09', 1, 'Extra aderezo'),
    (18, 5, '2024-10-11', 1, 'Con salsa especial'),
    (22, 1, '2024-10-13', 3, 'Sin aguacate'),
    (25, 7, '2024-10-15', 1, 'Agregar jalapeños'),
    (26, 2, '2024-10-17', 2, 'Sin jitomate'),
    (28, 3, '2024-10-19', 1, 'Con cebolla extra'),
    (31, 4, '2024-11-21', 1, 'Agregar tocino extra'),
    (34, 6, '2024-10-23', 3, 'Sin aderezo'),
    (35, 8, '2024-10-25', 1, 'Sabor fresa'),
    (1, 5, '2024-10-27', 1, 'Sin chile'),
    (3, 9, '2024-10-29', 2, 'Extra aderezo'),
    (5, 7, '2024-10-31', 1, 'Sin jitomate'),
    (8, 3, '2024-09-23', 1, 'Con doble aguacate'),
    (11, 1, '2024-09-25', 1, 'Sin aderezo'),
    (13, 6, '2024-09-27', 2, 'Con jalapeños extras'),
    (17, 5, '2024-09-29', 3, 'Extra tocino'),
    (19, 4, '2024-10-02', 1, 'Sin aguacate'),
    (20, 7, '2024-10-04', 2, 'Con doble salsa'),
    (24, 2, '2024-10-06', 3, 'Sin jitomate'),
    (27, 3, '2024-10-08', 1, 'Extra cebolla'),
    (30, 8, '2024-10-10', 2, 'Sabor plátano'),
    (33, 9, '2024-10-12', 1, 'Agregar salsa especial'),
    (36, 5, '2024-10-14', 1, 'Sin aderezo'),
    (37, 6, '2024-10-16', 1, 'Con queso extra'),
    (39, 4, '2024-10-18', 2, 'Sin jitomate'),
    (40, 7, '2024-10-20', 3, 'Agregar tocino extra'),
    (6, 8, '2024-10-22', 1, 'Sabor chocolate'),
    (9, 3, '2024-10-24', 2, 'Sin chile'),
    (12, 5, '2024-10-26', 1, 'Extra tocino'),
    (15, 1, '2024-10-28', 1, 'Sin jitomate'),
    (18, 2, '2024-10-30', 3, 'Con jalapeños extras'),
    (22, 9, '2024-10-31', 1, 'Sin aderezo'),
    (25, 4, '2024-10-31', 2, 'Con tocino extra'),
    (28, 7, '2024-10-31', 1, 'Sin salsa'),
    (30, 8, '2024-10-31', 1, 'Sabor fresa'),
    (32, 1, '2024-10-31', 2, 'Con doble aderezo'),
    (34, 3, '2024-10-31', 1, 'Extra cebolla'),
    (37, 6, '2024-10-31', 2, 'Sin jalapeños'),
    (38, 9, '2024-10-31', 3, 'Con salsa especial'),
    (40, 5, '2024-10-31', 1, 'Sin jitomate'),
    (10, 2, '2024-10-31', 2, 'Extra queso'),
    (16, 4, '2024-10-31', 3, 'Con cebolla extra'),
    (20, 7, '2024-10-31', 1, 'Sin chile'),
    (21, 8, '2024-10-31', 2, 'Sabor chocolate'),
    (25, 3, '2024-10-31', 1, 'Sin jitomate'),
    (29, 6, '2024-10-31', 1, 'Sin aderezo'),
    (36, 9, '2024-10-31', 2, 'Con doble salsa'),
    (38, 1, '2024-10-31', 1, 'Sin chile'),
    (40, 5, '2024-10-31', 3, 'Sin jitomate'),
    (13, 8, '2024-10-31', 1, 'Sabor plátano'),
    (27, 4, '2024-10-31', 2, 'Sin aguacate'),
    (11, 7, '2024-10-31', 1, 'Extra tocino')
]
for pedido in pedidos:
    insertarPedido(*pedido)

# Cerrar la conexión
conexion.close()
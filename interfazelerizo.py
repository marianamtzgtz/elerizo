import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy import stats

# Conexión a la base de datos SQLite
conexion = sqlite3.connect('db_elerizo')
cursorDB = conexion.cursor()

# Función para actualizar el contenido de las tablas en la interfaz
def actualizar_tablas():
    for tree, query in [(tree_clientes, "SELECT * FROM CLIENTES"),
                        (tree_pedidos, "SELECT * FROM PEDIDOS"),
                        (tree_productos, "SELECT * FROM PRODUCTO")]:
        for row in tree.get_children():
            tree.delete(row)
        cursorDB.execute(query)
        for i, row in enumerate(cursorDB.fetchall()):
            # Alternar colores de las filas (par/impar)
            tree.insert("", tk.END, values=row, tags=('oddrow',) if i % 2 else ('evenrow',))

# Función para agregar estilos personalizados
def configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    # Estilo para el encabezado de las tablas
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4CAF50", foreground="white")

    # Estilo para las filas de la tabla
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.map("Treeview", background=[("selected", "#90EE90")])

    # Colores alternados para filas
    style.configure("oddrow", background="#f2f2f2")
    style.configure("evenrow", background="white")

# Función para agregar un cliente
def agregar_cliente():
    def guardar_cliente():
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()
        if nombre and telefono and direccion:
            cursorDB.execute(
                "INSERT INTO CLIENTES (NOMBRE, TELEFONO, DIRECCION) VALUES (?, ?, ?)",
                (nombre, telefono, direccion),
            )
            conexion.commit()
            actualizar_tablas()
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    ventana = tk.Toplevel()
    ventana.title("Agregar Cliente")

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
    tk.Label(ventana, text="Teléfono:").grid(row=1, column=0)
    tk.Label(ventana, text="Dirección:").grid(row=2, column=0)

    entry_nombre = tk.Entry(ventana)
    entry_telefono = tk.Entry(ventana)
    entry_direccion = tk.Entry(ventana)

    entry_nombre.grid(row=0, column=1)
    entry_telefono.grid(row=1, column=1)
    entry_direccion.grid(row=2, column=1)

    tk.Button(ventana, text="Guardar", command=guardar_cliente).grid(row=3, column=0, columnspan=2)

# Función para eliminar un cliente
def eliminar_cliente():
    item = tree_clientes.selection()
    if item:
        cliente_id = tree_clientes.item(item, "values")[0]
        cursorDB.execute("DELETE FROM CLIENTES WHERE IDC = ?", (cliente_id,))
        conexion.commit()
        actualizar_tablas()
    else:
        messagebox.showerror("Error", "Seleccione un cliente para eliminar.")

# Función para editar un cliente
def editar_cliente():
    item = tree_clientes.selection()
    if item:
        cliente_id, nombre, telefono, direccion = tree_clientes.item(item, "values")

        def guardar_edicion():
            nuevo_nombre = entry_nombre.get()
            nuevo_telefono = entry_telefono.get()
            nueva_direccion = entry_direccion.get()
            if nuevo_nombre and nuevo_telefono and nueva_direccion:
                cursorDB.execute(
                    "UPDATE CLIENTES SET NOMBRE = ?, TELEFONO = ?, DIRECCION = ? WHERE IDC = ?",
                    (nuevo_nombre, nuevo_telefono, nueva_direccion, cliente_id),
                )
                conexion.commit()
                actualizar_tablas()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")

        ventana = tk.Toplevel()
        ventana.title("Editar Cliente")

        tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
        tk.Label(ventana, text="Teléfono:").grid(row=1, column=0)
        tk.Label(ventana, text="Dirección:").grid(row=2, column=0)

        entry_nombre = tk.Entry(ventana)
        entry_telefono = tk.Entry(ventana)
        entry_direccion = tk.Entry(ventana)

        entry_nombre.insert(0, nombre)
        entry_telefono.insert(0, telefono)
        entry_direccion.insert(0, direccion)

        entry_nombre.grid(row=0, column=1)
        entry_telefono.grid(row=1, column=1)
        entry_direccion.grid(row=2, column=1)

        tk.Button(ventana, text="Guardar", command=guardar_edicion).grid(row=3, column=0, columnspan=2)
    else:
        messagebox.showerror("Error", "Seleccione un cliente para editar.")

# Función para agregar un pedido
def agregar_pedido():
    def guardar_pedido():
        cliente_id = entry_cliente_id.get()
        producto_id = entry_producto_id.get()
        fecha = entry_fecha.get()
        cantidad = entry_cantidad.get()
        nota = entry_nota.get()
        if cliente_id and producto_id and fecha and cantidad:
            try:
                cantidad = int(cantidad)
                cursorDB.execute('SELECT PRECIO FROM PRODUCTO WHERE IDT = ?', (producto_id,))
                precio = cursorDB.fetchone()
                if precio is None:
                    messagebox.showerror("Error", "Producto no encontrado.")
                    return
                total = precio[0] * cantidad
                cursorDB.execute(
                    "INSERT INTO PEDIDOS (ID_CLIENTE, ID_PRODUCTO, FECHA, NOTA, CANTIDAD, TOTAL) VALUES (?, ?, ?, ?, ?, ?)",
                    (cliente_id, producto_id, fecha, nota, cantidad, total),
                )
                conexion.commit()
                actualizar_tablas()
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser un número.")
        else:
            messagebox.showerror("Error", "Todos los campos excepto nota son obligatorios.")

    ventana = tk.Toplevel()
    ventana.title("Agregar Pedido")

    tk.Label(ventana, text="ID Cliente:").grid(row=0, column=0)
    tk.Label(ventana, text="ID Producto:").grid(row=1, column=0)
    tk.Label(ventana, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0)
    tk.Label(ventana, text="Cantidad:").grid(row=3, column=0)
    tk.Label(ventana, text="Nota:").grid(row=4, column=0)

    entry_cliente_id = tk.Entry(ventana)
    entry_producto_id = tk.Entry(ventana)
    entry_fecha = tk.Entry(ventana)
    entry_cantidad = tk.Entry(ventana)
    entry_nota = tk.Entry(ventana)

    entry_cliente_id.grid(row=0, column=1)
    entry_producto_id.grid(row=1, column=1)
    entry_fecha.grid(row=2, column=1)
    entry_cantidad.grid(row=3, column=1)
    entry_nota.grid(row=4, column=1)

    tk.Button(ventana, text="Guardar", command=guardar_pedido).grid(row=5, column=0, columnspan=2)

# Función para eliminar un pedido
def eliminar_pedido():
    item = tree_pedidos.selection()
    if item:
        pedido_id = tree_pedidos.item(item, "values")[0]
        cursorDB.execute("DELETE FROM PEDIDOS WHERE IDP = ?", (pedido_id,))
        conexion.commit()
        actualizar_tablas()
    else:
        messagebox.showerror("Error", "Seleccione un pedido para eliminar.")

# Función para editar un pedido
def editar_pedido():
    item = tree_pedidos.selection()
    if item:
        pedido_id, cliente_id, producto_id, fecha, nota, cantidad, total = tree_pedidos.item(item, "values")

        def guardar_edicion():
            nueva_cantidad = entry_cantidad.get()
            nueva_nota = entry_nota.get()
            if nueva_cantidad:
                try:
                    nueva_cantidad = int(nueva_cantidad)
                    cursorDB.execute('SELECT PRECIO FROM PRODUCTO WHERE IDT = ?', (producto_id,))
                    precio = cursorDB.fetchone()
                    if precio is None:
                        messagebox.showerror("Error", "Producto no encontrado.")
                        return
                    nuevo_total = precio[0] * nueva_cantidad
                    cursorDB.execute(
                        "UPDATE PEDIDOS SET CANTIDAD = ?, NOTA = ?, TOTAL = ? WHERE IDP = ?",
                        (nueva_cantidad, nueva_nota, nuevo_total, pedido_id),
                    )
                    conexion.commit()
                    actualizar_tablas()
                    ventana.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Cantidad debe ser un número.")
            else:
                messagebox.showerror("Error", "Cantidad es obligatorio.")

        ventana = tk.Toplevel()
        ventana.title("Editar Pedido")

        tk.Label(ventana, text="Cantidad:").grid(row=0, column=0)
        tk.Label(ventana, text="Nota:").grid(row=1, column=0)

        entry_cantidad = tk.Entry(ventana)
        entry_nota = tk.Entry(ventana)

        entry_cantidad.insert(0, cantidad)
        entry_nota.insert(0, nota)

        entry_cantidad.grid(row=0, column=1)
        entry_nota.grid(row=1, column=1)

        tk.Button(ventana, text="Guardar", command=guardar_edicion).grid(row=2, column=0, columnspan=2)
    else:
        messagebox.showerror("Error", "Seleccione un pedido para editar.")

# Función para graficar las ventas por cliente, incluyendo la media, moda y mediana
def ventanaGraficacion():
    def crear_grafica():
        # Obtener las ventas totales por cliente desde la base de datos
        cursorDB.execute("""
            SELECT CLIENTES.NOMBRE, SUM(PEDIDOS.TOTAL) 
            FROM PEDIDOS 
            INNER JOIN CLIENTES ON PEDIDOS.ID_CLIENTE = CLIENTES.IDC 
            GROUP BY CLIENTES.NOMBRE
        """)
        datos = cursorDB.fetchall()
        
        if not datos:
            messagebox.showinfo("Info", "No hay datos suficientes para generar la gráfica.")
            return

        # Preparar los datos para la gráfica
        nombres_clientes = [dato[0] for dato in datos]
        totales_ventas = [dato[1] for dato in datos]

        # Calcular estadísticas
        media = np.mean(totales_ventas)
        mediana = np.median(totales_ventas)
        moda = stats.mode(totales_ventas, keepdims=True).mode[0]

        # Crear la gráfica
        figura, ax = plt.subplots(figsize=(10, 6))
        ax.bar(nombres_clientes, totales_ventas, color='skyblue', label='Ventas por Cliente')

        # Dibujar líneas horizontales para la media, mediana y moda
        ax.axhline(y=media, color='green', linestyle='--', label=f'Media: {media:.2f}')
        ax.axhline(y=mediana, color='red', linestyle='--', label=f'Mediana: {mediana:.2f}')
        ax.axhline(y=moda, color='purple', linestyle='--', label=f'Moda: {moda:.2f}')

        # Etiquetas y diseño
        ax.set_xlabel('Clientes', fontsize=12)
        ax.set_ylabel('Total de Ventas', fontsize=12)
        ax.set_title('Ventas Totales por Cliente', fontsize=14)
        ax.legend()
        plt.xticks(rotation=45, ha='right', fontsize=10)

        plt.tight_layout()  # Ajustar la visualización
        plt.show()

    # Llamar a la función para crear la gráfica
    crear_grafica()

# Función para mostrar la gráfica de pastel con productos más vendidos
def ventanaGraficapastel():
    def obtener_datos_ventas():
        cursorDB.execute("""
            SELECT P.NOMBRE, SUM(D.CANTIDAD) as total_vendido
            FROM PEDIDOS D
            JOIN PRODUCTO P ON D.IDT = P.IDT
            GROUP BY D.IDT
            ORDER BY total_vendido DESC
        """)
        return cursorDB.fetchall()

    def mostrar_grafica_productos():
        productos = obtener_datos_ventas()

        if not productos:
            messagebox.showinfo("Información", "No hay datos de ventas para mostrar.")
            return

        nombres = [p[0] for p in productos]
        cantidades = [p[1] for p in productos]

        # Crear la figura de la gráfica
        figura, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            cantidades,
            labels=nombres,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.tab20.colors,
        )
        ax.set_title("Distribución de Productos Vendidos", fontsize=14)

        # Mostrar la gráfica
        plt.show()

    # Mostrar la gráfica de pastel
    mostrar_grafica_productos()
    
# Configurar la ventana principal
root = tk.Tk()
root.title("Gestión de Base de Datos")

# Configurar estilos
configurar_estilos()

# Frame para la tabla de clientes
frame_clientes = ttk.LabelFrame(root, text="Clientes")
frame_clientes.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

btn_add_cliente = tk.Button(frame_clientes, text="Agregar Cliente", command=agregar_cliente)
btn_add_cliente.pack(side="left", padx=5)
btn_delete_cliente = tk.Button(frame_clientes, text="Eliminar Cliente", command=eliminar_cliente)
btn_delete_cliente.pack(side="left", padx=5)
btn_edit_cliente = tk.Button(frame_clientes, text="Editar Cliente", command=editar_cliente)
btn_edit_cliente.pack(side="left", padx=5)

tree_clientes = ttk.Treeview(frame_clientes, columns=("ID", "Nombre", "Teléfono", "Dirección"), show="headings", style="Treeview")
tree_clientes.pack(fill="both", expand="yes")
for col in ("ID", "Nombre", "Teléfono", "Dirección"):
    tree_clientes.heading(col, text=col)

# Frame para la tabla de pedidos
frame_pedidos = ttk.LabelFrame(root, text="Pedidos")
frame_pedidos.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

btn_add_pedido = tk.Button(frame_pedidos, text="Agregar Pedido", command=agregar_pedido)
btn_add_pedido.pack(side="left", padx=5)
btn_delete_pedido = tk.Button(frame_pedidos, text="Eliminar Pedido", command=eliminar_pedido)
btn_delete_pedido.pack(side="left", padx=5)
btn_edit_pedido = tk.Button(frame_pedidos, text="Editar Pedido", command=editar_pedido)
btn_edit_pedido.pack(side="left", padx=5)

tree_pedidos = ttk.Treeview(frame_pedidos, columns=("ID", "Cliente", "Producto", "Fecha", "Nota", "Cantidad", "Total"), show="headings", style="Treeview")
tree_pedidos.pack(fill="both", expand="yes")
for col in ("ID", "Cliente", "Producto", "Fecha", "Nota", "Cantidad", "Total"):
    tree_pedidos.heading(col, text=col)

# Frame para la tabla de productos
frame_productos = ttk.LabelFrame(root, text="Productos")
frame_productos.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

tree_productos = ttk.Treeview(frame_productos, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings", style="Treeview")
tree_productos.pack(fill="both", expand="yes")
for col in ("ID", "Nombre", "Descripción", "Precio"):
    tree_productos.heading(col, text=col)

# Frame adicional en la fila 3 para los botones
frame_botones = ttk.LabelFrame(root, text="Controles Adicionales")
frame_botones.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

# Botones en el nuevo frame
btn_grafica = tk.Button(frame_botones, text="GRAFICA DE BARRAS", command=ventanaGraficacion)
btn_grafica.pack(side="left", padx=5)
btn_graficapastel = tk.Button(frame_botones, text="GRAFICA DE PASTEL", command=ventanaGraficapastel)
btn_graficapastel.pack(side="left", padx=5)


# Configuración del grid para adaptabilidad
root.grid_rowconfigure(0, weight=1)  # Ajustar la primera fila
root.grid_rowconfigure(1, weight=1)  # Ajustar la segunda fila
root.grid_rowconfigure(2, weight=1)  # Ajustar la tercera fila para productos
root.grid_rowconfigure(3, weight=0)  # Ajustar la cuarta fila para botones
root.grid_columnconfigure(0, weight=1)  # Ajustar la primera columna
root.grid_columnconfigure(1, weight=1)  # Ajustar la segunda columna

# Actualizar tablas al inicio
actualizar_tablas()

# Iniciar la aplicación
root.mainloop()
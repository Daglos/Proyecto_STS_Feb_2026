import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import DatabaseManager
from reports import ReportGenerator
from datetime import datetime

class InventoryManagementApp:
    """Aplicación de gestión de inventario con interfaz Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Sistema de Gestión de Inventario")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        self.report_gen = ReportGenerator()
        
        if not self.db.connect():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        if not self.db.create_tables():
            messagebox.showerror("Error", "No se pudieron crear las tablas")
            return
        
        # Variables de sesión
        self.producto_seleccionado = None
        
        # Crear interfaz
        self.crear_interfaz()
        self.cargar_productos()
    
    # (Se eliminaron las configuraciones de colores personalizadas)
    
    def crear_interfaz(self):
        """Crear la interfaz principal mejorada"""
        # Menú
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        
        reportes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📊 Reportes", menu=reportes_menu)
        reportes_menu.add_command(label="Inventario", command=self.generar_reporte_inventario)
        reportes_menu.add_command(label="Movimientos", command=self.generar_reporte_movimientos)
        reportes_menu.add_command(label="Estadísticas", command=self.generar_reporte_estadisticas)
        
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Encabezado
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        header_label = ttk.Label(header_frame, text="✨ Sistema de Gestión de Inventario", 
                                 style='Header.TLabel')
        header_label.pack(side=tk.LEFT)
        
        # Contenedor principal (3 columnas)
        container = ttk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Frame izquierdo - Formulario
        left_frame = ttk.LabelFrame(container, text="📝 Datos del Producto", padding=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 12), ipady=10)
        
        # Campos del formulario con mejor espaciado
        labels_values = [
            ('Nombre:', 'nombre_entry', 25),
            ('Descripción:', 'descripcion_text', None),
            ('Cantidad:', 'cantidad_entry', 25),
            ('Precio Unitario:', 'precio_entry', 25),
            ('Proveedor:', 'proveedor_entry', 25),
        ]
        
        row = 0
        for label_text, attr, width in labels_values:
            label = ttk.Label(left_frame, text=label_text, style='TLabel')
            label.grid(row=row, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            if attr == 'descripcion_text':
                text_widget = tk.Text(left_frame, width=25, height=4, font=('Segoe UI', 9), 
                                      relief=tk.FLAT, borderwidth=2)
                text_widget.grid(row=row, column=1, pady=8, sticky=tk.EW)
                setattr(self, attr, text_widget)
            else:
                entry = ttk.Entry(left_frame, width=width)
                entry.grid(row=row, column=1, pady=8, sticky=tk.EW)
                setattr(self, attr, entry)
            
            row += 1
        
        # Frame de botones principal con mejor diseño
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky=tk.EW)
        
        create_btn = ttk.Button(button_frame, text="➕ Crear", command=self.crear_producto, style='Create.TButton')
        create_btn.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        
        update_btn = ttk.Button(button_frame, text="✏️ Actualizar", command=self.actualizar_producto, style='Update.TButton')
        update_btn.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        
        delete_btn = ttk.Button(button_frame, text="🗑️ Eliminar", command=self.eliminar_producto, style='Delete.TButton')
        delete_btn.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        
        clear_btn = ttk.Button(button_frame, text="🔄 Limpiar", command=self.limpiar_campos)
        clear_btn.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        
        # Frame derecho - Listado y movimientos
        right_container = ttk.Frame(container)
        right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Tabla de productos
        table_frame = ttk.LabelFrame(right_container, text="📦 Productos Registrados", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 0), pady=(0, 12))
        
        scroll = ttk.Scrollbar(table_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Nombre', 'Cantidad', 'Precio', 'Proveedor'),
            height=15,
            yscrollcommand=scroll.set,
            show='headings'
        )
        scroll.config(command=self.tree.yview)
        
        # Configurar columnas con mejor ancho
        self.tree.column('ID', anchor=tk.CENTER, width=50)
        self.tree.column('Nombre', anchor=tk.W, width=250)
        self.tree.column('Cantidad', anchor=tk.CENTER, width=100)
        self.tree.column('Precio', anchor=tk.CENTER, width=120)
        self.tree.column('Proveedor', anchor=tk.W, width=200)
        
        # Encabezados mejorados
        self.tree.heading('ID', text='ID', anchor=tk.CENTER)
        self.tree.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tree.heading('Cantidad', text='Cantidad', anchor=tk.CENTER)
        self.tree.heading('Precio', text='Precio Unitario', anchor=tk.CENTER)
        self.tree.heading('Proveedor', text='Proveedor', anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.tree.bind('<Double-1>', self.cargar_producto_seleccionado)
        
        # Frame de movimientos mejorado
        mov_frame = ttk.LabelFrame(right_container, text="➡️ Movimiento de Inventario", padding=12)
        mov_frame.pack(fill=tk.X, pady=(0, 12))
        
        mov_inner = ttk.Frame(mov_frame)
        mov_inner.pack(fill=tk.X)
        
        ttk.Label(mov_inner, text="Tipo:", style='TLabel').pack(side=tk.LEFT, padx=5)
        self.tipo_mov = ttk.Combobox(mov_inner, values=['📥 Entrada', '📤 Salida'], width=12, state='readonly')
        self.tipo_mov.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(mov_inner, text="Cantidad:", style='TLabel').pack(side=tk.LEFT, padx=5)
        self.mov_cantidad = ttk.Entry(mov_inner, width=12)
        self.mov_cantidad.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(mov_inner, text="✔️ Registrar", command=self.registrar_movimiento).pack(side=tk.LEFT, padx=5)
        
        # Frame de estadísticas mejorado
        stats_frame = ttk.LabelFrame(right_container, text="📈 Estadísticas en Tiempo Real", padding=12)
        stats_frame.pack(fill=tk.X)
        
        self.stats_label = ttk.Label(stats_frame, text="", style='Stats.TLabel')
        self.stats_label.pack(fill=tk.X)
        
        self.actualizar_estadisticas()
    
    def cargar_productos(self):
        """Cargar productos en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.db.obtener_productos()
        for producto in productos:
            self.tree.insert(
                '',
                tk.END,
                values=(
                    producto['id'],
                    producto['nombre'],
                    producto['cantidad'],
                    f"${float(producto['precio_unitario']):.2f}",
                    producto['proveedor'] if producto['proveedor'] else 'N/A'
                )
            )
    
    def cargar_producto_seleccionado(self, event):
        """Cargar datos del producto seleccionado en el formulario"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        id_producto = item['values'][0]
        
        producto = self.db.obtener_producto(id_producto)
        if producto:
            self.producto_seleccionado = id_producto
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, producto['nombre'])
            
            self.descripcion_text.delete('1.0', tk.END)
            self.descripcion_text.insert('1.0', producto['descripcion'] if producto['descripcion'] else '')
            
            self.cantidad_entry.delete(0, tk.END)
            self.cantidad_entry.insert(0, str(producto['cantidad']))
            
            self.precio_entry.delete(0, tk.END)
            self.precio_entry.insert(0, str(producto['precio_unitario']))
            
            self.proveedor_entry.delete(0, tk.END)
            self.proveedor_entry.insert(0, producto['proveedor'] if producto['proveedor'] else '')
    
    def crear_producto(self):
        """Crear nuevo producto"""
        try:
            nombre = self.nombre_entry.get()
            descripcion = self.descripcion_text.get('1.0', tk.END).strip()
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())
            proveedor = self.proveedor_entry.get()
            
            if not nombre:
                messagebox.showwarning("⚠️ Validación", "El nombre del producto es requerido")
                return
            
            if precio < 0 or cantidad < 0:
                messagebox.showwarning("⚠️ Validación", "Cantidad y Precio no pueden ser negativos")
                return
            
            success, msg = self.db.crear_producto(nombre, descripcion, cantidad, precio, proveedor)
            if success:
                messagebox.showinfo("✅ Éxito", f"Producto creado exitosamente:\n{nombre}")
                self.limpiar_campos()
                self.cargar_productos()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("❌ Error", msg)
        except ValueError:
            messagebox.showerror("❌ Error de Validación", "Verifique que:\n• Cantidad sea un número entero\n• Precio sea un número decimal")
    
    def actualizar_producto(self):
        """Actualizar producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("⚠️ Validación", "Seleccione un producto de la tabla")
            return
        
        try:
            nombre = self.nombre_entry.get()
            descripcion = self.descripcion_text.get('1.0', tk.END).strip()
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())
            proveedor = self.proveedor_entry.get()
            
            success, msg = self.db.actualizar_producto(
                self.producto_seleccionado, nombre, descripcion, cantidad, precio, proveedor
            )
            if success:
                messagebox.showinfo("✅ Éxito", msg)
                self.limpiar_campos()
                self.cargar_productos()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("❌ Error", msg)
        except ValueError:
            messagebox.showerror("❌ Error de Validación", "Cantidad debe ser número entero y Precio debe ser decimal")
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("⚠️ Validación", "Seleccione un producto de la tabla")
            return
        
        if messagebox.askyesno("⚠️ Confirmación", "¿Está seguro que desea eliminar este producto?"):
            success, msg = self.db.eliminar_producto(self.producto_seleccionado)
            if success:
                messagebox.showinfo("✅ Éxito", msg)
                self.limpiar_campos()
                self.cargar_productos()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("❌ Error", msg)
    
    def limpiar_campos(self):
        """Limpiar los campos del formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.descripcion_text.delete('1.0', tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.proveedor_entry.delete(0, tk.END)
        self.producto_seleccionado = None
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
    
    def registrar_movimiento(self):
        """Registrar movimiento de inventario"""
        try:
            selection = self.tree.selection()
            if not selection:
                messagebox.showwarning("⚠️ Validación", "Seleccione un producto de la tabla")
                return
            
            item = self.tree.item(selection[0])
            id_producto = item['values'][0]
            
            tipo_valor = self.tipo_mov.get()
            if not tipo_valor:
                messagebox.showwarning("⚠️ Validación", "Seleccione tipo de movimiento")
                return
            
            # Extraer el tipo sin el emoji
            tipo = tipo_valor.split(' ')[-1]
            cantidad = int(self.mov_cantidad.get())
            
            success, msg = self.db.registrar_movimiento(id_producto, tipo, cantidad)
            if success:
                messagebox.showinfo("✅ Éxito", msg)
                self.mov_cantidad.delete(0, tk.END)
                self.tipo_mov.set('')
                self.cargar_productos()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("❌ Error", msg)
        except ValueError:
            messagebox.showerror("❌ Error de Validación", "La cantidad debe ser un número entero")
    
    def mostrar_acerca_de(self):
        """Mostrar información acerca de la aplicación"""
        messagebox.showinfo(
            "ℹ️ Acerca de",
            "📦 Sistema de Gestión de Inventario\n\n"
            "Versión: 2.0\n"
            "Desarrollado con Python y Tkinter\n\n"
            "Características:\n"
            "  • Gestión completa de inventario\n"
            "  • Base de datos MySQL\n"
            "  • Reportes en PDF\n"
            "  • Estadísticas en tiempo real\n\n"
            "© 2026 - Equipo de Desarrollo"
        )
    
    def actualizar_estadisticas(self):
        """Actualizar estadísticas mostradas con formato profesional"""
        stats = self.db.obtener_estadisticas()
        total_prod = stats.get('total_productos', 0)
        stock_total = stats.get('stock_total', 0)
        valor_total = stats.get('valor_total', 0)
        bajo_stock = stats.get('bajo_stock', 0)
        
        # Crear texto con emojis y formato profesional
        texto = (
            f"  📊 Productos: {total_prod}  │  "
            f"📦 Stock Total: {stock_total}  │  "
            f"💰 Valor Total: ${valor_total:.2f}  │  "
            f"⚠️ Bajo Stock: {bajo_stock}"
        )
        self.stats_label.config(text=texto)
    
    def generar_reporte_inventario(self):
        """Generar reporte de inventario"""
        productos = self.db.obtener_productos()
        if not productos:
            messagebox.showwarning("⚠️ Advertencia", "No hay productos registrados para generar reporte")
            return
        
        success, msg = self.report_gen.generar_reporte_inventario(productos)
        if success:
            messagebox.showinfo("✅ Éxito", f"Reporte de inventario generado:\n{msg}")
        else:
            messagebox.showerror("❌ Error", msg)
    
    def generar_reporte_movimientos(self):
        """Generar reporte de movimientos"""
        movimientos = self.db.obtener_movimientos()
        if not movimientos:
            messagebox.showwarning("⚠️ Advertencia", "No hay movimientos registrados para generar reporte")
            return
        
        productos = self.db.obtener_productos()
        productos_dict = {p['id']: p for p in productos}
        
        success, msg = self.report_gen.generar_reporte_movimientos(movimientos, productos_dict)
        if success:
            messagebox.showinfo("✅ Éxito", f"Reporte de movimientos generado:\n{msg}")
        else:
            messagebox.showerror("❌ Error", msg)
    
    def generar_reporte_estadisticas(self):
        """Generar reporte de estadísticas"""
        stats = self.db.obtener_estadisticas()
        success, msg = self.report_gen.generar_reporte_estadisticas(stats)
        if success:
            messagebox.showinfo("✅ Éxito", f"Reporte de estadísticas generado:\n{msg}")
        else:
            messagebox.showerror("❌ Error", msg)
    
    def cerrar(self):
        """Cerrar la aplicación"""
        self.db.disconnect()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar)
    root.mainloop()

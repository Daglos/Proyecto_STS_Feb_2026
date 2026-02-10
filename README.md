# Sistema de Gestión de Inventario

## Descripción
Sistema completo de gestión de inventario que permite el registro, edición, visualización, eliminación de productos y generación de reportes en PDF.

## Características
- ✅ **CRUD Completo**: Crear, Leer, Actualizar, Eliminar productos
- ✅ **Base de Datos MySQL**: Almacenamiento persistente de datos
- ✅ **Interfaz Gráfica**: Aplicación de escritorio con Tkinter
- ✅ **Movimientos de Inventario**: Registro de entradas y salidas
- ✅ **Reportes en PDF**: Estadísticas, inventario y movimientos
- ✅ **Estadísticas en Tiempo Real**: Seguimiento de stock y valor

## Estructura del Proyecto
```
Proyecto_Seminario_Software/
├── main.py              # Punto de entrada de la aplicación
├── gui.py               # Interfaz gráfica (Tkinter)
├── database.py          # Gestor de base de datos MySQL
├── reports.py           # Generador de reportes en PDF
├── config.py            # Configuración del proyecto
├── requirements.txt     # Dependencias Python
└── README.md           # Este archivo
```

## Requisitos Previos
- Python 3.7 o superior
- MySQL Server instalado y funcionando
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar o descargar el proyecto
```bash
cd Proyecto_Seminario_Software
```

### 2. Crear un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

Primero, asegúrate de que MySQL Server está ejecutándose.

Abre el archivo `config.py` y actualiza las credenciales:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Tu usuario de MySQL
    'password': 'tu_contraseña',  # Tu contraseña de MySQL
    'database': 'inventory_management',
    'raise_on_warnings': True
}
```

Luego, crea la base de datos en MySQL:
```bash
mysql -u root -p
```

```sql
CREATE DATABASE inventory_management;
EXIT;
```

## Uso

### Ejecutar la aplicación
```bash
python main.py
```

## Funcionalidades

### 1. Gestión de Productos
- **Crear**: Añadir nuevos productos con nombre, descripción, cantidad, precio y proveedor
- **Ver**: Visualizar todos los productos en una tabla
- **Editar**: Doble clic en un producto para cargar sus datos y actualizar
- **Eliminar**: Remover productos del inventario

### 2. Movimientos de Inventario
- Registrar entradas y salidas de producto
- Actualización automática de stock
- Historial de movimientos

### 3. Reportes
- **Reporte de Inventario**: Listado completo de productos en PDF
- **Reporte de Movimientos**: Historial de movimientos de inventario
- **Reporte de Estadísticas**: Resumen con totales y métricas

### 4. Estadísticas en Tiempo Real
- Total de productos
- Stock total del inventario
- Valor total del inventario
- Cantidad de productos con stock bajo (< 10)

## Base de Datos

### Tabla: productos
```sql
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    cantidad INT NOT NULL DEFAULT 0,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    proveedor VARCHAR(255),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Tabla: movimientos
```sql
CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    tipo_movimiento VARCHAR(50),
    cantidad INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
);
```

## Troubleshooting

### Error: "No se pudo conectar a la base de datos"
- Verifica que MySQL Server está ejecutándose
- Comprueba las credenciales en `config.py`
- Confirma que la base de datos `inventory_management` existe

### Error: "No module named 'mysql'"
```bash
pip install mysql-connector-python
```

### Los reportes no se generan
- Verifica que existe la carpeta `reportes/` o déjala que se cree automáticamente
- Comprueba permisos de escritura en el directorio del proyecto

## Contribuciones
Las contribuciones son bienvenidas. Para cambios importantes, abre un issue primero.

## Licencia
Este proyecto está bajo licencia MIT.

## Autor
Proyecto Seminario de Software

---
**Última actualización**: Febrero 2026

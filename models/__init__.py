from flask_sqlalchemy import SQLAlchemy

# Crear la instancia global de SQLAlchemy
db = SQLAlchemy()

# Importar los modelos para que estén disponibles al inicializar
from .usuarios import Usuario
from .pagos import Pago
from .documentos import Documentos
from .programacion_impresion import ProgramacionImpresion
from .almacen import Almacen
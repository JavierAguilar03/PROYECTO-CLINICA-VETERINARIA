# Proyecto: Clínica Veterinaria

Breve descripción
------------------
Este repositorio contiene una aplicación en Python para gestionar aspectos de una clínica veterinaria (entidades, persistencia, pruebas, etc.). El archivo principal de ejecución es `app.py` en la raíz del proyecto.

Requisitos
----------
- Python 3.8+ (se recomienda 3.10+)
- pip
- (Opcional) un entorno virtual

Instalación rápida (Windows PowerShell)
--------------------------------------
1. Crear y activar un entorno virtual (recomendado):

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Ejecución
---------
Para ejecutar la aplicación localmente (si `app.py` está pensado para correr como entrypoint):

```powershell
streamlit run app.py
```

Si la aplicación usa un framework (por ejemplo FastAPI/Flask) revisa `app.py` para ver comandos específicos.

Tests
-----
Las pruebas unitarias están bajo el directorio `test/` y usan `pytest`.

Ejecutarlas:

```powershell
pytest -q
```

Estructura del proyecto (resumen)
--------------------------------
- `app.py` — punto de entrada de la aplicación
- `requirements.txt` — dependencias del proyecto
- `env/` — entorno virtual (generalmente ignorado por `.gitignore`)
- `pages/`, `src/`, `test/` — código fuente, módulos y pruebas

Contribuir
---------
1. Haz un fork o crea una rama nueva para tus cambios.
2. Añade pruebas para nuevas funcionalidades o correcciones.
3. Envía un pull request con una descripción clara de los cambios.

Notas y recomendaciones
-----------------------
- El repositorio ya contiene un `.gitignore` para excluir entornos virtuales, archivos temporales y configuraciones de editores.
- Añade un archivo `LICENSE` si quieres aclarar la licencia del proyecto.

Contacto
-------
Para preguntas, abre un issue en el repositorio.

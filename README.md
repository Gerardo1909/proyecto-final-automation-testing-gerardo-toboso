# Proyecto final - Curso QA Automation

**Realizado por: Gerardo Toboso**

![CI
Status](https://github.com/Gerardo1909/proyecto-final-automation-testing-gerardo-toboso/actions/workflows/ci.yml/badge.svg)

## Propósito

El propósito de esta entrega final es aplicar los conocimientos adquiridos sobre la **automatización de pruebas de software** 
haciendo uso de **Python** como lenguaje de programación principal y librerías pertinentes para este contexto como lo son **Pytest, Selenium y Requests**. Los puntos que se ponen en práctica más precisamente son:

* Automatización de flujos básicos de navegación web utilizando **Selenium WebDriver**.

* Interacción con elementos web.

* Estrategias de localización y validación de estados dentro de una página.

* Construir un conjunto de pruebas extenso que abarque las funcionalidades más importantes de la página.

* Automatización de pruebas de **API REST** utilizando **Requests**.

* Validación de respuestas HTTP incluyendo status codes, headers, estructura de datos y performance.

* Implementación de pruebas E2E para el ciclo de vida completo de recursos (CRUD).

En este caso la página que se estará utilizando será [saucedemo.com](https://www.saucedemo.com/), la cual está diseñada
exclusivamente para llevar a cabo pruebas de UI, y la API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com/) para pruebas de API.

## Tecnologías usadas

* **Python 3.13+**: Lenguaje de programación principal
* **Selenium 4.35.0**: Automatización de navegador web
* **Requests 2.32.5**: Cliente HTTP para pruebas de API REST
* **Pytest 8.4.2**: Framework de testing unitario y de integración
* **Pytest-HTML 3.2.0**: Generación de reportes HTML para las pruebas
* **Pytest-Check 2.6.0**: Soft assertions para mejor granularidad en los tests
* **Pytest-Timeout 2.4.0**: Control de tiempo máximo de ejecución de tests

## Estructura del proyecto

```text
proyecto-final-automation-testing-gerardo-toboso/
├── src/
│   ├── data/                    # Datos de prueba (CSV, JSON)
│   ├── logs/                    # Archivos de log (pytest y behave)
│   ├── pages/                   # Page Objects (patrón de diseño)
│   ├── reports/                 # Reportes HTML, JSON y screenshots de fallos
│   ├── tests/                   # Casos de prueba con pytest
│   │   ├── conftest.py         # Configuración de fixtures y hooks de pytest
│   │   ├── test_catalog.py
│   │   ├── test_login.py
│   │   ├── test_shopping_cart.py
│   │   ├── test_json_placeholder.py  # Pruebas de API individuales (GET, POST, PUT, PATCH, DELETE)
│   │   └── test_post_lifecycle.py    # Pruebas E2E del ciclo de vida completo de un post (CRUD)
│   └── utils/                   # Utilidades compartidas
│       ├── api_utils.py        # Función helper para validación de respuestas API
│       ├── logger.py           # Logger para pruebas pytest y behave
│       ├── csv_reader.py
│       ├── json_reader.py
│       └── screenshot_saver.py
├── .gitignore                   # Archivos ignorados por git
├── pytest.ini                   # Configuración de pytest (markers, opciones, etc.)
├── pyproject.toml               # Configuración del proyecto y dependencias
├── requirements.txt             # Lista de dependencias del proyecto
└── README.md                    # Este archivo
```

## Instrucciones de instalación de dependencias

> Antes de seguir los siguientes pasos asegúrate de tener Python 3.13+ instalado en tu máquina local.

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Gerardo1909/proyecto-final-automation-testing-gerardo_toboso.git
   cd proyecto-final-automation-testing-gerardo_toboso
   ```

2. Crea un entorno virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows
```

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Mac/Linux
```

3. Instala las dependencias usando pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Descarga el WebDriver de Google Chrome [en este link](https://googlechromelabs.github.io/chrome-for-testing/) verificando que la versión coincida con la que está actualmente en tu navegador.

> Asegúrate de que el WebDriver esté en tu PATH o especifica su ubicación en el código (puedes ayudarte con [esta consulta en StackOverflow](https://stackoverflow.com/questions/40555930/selenium-chromedriver-executable-needs-to-be-in-path)).

## Comandos para ejecutar las pruebas

> Asegúrate de tener activado el entorno virtual que creaste anteriormente

Ubicado en el directorio de raíz del proyecto, ejecuta:

```bash
pytest
```

Este comando ejecutará:
- Todas las pruebas escritas en Pytest
- Generará logs detallados en `src/logs/` (test.log para Pytest)
- Creará un reporte HTML de Pytest en `src/reports/report.html`
- Guardará screenshots de fallos en `src/reports/screenshots/`

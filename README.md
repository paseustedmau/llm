# Lumen Casa — Sistema de atención al cliente con IA

Proyecto 3 del módulo **LLM**: un chatbot de soporte para una tienda ficticia,
construido con Streamlit y la API de OpenAI.

El asistente, llamado **Sol**, mantiene el contexto de la conversación y puede
usar herramientas locales para consultar pedidos, explicar políticas y escalar
un caso a una persona. Todos los clientes, pedidos y tickets son simulados.

## Funcionalidades

- Chat conversacional en español mediante la **Responses API de OpenAI**.
- Consulta de una base de datos ficticia de pedidos.
- Base de conocimiento de envíos, devoluciones, garantía y pagos.
- Creación simulada de tickets para atención humana.
- Historial durante la sesión y botón para comenzar una conversación nueva.
- Reglas para evitar inventar estados o solicitar datos sensibles.
- Mensajes claros ante errores de autenticación, conexión o límite de uso.
- Pruebas unitarias de la lógica local, sin consumir créditos de la API.

## Requisitos

- Python 3.10 o superior.
- Una clave de la [API de OpenAI](https://platform.openai.com/api-keys).

> Una suscripción de ChatGPT no incluye automáticamente créditos para la API.

## Instalación

Desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell, activa el entorno con:

```powershell
.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuración

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita `.env` y reemplaza el valor de ejemplo:

```dotenv
OPENAI_API_KEY=sk-tu-clave-real
OPENAI_MODEL=gpt-5.4-mini
```

También puedes omitir `.env` e ingresar la clave temporalmente en la barra
lateral. El archivo `.env` está excluido de Git para evitar publicar secretos.

## Ejecución

```bash
streamlit run app.py
```

Streamlit mostrará la URL local, normalmente `http://localhost:8501`.

Prueba cualquiera de estas consultas:

- `¿Dónde está mi pedido LUM-1042?`
- `¿Puedo devolver un producto después de abrirlo?`
- `Quiero hablar con una persona.`

Pedidos disponibles en la demostración: `LUM-1042`, `LUM-2088` y `LUM-3301`.

## Pruebas

Las pruebas no llaman a OpenAI y, por tanto, no consumen créditos:

```bash
pip install -r requirements-dev.txt
pytest
```

## Estructura

```text
.
├── app.py                  # Interfaz Streamlit
├── support/
│   ├── assistant.py        # Responses API y ciclo de function calling
│   └── data.py             # Pedidos, políticas y tickets ficticios
├── tests/test_data.py      # Pruebas de la lógica simulada
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## Flujo técnico

1. Streamlit envía el mensaje a la Responses API.
2. El modelo decide si necesita una herramienta local.
3. Python ejecuta la consulta sobre datos ficticios y devuelve el resultado al
   modelo.
4. El modelo redacta una respuesta natural sin inventar información.
5. `previous_response_id` conserva el contexto mientras dura la sesión.

La clave nunca se incluye en el código ni se envía al navegador como parte de
la conversación. Para un sistema real habría que añadir autenticación, una base
de datos persistente, verificación de identidad, observabilidad y controles de
privacidad.

## Tecnologías

- Python
- Streamlit
- SDK oficial de OpenAI para Python
- Pytest

## Referencias

- [Generación de texto con la Responses API](https://developers.openai.com/api/docs/guides/text)
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [SDK de OpenAI](https://developers.openai.com/api/docs/libraries)

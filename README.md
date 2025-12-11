# Webflow Webhook Handler

Este script de Flask recibe webhooks de formularios de Webflow y envía los datos por correo electrónico utilizando SMTP.

## Despliegue en Render.com

1. Crea un nuevo **Web Service** en Render.
2. Conecta tu repositorio.
3. Configura el **Build Command**: `pip install -r requirements.txt`
4. Configura el **Start Command**: `gunicorn app:app`

## Variables de Entorno

Para que el envío de correos funcione, debes configurar las siguientes variables de entorno en tu proveedor de hosting (Render, Heroku, etc.) o en tu archivo `.env` local:

| Variable        | Descripción                                      | Ejemplo (Gmail)          |
|-----------------|--------------------------------------------------|--------------------------|
| `SMTP_USER`     | Tu dirección de correo electrónico remitente.    | `tu_email@gmail.com`     |
| `SMTP_PASSWORD` | Tu contraseña de aplicación (App Password).      | `abcd 1234 efgh 5678`    |
| `SMTP_SERVER`   | El servidor SMTP de tu proveedor de correo.      | `smtp.gmail.com`         |
| `SMTP_PORT`     | El puerto SMTP (generalmente 587 para TLS).      | `587`                    |

> **Nota para Gmail:** Si usas Gmail, debes habilitar la verificación en dos pasos y generar una **Contraseña de Aplicación** para usar en `SMTP_PASSWORD`. No uses tu contraseña normal.

## Configuración de Formularios

Edita el diccionario `FORM_CONFIG` en `app.py` para mapear los nombres de tus formularios de Webflow a los correos de destino:

```python
FORM_CONFIG = {
    'Nombre Formulario Webflow': 'email_destino@empresa.com',
    'Otro Formulario': 'otro_email@empresa.com'
}
```

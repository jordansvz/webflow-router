import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

# Configuración de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Diccionario de mapeo: 'Nombre del Formulario en Webflow': 'email_destino@empresa.com'
# Puedes agregar más formularios aquí fácilmente.
FORM_CONFIG = {
    'Contact Form': 'jordan.svz1@gmail.com',
    'Support Ticket': 'esveidi.esveidi@gmail.com',
    'Newsletter Signup': 'jordy.queno@gmail.com',
    # 'Nombre Exacto en Webflow': 'email@destino.com'
}

# Configuración SMTP desde Variables de Entorno
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

import threading

# ... (imports remain the same)

def send_email_thread(to_email, form_name, form_data):
    """
    Función para enviar el correo en un hilo separado.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.error("Error: Variables de entorno SMTP_USER o SMTP_PASSWORD no configuradas.")
        return

    try:
        logger.info(f"Iniciando envío de correo a {to_email}...")
        
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = f"Nuevo envío de formulario: {form_name}"

        # Construir el cuerpo del correo
        body = f"Se ha recibido un nuevo envío del formulario '{form_name}'.\n\nDatos:\n"
        for key, value in form_data.items():
            body += f"- {key}: {value}\n"
        
        msg.attach(MIMEText(body, 'plain'))

        # Conexión SMTP
        logger.info("Conectando al servidor SMTP...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() # Encriptación TLS
        
        logger.info("Iniciando sesión SMTP...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        
        logger.info("Enviando mensaje...")
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Correo enviado exitosamente a {to_email} para el formulario '{form_name}'")

    except Exception as e:
        logger.error(f"Error al enviar correo: {e}")

def send_email(to_email, form_name, form_data):
    """
    Inicia el envío de correo en segundo plano.
    """
    thread = threading.Thread(target=send_email_thread, args=(to_email, form_name, form_data))
    thread.start()
    return True

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # ... (rest of the function)
    # ...
        # Verificar si el formulario está en nuestra configuración
        if form_name in FORM_CONFIG:
            target_email = FORM_CONFIG[form_name]
            logger.info(f"Procesando formulario: {form_name} -> Enviando a {target_email}")
            
            # Extraer los datos reales del formulario
            form_data = payload.get('data', {})
            
            # Enviar el correo en segundo plano
            send_email(target_email, form_name, form_data)
            
            return jsonify({"status": "success", "message": "Email processing started"}), 200

        else:
            # Si el formulario no está configurado, logueamos y respondemos 200
            logger.warning(f"Formulario recibido '{form_name}' no está configurado en FORM_CONFIG. Ignorando.")
            return jsonify({"status": "ignored", "reason": "Form not configured"}), 200

    except Exception as e:
        logger.error(f"Error interno en el webhook: {e}")
        # En caso de error de servidor, Webflow podría reintentar si devolvemos 500. 
        # Dependiendo de la lógica deseada, podemos devolver 500 o 200. 
        # Para seguridad de que no se rompa el flujo de Webflow, a veces es mejor 200 si es un error de datos.
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def health_check():
    return "Webflow Webhook Listener is running."

if __name__ == '__main__':
    # Ejecutar en modo debug localmente
    app.run(debug=True, port=5000)

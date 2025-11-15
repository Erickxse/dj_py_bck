from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviarCorreo(email, otp):
    subject = "Creación de cuenta Artex"
    plain_text = f"Your OTP code is {otp}"

    html_message = f"""
    <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <img src="https://artex.ec/images/upload/126/med/5a53dae5c7a732.08916532.jpeg" alt="Artex Logo" style="width: 400px; margin-top: 50px;">
            <hr style="max-width: 600px; height: 5px; background-color: #000000; border: none;"></hr>
            <div style="max-width: 700px; margin: auto; padding: 35px;">
                <div style="margin: 35px;">
                    <p style="color:rgb(0, 0, 0); font-size: 24px">Hemos recibido una solicitud para crear tu cuenta de Artex, a través del correo <span style="color: #000000; font-weight: bold;">{email} </span></p>
                    <p style="font-size: 18px;color: #000000; margin-top: 50px; "><strong>Tu código de verificacion es:</strong> </p>
                    <p style="font-size: 36px; font-weight: bold; color: #000000; margin-top: -5px; margin-bottom: 50px;">{otp}</p>
                    <p style="font-size: 20px; color: black; font-weight: bold; margin-bottom: 60px; ">El código es de un solo uso, no lo compartas, ni reenvíes este correo a terceros.</p>
                </div>
                <div style="max-width: 700px; margin: auto; padding: 45px; background-color: #000000; ">
                    <p style="font-size: 20px; color: white;">Este correo ha sido enviado a {email} para finalizar el proceso de creación de su cuenta en Artex</p>
                    <center>
                        <p style="font-size: 18px; color: white; font-weight: bold;">© ARTEX 2025</p>
                        <a href="#" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">Términos y condiciones</a>
                    </center>
                </div>
            </div>
        </body>
    </html>
    """

    enviar_email_sendgrid(
        subject=subject,
        to_email=email,
        plain_text=plain_text,
        html_content=html_message
    )


def enviarCorreoResetPass(email, otp):
    subject = "Recuperación de contraseña en Artex"
    plain_text = f"Your OTP code is {otp}"

    html_message = f"""
    <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <img src="https://artex.ec/images/upload/126/med/5a53dae5c7a732.08916532.jpeg" alt="Artex Logo" style="width: 400px; margin-top: 50px;">
            <hr style="max-width: 600px; height: 5px; background-color: #000000; border: none;"></hr>
            <div style="max-width: 700px; margin: auto; padding: 35px;">
                <div style="margin: 35px;">
                    <p style="color:rgb(0, 0, 0); font-size: 24px">Hemos recibido una solicitud para recuperación de contraseña en Artex, a través del correo <span style="color: #000000; font-weight: bold;">{email} </span></p>
                    <p style="font-size: 18px;color: #000000; margin-top: 50px; "><strong>Tu código de verificacion es:</strong> </p>
                    <p style="font-size: 36px; font-weight: bold; color: #000000; margin-top: -5px; margin-bottom: 50px;">{otp}</p>
                    <p style="font-size: 20px; color: black; font-weight: bold; margin-bottom: 60px; ">El código es de un solo uso, no lo compartas, ni reenvíes este correo a terceros.</p>
                </div>
                <div style="max-width: 700px; margin: auto; padding: 45px; background-color: #000000; ">
                    <p style="font-size: 20px; color: white;">Este correo ha sido enviado a {email} para finalizar el proceso de recuperación de contraseña en Artex</p>
                    <center>
                        <p style="font-size: 18px; color: white; font-weight: bold;">© ARTEX 2025</p>
                        <a href="#" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">Términos y condiciones</a>
                    </center>
                </div>
            </div>
        </body>
    </html>
    """

    enviar_email_sendgrid(
        subject=subject,
        to_email=email,
        plain_text=plain_text,
        html_content=html_message
    )


def enviar_email_sendgrid(subject, to_email, plain_text, html_content):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=plain_text,
        html_content=html_content
    )



    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email enviado: Status {response.status_code}")
        print(response.body)
        print(response.headers)
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error enviando email con SendGrid: {e}")

def enviarCorreoNotificacionCotizacion(dest_email, datos_quote):
    subject = "Nueva cotización recibida en Artex"

    plain_text = (
        f"Has recibido una nueva cotización de {datos_quote['quoted_by']}.\n"
        f"Email: {datos_quote['quote_email']}\n"
        f"Teléfono: {datos_quote['quote_phone']}\n"
        f"Cantidad: {datos_quote['service_product_no_of_items']}\n"
        f"Notas: {datos_quote['quote_notes']}"
    )

    html_content = f"""
    <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <img src="https://artex.ec/images/upload/126/med/5a53dae5c7a732.08916532.jpeg" alt="Artex Logo" style="width: 400px; margin-top: 50px;">
            <hr style="max-width: 600px; height: 5px; background-color: #000000; border: none;">

            <div style="max-width: 700px; margin: auto; padding: 35px;">
                <div style="margin: 35px;">
                    <p style="color: rgb(0, 0, 0); font-size: 24px;">
                        Has recibido una <span style="color: #000000; font-weight: bold;">nueva cotización</span> en Artex
                    </p>
                    <p style="font-size: 18px; color: #000000; margin-top: 50px;"><strong>Detalles de la cotización:</strong></p>
                    
                    <table style="width: 100%; max-width: 600px; margin: 30px auto; border-collapse: collapse;">
                        <tr>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;"><strong>Nombre:</strong></td>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;">{datos_quote['quoted_by']}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;"><strong>Email:</strong></td>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;">{datos_quote['quote_email']}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;"><strong>Teléfono:</strong></td>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;">{datos_quote['quote_phone']}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;"><strong>Cantidad:</strong></td>
                            <td style="text-align: left; padding: 8px; border-bottom: 1px solid #ccc;">{datos_quote['service_product_no_of_items']}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left; padding: 8px;"><strong>Notas:</strong></td>
                            <td style="text-align: left; padding: 8px;">{datos_quote['quote_notes']}</td>
                        </tr>
                    </table>
                    
                    <p style="font-size: 20px; color: black; font-weight: bold; margin-top: 50px;">
                        Este correo es solo informativo. Por favor gestiona la cotización en tu panel de Artex.
                    </p>
                </div>
            </div>

            <div style="max-width: 700px; margin: auto; padding: 45px; background-color: #000000;">
                <p style="font-size: 20px; color: white;">Este correo ha sido enviado a {dest_email} para notificarte sobre una nueva cotización recibida.</p>
                <center>
                    <p style="font-size: 18px; color: white; font-weight: bold;">© ARTEX 2025</p>
                    <a href="#" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">Términos y condiciones</a>
                </center>
            </div>
        </body>
    </html>
    """


    enviar_email_sendgrid(
        subject=subject,
        to_email=dest_email,
        plain_text=plain_text,
        html_content=html_content
    )



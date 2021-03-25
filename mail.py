from os import getenv
from jinja2 import FileSystemLoader, Environment
from smtplib import SMTP
from email.mime.text import MIMEText


class Mailer:
    """
    This class contains methods to send an email with a template
    """

    def __init__(self, file_system_loader=FileSystemLoader, environment=Environment, mime_text=MIMEText, smtp=SMTP):
        """
        Constructor function

        :param file_system_loader: Loads templates from the file system
        :param environment: Jinja2 configurations
        :param mime_text: MIME document generator
        :param smtp: SMTP connection manager
        """
        self.file_system_loader = file_system_loader
        self.environment = environment
        self.mime_text = mime_text
        self.smtp = smtp

    def render_template(self, template_file: str, data: dict) -> str:
        """
        Function to render the template with data

        :param template_file: The relative-path to the Jinja2 template file
        :param data: The data to be populated
        :return: Template object
        """
        template_loader = self.file_system_loader(searchpath="./")
        output = self.environment(loader=template_loader, autoescape=True).get_template(template_file).render(data)
        return output

    def send_mail(self, receiver: str, subject: str, message: str):
        """
        Function to send an email

        :param receiver: The email address of the receiver
        :param subject: The subject line of the email
        :param message: The content of the email
        """
        mail_server = getenv('MAIL_SERVER', 'smtp.mailtrap.io')
        mail_port = getenv('MAIL_PORT', '2525')
        mail_default_sender = getenv('MAIL_DEFAULT_SENDER')
        mail_username = getenv('MAIL_USERNAME')
        mail_password = getenv('MAIL_PASSWORD')

        msg = self.mime_text(message, 'html')
        msg['Subject'] = subject
        msg['From'] = mail_default_sender
        msg['To'] = receiver

        # Send email
        with self.smtp(mail_server, mail_port) as server:
            server.login(mail_username, mail_password)
            server.sendmail(mail_default_sender, receiver, msg.as_string())
            del msg

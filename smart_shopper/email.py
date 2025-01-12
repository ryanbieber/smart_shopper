"""Base Email Class for the Smart Shopper"""

import sendgrid
from sendgrid.helpers.mail import To, Mail, Content, Email
import json


class EmailSender:
    def __init__(self, settings, from_email, to_email, subject, content=None, template=None, data=None):

        self.sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = Email(from_email)
        self.to_email = To(to_email)
        self.subject = subject

        if content:
            self.content = Content("text/html", content)
        elif template and data:
            self.content = self._build_from_template(template, data)
        else:
            raise ValueError("Either content or template and data must be provided")

        self.mail = Mail(self.from_email, self.to_email, self.subject, self.content)

    def _build_from_template(self, template, data):
        if template == "table":
            return self._build_table_template(data)
        raise ValueError(f"Unknown template: {template}")

    def _build_table_template(self, items):
        table_html = """<table border="1">
        <tr>
            <th>Name</th>
            <th>Discount</th>
            <th>Category</th>
        </tr>
        """
        for item in items:
            if isinstance(item, str):
                item = json.loads(item)
            table_html += f"<tr><td>{item['name']}</td><td>{item['discount']}</td><td>{item['category']}</td></tr>"
        table_html += "</table>"
        return Content("text/html", table_html)

    def send_email(self):
        return self.sg.client.mail.send.post(request_body=self.mail.get())

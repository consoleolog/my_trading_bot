import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from config import *


class SMTPModule:


    def write_email(self, subject, ticker, created, status, price, filepath: list, filename: list):
        return {
            'subject': f"{subject}",
            'html': f"""
            <table>
                <thead>
                    <tr>
                        <th style="width: 18.181818181818183%">일시</th>
                        <th style="width: 18.181818181818183%">종목</th>
                        <th style="width: 9.090909090909092%">매도/매매</th>
                        <th style="width: 27.27272727272727%">가격</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="text-align:center">{created}</td>
                        <td style="text-align:center">{ticker}</td>
                        <td style="text-align:center">{status}</td>
                        <td style="text-align:center">{price}</td>
                    </tr>
                </tbody>
            </table>
            """,
            'filepath': filepath,
            'filename': filename
        }

    def send_email(self, inputs):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = inputs["subject"]
        msg['From'] = SMTP_FROM
        msg['To'] = SMTP_TO
        html_content = f"""
        {inputs['html']}
        """
        part = MIMEText(html_content, "html")
        msg.attach(part)

        try:
            for index, filename in enumerate(inputs['filename']):
                with open(f"{os.getcwd()}/{inputs['filepath'][index]}", "rb") as f:
                    file = MIMEBase("application", "octet-stream")
                    file.set_payload(f.read())
                encoders.encode_base64(file)
                file.add_header("Content-Disposition", f"attachment; filename={filename}")
                msg.attach(file)
        except KeyError as key_error:
            pass

        s = smtplib.SMTP('smtp.naver.com', 587)
        s.starttls()  # TLS 보안 처리
        s.login(NAVER_ID, NAVER_PASSWORD)
        s.sendmail(SMTP_FROM, SMTP_TO, msg.as_string())
        s.close()

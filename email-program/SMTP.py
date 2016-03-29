'''
Created on Feb 20, 2016

@author: xuyi
'''
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

if __name__ == '__main__':
    # 输入Email地址和口令:
    from_addr = 'xuyithuss@126.com'
    password = '19940801xuyi'
    # 输入收件人地址:
    to_addr = 'xuyi556677@163.com'
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.163.com'
    smtp_port = 994
    
    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
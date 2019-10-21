# encoding : utf-8
# @Author  : Steven Xu
# @Email   ：youzi5201@163.com

import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  

sender = 'youzi5201@163.com'  
receiver = 'youzi5201@163.com'  
smtpserver = 'smtp.163.com'  
username = 'XXX'  
password = 'XXX'  

# 邮件主题  
mail_title = '主题：测试报告'  


# 读取html文件内容  
f = open('report_test.html', 'rb')  
mail_body = f.read()  
f.close()  


# 邮件内容, 格式, 编码  
message = MIMEText(mail_body, 'html', 'utf-8')  
message['From'] = sender  
message['To'] = receiver  
message['Subject'] = Header(mail_title, 'utf-8')  


try:  
    smtp = smtplib.SMTP()  
    smtp.connect('smtp.163.com')  
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, message.as_string())  
    print("发送邮件成功！！！")  
    smtp.quit()  
except smtplib.SMTPException:  
    print("发送邮件失败！！！") 

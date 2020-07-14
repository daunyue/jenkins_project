from HTMLTestRunner import HTMLTestRunner
import unittest
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import time
import os
from script.test_login import TestLogin

# 需求1 :整合自动发邮件功能，执行测试用例生成最新测试报告，取最新的测试报告，发送最新测试报告至邮箱。
# 需求2 :定时执行脚本，可以通过Jenkins工具，或者Windows系统自带的任务计划程序实现。


# 163邮箱
my_sender = 'd18600643930@163.com'  # 发件人邮箱账号
my_pass = 'KHZOSLBGBVJKTWTJ'  # 这里的密码为开启SMTP，生成的授权码
my_user = 'd18600643930@163.com'  # 收件人邮箱账号，我这边发送给自己


# 查找测试报告目录，找到最新生成的测试报告文件
def new_report(testreport):
    lists = os.listdir(testreport)
    # 重新按时间对目录下的文件进行排序
    lists.sort(key=lambda fn: os.path.getmtime(testreport + "\\" + fn))
    file_new = os.path.join(testreport, lists[-1])
    print(file_new)
    return file_new


def send_mail(file_new):
    ret = True
    try:
        f = open(file_new, "rb")
        mail_body = f.read()
        f.close()
        # 编写HTML类型邮件正文
        msg = MIMEText(mail_body, "html", "utf-8")
        msg["Subject"] = Header("自动化测试报告", "utf-8")
        msg['from'] = my_sender
        msg['to'] = my_user
        msg["date"] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
        # 163邮箱
        server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


if __name__ == "__main__":

    # 测试报告存放路径
    test_report = "C:\\Users\\admin\\Desktop\\自动化测试脚本\\web_bzb_01\\report"
    # 创建测试套件对象
    testunit = unittest.TestSuite()
    # 添加测试用例
    testunit.addTest(unittest.makeSuite(TestLogin))
    # 时间格式
    now = time.strftime("%Y-%m-%d_%H-%M", time.localtime(time.time()))
    # 指定测试报告路径
    # filename = "./report/8001_{}.html".format(now)
    filename = "C:/Users/admin/Desktop/自动化测试脚本/web_bzb_01/report/8001_{}.html".format(now)
    fp = open(filename, "wb")
    runner = HTMLTestRunner(stream=fp, title="标准版自动化测试报告", description="用例执行情况：")
    runner.run(testunit)
    fp.close()
    # 取最新测试报告
    new_report = new_report(test_report)
    # 发送邮件，发送最新测试报告html
    send_mail(new_report)
    ret = send_mail
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

import unittest
from BeautifulReport import BeautifulReport

if __name__ == '__main__':
    # "."表示当前目录，"D_.py"匹配当前目录下所有D*.py开头的用例
    suite_tests = unittest.defaultTestLoader.discover("./script", pattern="test_xzxmlr.py", top_level_dir=None)
    # log_path='.'把report放到当前目录下
    BeautifulReport(suite_tests).report(filename='标准版—8001测试报告', description='送审、审核流程测试', report_dir='report')

    # 指定测试报告路径
    # reprot_file = config.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))

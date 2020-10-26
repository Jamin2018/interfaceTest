import json
import unittest
from common.configHttp import RunMain
import paramunittest
import geturlParams
import urllib.parse
# import pythoncom
import readExcel
# pythoncom.CoInitialize()

url = geturlParams.geturlParams().get_Url()# 调用我们的geturlParams获取我们拼接的URL
login_xls = readExcel.readExcel().get_xls('userCase.xlsx', 'login')

@paramunittest.parametrized(*login_xls)
class testHyperx(unittest.TestCase):
    def setParameters(self, case_name, path, query, method, headers):
        """
        set params
        :param case_name:
        :param path
        :param query
        :param method
        :return:
        """
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)
        self.headers = json.loads(headers)

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        print(self.case_name+"测试开始前准备")

    def test01case(self):
        self.checkResult()

    def tearDown(self):
        print("测试结束，输出log完结\n\n")
        print('报错url：', self.path, "\n\n")

    def checkResult(self):# 断言
        """
        check test result
        :return:
        """


        url1 = "?"
        new_url = url1 + self.query
        data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))# 将一个完整的URL中的name=&pwd=转换为{'name':'xxx','pwd':'bbb'}

        url = self.path
        if self.method == 'get':
            url = self.path + "?" + self.query

        info = RunMain().run_main(self.method, url, data1, self.headers)# 根据Excel中的method调用run_main来进行requests请求，并拿到响应
        if self.case_name == 'listZone' or self.case_name == 'listDiskState' or self.case_name == 'listZoneStatisticalData' or self.case_name == 'listZoneStatisticalDetailedDat':# 如果case_name是login，说明合法，返回的code应该为200
            if info.status_code != 200:
                assert False

        else:
            ss = json.loads(info)# 将响应转换为字典格式

            if self.case_name == 'login_error':# 同上
                self.assertEqual(ss['code'], -1)
            if self.case_name == 'login_null':# 同上
                self.assertEqual(ss['code'], 10001)

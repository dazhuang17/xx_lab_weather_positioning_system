from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
import serial.tools.list_ports
import os
import handle
import time
import work
import threading
import global_var


class Stats:

    def __init__(self):
        """
        从文件中加载UI定义
        从 UI 定义中动态 创建一个相应的窗口对象
        注意：里面的控件对象也成为窗口对象的属性了
        比如 self.ui.button , self.ui.textEdit
        可以在envs\envs_name\Lib\site-packages\PySide2文件下能找到designer.exe可执行文件
        """

        self.ui = QUiLoader().load('cn_sea.ui')
        self.ui.me_test.clicked.connect(self.me_test)
        self.ui.beidou_test.clicked.connect(self.bd_test)
        self.ui.refresh_com.clicked.connect(self.getcom)
        self.ui.sql_test.clicked.connect(self.qsl_test)
        self.ui.start.clicked.connect(self.showtime)
        self.ui.stop.clicked.connect(self.stop)
        self.ui.m_com.currentIndexChanged.connect(self.me_current_com)
        self.ui.b_com.currentIndexChanged.connect(self.bd_current_com)
        self.ui.fre.returnPressed.connect(self.get_fre)

        self.config_info()
        able = threading.Thread(target=self.flag)
        able.start()

    def config_info(self):
        self.ui.config_info.append('数据库配置信息：')
        self.ui.config_info.append('host： localhost')
        self.ui.config_info.append('user： root')
        self.ui.config_info.append('password： 123456')
        self.ui.config_info.append('db： cn_sea_data')
        self.ui.config_info.append('port： 3306')
        self.ui.config_info.append('================')
        self.ui.fre.setPlaceholderText(global_var.get_value('fre'))

    # 状态监测
    def flag(self):
        while True:
            if global_var.get_value('m_test_flag') == '失败':
                self.ui.textBrowser.append(global_var.get_value('m_com') + ' 通信失败!')
                self.ui.textBrowser.append('================')
                global_var.set_value('m_test_flag', '0')

            if global_var.get_value('b_test_flag') == '失败':
                self.ui.textBrowser.append(global_var.get_value('b_com') + ' 通信失败!')
                self.ui.textBrowser.append('================')
                global_var.set_value('b_test_flag', '0')

            if global_var.get_value('m_com_ok') == '1':
                self.ui.textBrowser.append(global_var.get_value('m_com') + ' 通信成功!')
                self.ui.textBrowser.append('================')
                self.ui.config_info.append('气象串口： ' + global_var.get_value('m_com'))
                self.ui.config_info.append('================')
                global_var.set_value('m_com_ok', 'ok')

            if global_var.get_value('m_com_ok') == 'ok':
                self.ui.me_test.setEnabled(False)

            if global_var.get_value('b_com_ok') == '1':
                self.ui.textBrowser.append(global_var.get_value('b_com') + ' 通信成功!')
                self.ui.textBrowser.append('================')
                if global_var.get_value('bd_com_ok') == '0':
                    self.ui.config_info.append('北斗串口： ' + global_var.get_value('b_com'))
                    self.ui.config_info.append('================')
                    global_var.set_value('bd_com_ok', '1')
                global_var.set_value('b_com_ok', 'ok')

            if global_var.get_value('b_com_ok') == 'ok' :
                if global_var.get_value('b_data') == '定位失败':
                    self.ui.textBrowser.append('北斗定位失败')
                    self.ui.textBrowser.append('================')
                    global_var.set_value('b_data', '0')
                if global_var.get_value('b_data') == 'ok':
                    self.ui.textBrowser.append('北斗定位成功')
                    self.ui.textBrowser.append('================')
                    self.ui.beidou_test.setEnabled(False)
                    global_var.set_value('b_data', '准备好了！')

            if global_var.get_value('start_data') == 'ok':
                self.ui.beidou_test.setEnabled(False)
                self.ui.me_test.setEnabled(False)
                self.ui.sql_test.setEnabled(False)
                self.ui.refresh_com.setEnabled(False)

            if global_var.get_value('start_data') == '终止':
                self.ui.beidou_test.setEnabled(True)
                self.ui.me_test.setEnabled(True)
                self.ui.sql_test.setEnabled(True)
                self.ui.refresh_com.setEnabled(True)

            if global_var.get_value('sql_test') == '1':
                time.sleep(1)
                if global_var.get_value('db') != '连接成功':
                    global_var.set_value('sql_test', '0')
                    self.ui.textBrowser.append('数据库连接失败！请确认地址、用户、密码后重新连接！')
                    self.ui.textBrowser.append('================')
                if global_var.get_value('sql_com') != '连接成功':
                    global_var.set_value('sql_test', '0')
                    print(global_var.get_value('sql_com'))
                    self.ui.textBrowser.append('串口连接失败！请确认串口选择正确！')
                    self.ui.textBrowser.append('================')
                    work.com_close()
                if global_var.get_value('sql_tx') != '连接成功':
                    global_var.set_value('sql_test', '0')
                    self.ui.textBrowser.append('串口发送失败！请确认串口！')
                    self.ui.textBrowser.append('================')
                    work.com_close()
                if global_var.get_value('sql_rx') != '连接成功':
                    global_var.set_value('sql_test', '0')
                    self.ui.textBrowser.append('串口解码失败！请确认串口！')
                    self.ui.textBrowser.append('================')
                    work.com_close()
                if global_var.get_value('sql_save') != '连接成功':
                    global_var.set_value('sql_test', '0')
                    self.ui.textBrowser.append('写入数据库失败！请确认数据库配置！')
                    self.ui.textBrowser.append('================')
                    work.com_close()

            self.ui.date.setText(global_var.get_value('date'))
            self.ui.time.setText(global_var.get_value('time'))
            self.ui.tem_label.setText(global_var.get_value('temperature'))
            self.ui.hum_label.setText(global_var.get_value('humidity'))
            self.ui.lat_label.setText(global_var.get_value('latitude'))
            self.ui.lon_label.setText(global_var.get_value('longitude'))

            time.sleep(1)

    def get_fre(self):
        global_var.set_value('fre', self.ui.fre.text())
        self.ui.config_info.append(global_var.get_value('fre'))

    # 获取正确串口号
    def me_current_com(self):
        if global_var.get_value('m_com_ok') == '0':
            me_com = self.ui.m_com.currentText()
            global_var.set_value('me_com', me_com)
            t_com = threading.Thread(target=handle.handle_me_com)
            t_com.start()

    def bd_current_com(self):
        if global_var.get_value('b_com_ok') == '0':
            bd_com = self.ui.b_com.currentText()
            global_var.set_value('bd_com', bd_com)
            b_com = threading.Thread(target=handle.handle_bd_com)
            b_com.start()

    # 获取串口进程
    def getcom(self):
        com = threading.Thread(target=self.com)
        com.start()

    # 更新串口
    def com(self):
        self.ui.m_com.clear()
        self.ui.b_com.clear()
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            self.ui.m_com.addItem("无串口设备。")
            self.ui.b_com.addItem("无串口设备。")
        else:
            for comport in ports_list:
                self.ui.m_com.addItem(list(comport)[1])
                self.ui.b_com.addItem(list(comport)[1])

    # 气象串口测试进程
    def me_test(self):
        self.ui.textBrowser.append('气象串口测试...')
        self.ui.textBrowser.append('等待测试结果...')
        me_test = threading.Thread(target=handle.meteorological_test)
        me_test.start()

    # 定位串口测试进程
    def bd_test(self):
        self.ui.textBrowser.append('北斗定位串口测试...')
        self.ui.textBrowser.append('等待测试结果...')
        bd_test = threading.Thread(target=handle.beidou_test)
        bd_test.start()

    # 数据库连接测试
    def qsl_test(self):
        global_var.set_value('sql_test', '1')
        self.ui.textBrowser.append('数据库连接...')
        global_var.set_value('db_start', '开始连接')
        self.ui.textBrowser.append(global_var.get_value('db_start') + '...')
        work.connect_sql()
        global_var.set_value('db', '连接成功')
        self.ui.textBrowser.append('数据库连接成功!')
        self.ui.textBrowser.append('连接串口，向设备发送问询码...')
        work.connect_com()
        global_var.set_value('sql_com', '连接成功')
        work.com_tx()
        global_var.set_value('sql_tx', '连接成功')
        self.ui.textBrowser.append('发送成功！')
        self.ui.textBrowser.append('接收设备响应码...')
        work.com_rx()
        global_var.set_value('sql_rx', '连接成功')
        self.ui.textBrowser.append('接收成功，解析数据...')
        self.ui.textBrowser.append('写入数据库...')
        work.save_Sql()
        global_var.set_value('sql_save', '连接成功')
        self.ui.textBrowser.append('写入成功！')
        self.ui.textBrowser.append('================')
        global_var.set_value('sql_test', '0')
        work.com_close()

    # 采集数据
    def showtime(self):
        global_var.set_value('sql_test', '0')
        if global_var.get_value('com_open') == '需重新打开':
            global_var.set_value('com_open', '重新打开')
        global_var.set_value('start_data', '1')
        if global_var.get_value('config_info') == '0':
            self.ui.config_info.clear()
            self.ui.config_info.append('数据库配置信息：')
            self.ui.config_info.append('host： localhost')
            self.ui.config_info.append('user： root')
            self.ui.config_info.append('password： 123456')
            self.ui.config_info.append('db： cn_sea_data')
            self.ui.config_info.append('port： 3306')
            self.ui.config_info.append('================')
            self.ui.config_info.append('气象串口： ' + global_var.get_value('m_com'))
            self.ui.config_info.append('================')
            self.ui.config_info.append('北斗串口： ' + global_var.get_value('b_com'))
            self.ui.config_info.append('================')
            self.ui.config_info.append('采集频率： ' + global_var.get_value('fre') + '次/秒')
            self.ui.config_info.append('================')
            global_var.set_value('config_info', '1')
        true_work = threading.Thread(target=work.work)
        # true_work.setDaemon(True)
        true_work.start()

    def stop(self):
        global_var.set_value('start_data', '终止')
        global_var.set_value('com_open', '需重新打开')
        work.com_close()


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('private.png'))
    global_var._init()
    stats = Stats()
    stats.ui.show()
    app.exec_()
    # sys.exit(app.exec_())
    os._exit(0)
    # sys.exit(0)

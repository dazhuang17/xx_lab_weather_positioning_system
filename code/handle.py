import serial.tools.list_ports
import time
import global_var


def handle_me_com():
    ports_list = list(serial.tools.list_ports.comports())
    for comport in ports_list:
        if global_var.get_value('me_com') == list(comport)[1]:
            global_var.set_value('m_com', list(comport)[0])
        else:
            continue


def handle_bd_com():
    ports_list = list(serial.tools.list_ports.comports())
    for comport in ports_list:
        if global_var.get_value('bd_com') == list(comport)[1]:
            global_var.set_value('b_com', list(comport)[0])
        else:
            continue


def beidou_test():   # 发送函数
    beidou_GPS = serial.Serial(global_var.get_value('b_com'), 9600, timeout=1)
    beidou_tx = bytes([0X01, 0X03, 0X00, 0X05, 0X00, 0X23, 0X14, 0X12])    # 需要发送的十六进制数据
    beidou_GPS.write(beidou_tx)    # 用write函数向串口发送数据
    time.sleep(1)
    if beidou_GPS.inWaiting() > 72:  # 当接收缓冲区中的数据不为零时，执行下面的代码
        beidou_rx = beidou_GPS.read(72)     # 提取接收缓冲区中的前12个字节数
        beidou_rx = str(beidou_rx)[11:80]
        if global_var.get_value('b_data') == '0':
            if beidou_rx[0] == '$':
                global_var.set_value('b_com_ok', '1')
                if beidou_rx[17] == 'A':
                    global_var.set_value('b_data', 'ok')
                else:
                    global_var.set_value('b_data', '定位失败')
            else:
                global_var.set_value('b_test_flag', '失败')
        else:
            if beidou_rx[17] == 'A':
                global_var.set_value('b_data', 'ok')
    else:
        global_var.set_value('b_test_flag', '失败')


def meteorological_test():   # 发送函数
    meteorological_tx = bytes([0X01, 0X03, 0X00, 0X00, 0X00, 0X02, 0XC4, 0X0B])
    meteorological_collection = serial.Serial(global_var.get_value('m_com'), 9600, timeout=1)
    meteorological_collection.write(meteorological_tx)
    time.sleep(1)
    if meteorological_collection.inWaiting() > 0:  # 当接收缓冲区中的数据不为零时，执行下面的代码
        meteorological_rx = meteorological_collection.read(9)     # 提取接收缓冲区中的前12个字节数
        meteorological_rx = ''.join(map(lambda x: ('/x' if len(hex(x)) >= 4 else '/x0')+hex(x)[2:], meteorological_rx))
        meteorological_rx = meteorological_rx[2:].split('/x')
        # print(meteorological_rx)
        if meteorological_rx[4] != '00':
            global_var.set_value('m_com_ok', '1')
        else:
            global_var.set_value('m_test_flag', '失败')
    else:
        global_var.set_value('m_test_flag', '失败')

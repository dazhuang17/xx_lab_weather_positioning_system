import pymysql
import serial
import time
import serial.tools.list_ports
import global_var



# 数据处理
def handle_data(beidou_data, meteorological_data):
    if beidou_data[0] == '$' and beidou_data[17] == 'A':
        global_var.set_value('date', c_date(beidou_data[58:]))       # 日期
        global_var.set_value('time', c_time(beidou_data[7:16]))      # 时间
        global_var.set_value('latitude', c_latitude(beidou_data[19:31]))       # 纬度
        global_var.set_value('longitude', c_longitude(beidou_data[32:45]))       # 经度
    else:
        global_var.set_value('date', 'error')       # 日期
        global_var.set_value('time', 'error')      # 时间
        global_var.set_value('latitude', 'error')       # 纬度
        global_var.set_value('longitude', 'error')      # 经度

    if len(meteorological_data) == 9:
        global_var.set_value('temperature', c_temperature(meteorological_data))       # 温度
        global_var.set_value('humidity', c_humidity(meteorological_data))       # 湿度
    else:
        global_var.set_value('temperature', 'error')
        global_var.set_value('humidity', 'error')

    # print('日期：', "%s" % global_var.get_value('date'))
    # print('时间：', "%s" % global_var.get_value('time'))
    # print('温度：', "%s" % global_var.get_value('temperature'))
    # print('湿度：', "%s" % global_var.get_value('humidity'))
    # print('纬度：', "%s" % global_var.get_value('latitude'))
    # print('经度：', "%s" % global_var.get_value('longitude'))
    # print(' ')

    save_Sql()


# 日期计算
def c_date(date):
    return str('20' + date[4:6] + '-' + date[2:4] + '-' + date[:2])


# 时间计算
def c_time(tim):
    h = str(int(tim[0:2]) + 8)
    return str(h + ':' + tim[2:4] + ':' + tim[4:6])
    # return str(h + ':' + time[2:4] + ':' + time[4:6] + ':' + time[7:])


# 温度计算
def c_temperature(tem):
    tem_bin = [128, 64, 32, 16, 8, 4, 2, 1]

    if tem[5][0] == 'F' or tem[5][0] == 'f':
        result = 0
        a = bin(int(tem[6], 16))
        a = a[2:].replace('1', '2')
        a = a.replace('0', '1')
        a = a.replace('2', '0')
        for x in range(len(a)):
            if a[x] == '1':
                result += tem_bin[x]
            else:
                continue
        result += 1

        return "%.1f" % float(int(result) * 0.1) + ' °C'
    else:
        return "%.1f" % float(int(tem[5]+tem[6], 16) * 0.1) + ' °C'


# 湿度计算
def c_humidity(hum):
    return "%.1f" % float(int(hum[3]+hum[4], 16) * 0.1) + ' %RH'


# 纬度计算
def c_latitude(lat):
    # print(lat)
    # print(float(lat[3:10]))
    # return float(float(lat[:2]) + float(lat[3:5]) / 60 + float(lat[6:10]) * 0.000001 / 60)
    # print(float(lat[:2]) + float(lat[2:10]) / 60)
    return "%0.5f" % (float(lat[:2]) + float(lat[2:10]) / 60) + ' ' + str(lat[-1])


# 经度计算
def c_longitude(long):
    # print(long)
    # print(long[3:11])
    return "%0.5f" % (float(long[:3]) + float(long[3:11]) / 60) + ' ' + str(long[-1])

def com_close():
    beidou_GPS.flushInput()
    meteorological_collection.flushInput()
    meteorological_collection.close()
    beidou_GPS.close()

def connect_com():
    global beidou_GPS
    global meteorological_collection
    global flag

    # if global_var.get_value('com_open') == '0':
    meteorological_collection = serial.Serial(global_var.get_value('m_com'), 9600, timeout=1)
    beidou_GPS = serial.Serial(global_var.get_value('b_com'), 9600, timeout=1)
    # if global_var.get_value('com_open') == '重新打开':
    #     meteorological_collection.close()
    #     beidou_GPS.close()
    #     meteorological_collection = serial.Serial(global_var.get_value('m_com'), 9600, timeout=1)
    #     beidou_GPS = serial.Serial(global_var.get_value('b_com'), 9600, timeout=1)
    if global_var.get_value('sql_test') == '0':
        global_var.set_value('start_data', 'ok')
        global_var.set_value('com_open', '已打开')
    # meteorological_collection = serial.Serial('com12', 9600, timeout=1)
    # beidou_GPS = serial.Serial('com11', 9600, timeout=1)

def com_tx():   # 发送函数

    global flag
    beidou_tx = bytes([0X01, 0X03, 0X00, 0X05, 0X00, 0X23, 0X14, 0X12])    # 需要发送的十六进制数据
    meteorological_tx = bytes([0X01, 0X03, 0X00, 0X00, 0X00, 0X02, 0XC4, 0X0B])
    beidou_GPS.write(beidou_tx)    # 用write函数向串口发送数据
    meteorological_collection.write(meteorological_tx)
    if global_var.get_value('sql_test') == '0':
        flag = 1

def com_rx():
    if beidou_GPS.inWaiting() > 72 & meteorological_collection.inWaiting() > 0:  # 当接收缓冲区中的数据不为零时，执行下面的代码
        beidou_rx = beidou_GPS.read(72)     # 提取接收缓冲区中的前12个字节数
        meteorological_rx = meteorological_collection.read(9)
        meteorological_rx = ''.join(map(lambda x: ('/x' if len(hex(x)) >= 4 else '/x0')+hex(x)[2:], meteorological_rx))
        meteorological_rx = meteorological_rx[2:].split('/x')   # 由于datas变量中的数据前两个是/x，所以用到切片工具
        beidou_rx = str(beidou_rx)[11:80]
        if global_var.get_value('sql_test') == '0':
            handle_data(beidou_rx, meteorological_rx)


def connect_sql():
    global cursor
    global db
    # 打开数据库连接
    db = pymysql.connect(host='localhost', user='root', password='123456', db='cn_sea_data', port=3306, )
    # 使用sursor()方法创建一个游标对象cursor
    cursor = db.cursor()

# 保存至数据库
def save_Sql():
    global flag
    if global_var.get_value('sql_test') == '1':
        cursor.execute('insert into data (date,time,temperature,humidity,latitude,longitude) values (%s,%s,%s,%s,%s,%s)',
                       ('测试数据', '测试数据', '测试数据', '测试数据', '测试数据', '测试数据')
                       )

    if global_var.get_value('sql_test') == '0':
        cursor.execute('insert into data (date,time,temperature,humidity,latitude,longitude) values (%s,%s,%s,%s,%s,%s)',
                       (global_var.get_value('date'), global_var.get_value('time'), global_var.get_value('temperature'),
                        global_var.get_value('humidity'), global_var.get_value('latitude'), global_var.get_value('longitude'))
                       )

    db.commit()
    beidou_GPS.flushInput()
    meteorological_collection.flushInput()
    flag = 0


def work():
    global flag
    connect_sql()
    sleep_time = global_var.get_value('fre')
    while True:
        if global_var.get_value('start_data') != '终止':

            if global_var.get_value('com_open') == '0' or global_var.get_value('com_open') == '重新打开':
                connect_com()

            com_tx()
            time.sleep(1)
            if flag == 1:
                com_rx()
            time.sleep(int(sleep_time) - 1)


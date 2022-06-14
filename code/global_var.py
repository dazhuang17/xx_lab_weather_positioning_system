# -*- coding: utf-8 -*-

def _init():  # 初始化
    global _global_dict
    _global_dict = {}
    dict_init()


def set_value(key, value):
    #定义一个全局变量
    _global_dict[key] = value


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except:
        return _global_dict['error']


def dict_init():
    _global_dict['error'] = '未找到目标'
    _global_dict['m_test_flag'] = '0'
    _global_dict['b_test_flag'] = '0'
    _global_dict['b_com_ok'] = '0'
    _global_dict['m_com_ok'] = '0'
    _global_dict['b_data'] = '0'
    _global_dict['bd_com_ok'] = '0'
    _global_dict['config_info'] = '0'
    _global_dict['com_open'] = '0'
    _global_dict['fre'] = '3'

    _global_dict['date'] = '日期'
    _global_dict['time'] = '时间'
    _global_dict['temperature'] = '0'
    _global_dict['humidity'] = '0'
    _global_dict['latitude'] = '0'
    _global_dict['longitude'] = '0'

    # _global_dict['db_start'] = '0'
    # _global_dict['sql_test'] = '0'
    # _global_dict['bd_com'] = '0'
    # _global_dict['me_com'] = '0'

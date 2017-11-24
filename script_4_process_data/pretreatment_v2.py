# -*- coding:utf-8 -*-
import re

ch_int_re = r'[零一二三四五六七八九十](?=\s*[万亿TtGg个期])|^[零一二三四五六七八九十]'
ch_int_dict = {
    '零': '0',
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
}
unit_dict = {
    '元': 1,
    '万': 10000,
    '亿': 100000000,
}


def multi_problem(opt, unit):
    '''
    :param opt:
    :param unit:
    :return: 去除所有未涉及、未采用等
    '''

    match_option = re.search(r'(.+\*\*)未.+\*\*$|(.+\*\*)没有.+\*\*$', opt)
    if match_option:
        return match_option.group(1) if match_option.group(1) else match_option.group(2)
    else:
        return opt


def int_problem(opt, unit):
    """
    整数的合理化处理
    :param opt:
    :param unit:
    :return: 返回的是字符型
    """

    match_int = re.search('[\d]+\.*[\d]*', opt)
    match_int_comma = re.search('([\d]+,*)+\.*[\d]*', opt)
    match_chi_int = re.search(ch_int_re, opt)
    match_unit = re.search('[万亿]', opt)
    if match_int_comma:
        opt = match_int_comma.group()
        opt = ''.join(opt.split(','))
    elif match_int:  # there is a int in it, just extract the first one
        opt = match_int.group()
    elif match_chi_int:  # there is a Chinese int in it
        opt = ch_int_dict[match_chi_int.group()]
    else:  # there is not any int in it
        return '0'
    if match_unit:  # there is a unit with it
        opt = float(opt) * unit_dict[match_unit.group()]
    opt = str(int(float(opt)))
    return opt


def float_problem(opt, unit):
    """
    小数的预处理
    :param opt:
    :param unit:
    :return: 无单位的字符串结果
    eg.'d3.3f' to '3.30'
        otherwise '0.00'
    """
    match_float = re.search('\d+\.*\d*', opt)
    match_float_comma = re.search('(\d+,)+\d+\.*\d*', opt)
    match_chi_int = re.search(ch_int_re, opt)
    match_unit = re.search('[万亿元TtGg]', opt)
    if match_float_comma:  # there is a int in it, just extract the first one
        opt = match_float_comma.group()
        opt = ''.join(opt.split(','))
    elif match_float:
        opt = match_float.group()
        match_dot = re.search('\.+', opt)
        if match_dot:
            opt = opt.replace(match_dot.group(), '.')
    elif match_chi_int:  # there is a Chinese int in it
        opt = ch_int_dict[match_chi_int.group()]
    else:  # there is not any int in it
        return '0.00'
    opt = float(opt)

    if match_unit:  # there is a unit with it
        unit_match = match_unit.group()
        if unit_match in ['g', 'G']:
            opt = opt / 1024
        elif unit_match in unit_dict:
            if unit == '':
                opt = opt * unit_dict[match_unit.group()]
            else:
                opt = opt * unit_dict[match_unit.group()] / unit_dict[unit]
    elif opt > 1000000:
        if unit != '':
            opt = opt / 10000

    if unit in unit_dict:
        opt = opt * unit_dict[unit]

    """
        单位万 不允许超过100亿，单位T不允许超过1024
        这里是将异常数据进行了置零处理。
    """
    if unit == '万' and opt > 1000000:
        return '0.00'
    if unit == 'T' and opt > 1024:
        return '0.00'

    opt = '%.2f' % float(opt)

    return opt


def percent_problem(opt, unit):
    """
    百分比格式化
    :param opt:
    :param unit:
    :return: eg. '99.2%' to '99.20'
        '0' means '未涉及'
        else ''
    """
    if opt == '0':
        return '0'
    else:
        match_float = re.search('[\d]+\.*[\d]*', opt)
        if match_float:
            opt = float(match_float.group())
            if opt < 1.0:
                opt *= 100
            if opt > 100:
                return ''
            return '%.2f' % opt
        else:
            return ''


def order_problem(opt, unit):
    """
    序列相关的数字权重设置
    :param opt:
    :param unit:
    :return: eg. 'a b' to {'a':['stem', 5], 'b':['stem', 4]}
        otherwise ''
    """
    unit_dict = {}
    unit = unit.split(';')
    for u in unit:
        u = u.split(':')
        unit_dict[u[0]] = u[1]

    match_letter = re.findall('[A-Z]', opt.upper())
    if match_letter:
        opt = {}
        w = 5
        n = 0
        n_letter = len(match_letter)
        while w > 0 and n < n_letter:
            letter = match_letter[n]
            if letter in unit_dict:
                opt[match_letter[n]] = [unit_dict[match_letter[n]], w]
                w -= 1
            n += 1
        if len(opt) == 0:
            return ''
        else:
            return opt
    else:
        return ''


def time_problem(opt, unit):
    """
    时间相关的数据进行处理
    如201409处理成2014
    用0表示 未计划
    :param opt:
    :param unit:
    :return:
    """
    match_time = re.search('\d\d\d\d', opt)
    if match_time:
        time = match_time.group()
        if time.startswith('19') or time.startswith('20'):
            return time
        else:
            return '0'
    else:
        return '0'

def haveOrNot_problem(opt, unit):
    """
    将有无问题的结果设置为有或无
    :param opt:
    :param unit:
    :return: "有" or "无"
    """
    if opt:
        return "无"
    else:
        match_not = re.search('[无未]', opt)
        if match_not:
            return "无"
        else:
            return "有"


def get_option(flag, opt, unit=''):
    """
    将问卷结果分类预处理成可统计的结果。

    :param flag:
    :param opt:
    :param unit:
    :return:
    """
    flag_function = {
        '2': multi_problem,
        '3': int_problem,
        '4': float_problem,
        '5': percent_problem,
        '6': order_problem,
        '7': time_problem,
        '9': haveOrNot_problem
    }
    if flag in flag_function:
        return flag_function[flag](opt, unit)
    else:
        return opt

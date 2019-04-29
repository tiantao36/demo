#!/usr/bin/env python
#-*- coding:utf-8 -*-

import wmi
import pythoncom

def handler(ip,username,password,date_time):
    '''
    https://www.jianshu.com/p/b67af72f0e86
    :param ip:
    :param username:
    :param password:
    :param date_time:
    :return:
    '''
    try:
        data=date_time.strip().split()
        action_date="cmd.exe /c date {0} & time {1}".format(data[0],data[1])
        pythoncom.CoInitialize()
        print('win#@##########',action_date,ip,username,password,date_time)
        c = wmi.WMI(computer=ip,user=username, password=password)
        print('@@@@@@@@@@',c)
        process_id, date_result = c.Win32_Process.Create(CommandLine=action_date)
        print('@@@@@@@@@@',date_result)
        if date_result:
            return False
        else:
            return True

    except Exception as e:
        print(e)
        return False

#!/usr/bin/env python
#-*- coding:utf-8 -*-

from winrm.protocol import Protocol

def handler(ip,username,password):
    '''
     Get-Date -Format 'yyyy-M-d H:m:s'
	https://www.cnblogs.com/weloveshare/p/5753139.html
    https://www.jianshu.com/p/b67af72f0e86
    :param ip:
    :param username:
    :param password:
    :param date_time:
    :return:
    '''
    try:
        endpoint='http://{0}:5985/wsman'.format(ip)
        print('window#######@@@@@@',endpoint)
        p = Protocol(
            endpoint=endpoint,
            transport='ntlm',
            username=username,
            password=password,
            server_cert_validation='ignore')
        shell_id = p.open_shell()
        command_id = p.run_command(shell_id, 'echo %DATE:~-10% %time:~0,2%:%time:~3,2%:%time:~6,2%',())
        std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
        p.cleanup_command(shell_id, command_id)
        p.close_shell(shell_id)
        if status_code==0:
            data=std_out.decode().replace('/','-')
            return data
        return False
    except Exception:
        return False



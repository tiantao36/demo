#!/usr/bin/env python
#-*- coding:utf-8 -*-

from winrm.protocol import Protocol

def handler(ip,username,password,date_time):
    '''
    winrm set winrm/config/winrs @{MaxConcurrentUsers="100"}
    winrm set winrm/config/winrs @{MaxShellsPerUser="100"}
    https://www.jianshu.com/p/b67af72f0e86
    :param ip:
    :param username:
    :param password:
    :param date_time:
    :return:
    '''

    endpoint='http://{0}:5985/wsman'.format(ip)
    print('window#######@@@@@@',endpoint)
    p = Protocol(
        endpoint=endpoint,
        transport='ntlm',
        username=username,
        password=password,
        server_cert_validation='ignore')
    shell_id = p.open_shell()
    #echo %date:~0,4%-%date:~5,2%-%date:~8,2% %time:~0,2%:%time:~3,2%:%time:~6,2%
    #%date:~2,5%-%date:~8,2%-%date:~11,2% %time:~0,2%:%time:~3,2%:%time:~6,2%
    '''
    %date:~0,4% 表示从左向右指针向右偏0位，然后从指针偏移到的位置开始提取4位字符，结果是2014（年的值）
    %date:~5,2%  表示指针从左向右偏移5位，然后从偏移处开始提取2位字符，结果是03（月的值）
    %date:~8,2%  表示指针从左向右偏移8位，然后从偏移处开始提取2位字符，结果是01（日的值）
    %date:~5%    表示指针从左向右偏移5位，然后提取所有的值
    %date:~-5%   表示指针反方向偏移，从最右端开始，偏移5位，然后从指针处提取左边的所有数值。
   '''
    data = date_time.strip().split()
    print('@@@@@@@@@@@@@',data)
    action_date = "cmd.exe /c date {0} & time {1}".format(data[0], data[1])
    print(action_date)
    command_id = p.run_command(shell_id, action_date,())
    print(command_id)
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
    print('status_code',status_code)
    if status_code==0:
        try:
            p.cleanup_command(shell_id, command_id)
            p.close_shell(shell_id)
        except Exception as e:
            print(e)
        return True
    else:
        try:
            p.cleanup_command(shell_id, command_id)
            p.close_shell(shell_id)
        except Exception:
            pass
        return False

if __name__=="__main__":
    handler('192.168.180.49', 'Administrator', 'maitian123?','2033-10-03 08:20:03')

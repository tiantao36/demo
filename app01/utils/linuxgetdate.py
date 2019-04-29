#!/usr/bin/env python
#-*- coding:utf-8 -*-

import paramiko
def handler(ip,port,username,password):
    # 创建SSH对象
    try:
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('linux#######@@@@@@', ip, username, password)
        ssh.connect(hostname=ip, port=port, username=username, password=password,timeout=2)
        action='date +"%Y-%m-%d %H:%M:%S"'
        print('linux#######@@@@@@',action,ip,username,password)
        stdin, stdout, stderr = ssh.exec_command(action)
        stdout = stdout.read()
        stderr = stderr.read()
        if stderr:
            print('stder====>',stderr)
            ssh.close()
            return False
        elif stdout:
            print('stdout=====>',stdout)
            ssh.close()
            return stdout.decode().strip()
        else:
            ssh.close()
            return True
    except Exception:
        ssh.close()
        return False
'''
Copyright (c) 2025 by Albresky, All Rights Reserved. 

Author: Albresky albre02@outlook.com
Date: 2025-04-02 16:33:07
LastEditTime: 2025-04-02 18:12:26
FilePath: /system-monitor/src/config.py

Description: 
'''
import os

# 邮件配置
EMAIL_SENDER = None
EMAIL_PASSWORD = None
SMTP_SERVER = None
SMTP_PORT = None

with open('email.conf', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('EMAIL_SENDER'):
            EMAIL_SENDER = line.split('=')[1].strip()
        elif line.startswith('EMAIL_PASSWORD'):
            EMAIL_PASSWORD = line.split('=')[1].strip()
        elif line.startswith('SMTP_SERVER'):
            SMTP_SERVER = line.split('=')[1].strip()
        elif line.startswith('SMTP_PORT'):
            SMTP_PORT = int(line.split('=')[1].strip())

# 监控阈值 (%)
MEMORY_THRESHOLD = 95.0
CPU_THRESHOLD = 95.0

# 监控间隔 (秒)
MONITOR_INTERVAL = 10

# 用户联系人文件路径
CONTACTS_FILE = "/usr/tools/contacts.conf"
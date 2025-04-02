'''
Copyright (c) 2025 by Albresky, All Rights Reserved. 

Author: Albresky albre02@outlook.com
Date: 2025-04-02 16:36:56
LastEditTime: 2025-04-02 17:21:20
FilePath: /system-monitor/src/email_sender.py

Description: 
'''
import logging
import yagmail
import config
from process_finder import format_process_info

logger = logging.getLogger(__name__)

def get_user_email(username):
    """从contacts.conf文件中获取用户的电子邮件地址"""
    try:
        with open(config.CONTACTS_FILE, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                if line.strip() and ':' in line:
                    user, email = line.strip().split(':', 1)
                    if user.strip() == username:
                        return email.strip()
        
        logger.warning(f"找不到用户 {username} 的电子邮件地址")
        return None
    except Exception as e:
        logger.error(f"读取联系人文件时出错: {e}")
        return None

def send_notification_email(username, resource_type, processes):
    """发送资源使用警告邮件给特定用户"""
    user_email = get_user_email(username)
    if not user_email:
        logger.error(f"无法发送邮件：找不到用户 {username} 的邮箱地址")
        return False
        
    try:
        subject = f"系统资源警告: {resource_type.upper()} 使用过高"
        
        # 构建邮件内容
        resource_name = {
            'memory': '内存',
            'swap': '交换空间',
            'cpu': 'CPU'
        }.get(resource_type, resource_type)
        
        process_info = format_process_info(processes, resource_type)
        
        body = f"""尊敬的用户 {username}，

您的进程占用了大量系统【{resource_name}】资源，这可能会影响系统的整体性能。
系统检测到【{resource_name}】占用率已超过95%，您是该资源的主要消耗者。

以下是您的相关进程详情:

{process_info}

请考虑优化您的应用程序或减少资源密集型任务，以帮助改善系统的整体性能。

此致，
系统管理员
        """
        
        logger.info(f"准备发送邮件到 {user_email}")
        
        # 使用yagmail发送邮件
        # 配置腾讯企业邮箱
        yag = yagmail.SMTP(
            user=config.EMAIL_SENDER,
            password=config.EMAIL_PASSWORD,
            host="smtp.exmail.qq.com",
            port=465,
            smtp_ssl=True
        )
        
        # 发送邮件
        yag.send(
            to=user_email,
            subject=subject,
            contents=body
        )
        
        logger.info(f"邮件成功发送到 {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"发送邮件时出错: {e}", exc_info=True)
        return False
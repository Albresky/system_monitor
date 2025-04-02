'''
Copyright (c) 2025 by Albresky, All Rights Reserved. 

Author: Albresky albre02@outlook.com
Date: 2025-04-02 16:36:25
LastEditTime: 2025-04-02 17:26:12
FilePath: /system-monitor/src/monitor.py

Description: 
'''
import psutil
import time
import logging
from process_finder import find_highest_resource_user, get_user_processes
from email_sender import send_notification_email
import config

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   filename='/var/log/system-monitor.log')
logger = logging.getLogger(__name__)

def monitor_system_resources():
    """持续监控系统资源并在超过阈值时发送警报"""
    logger.info("开始系统资源监控")
    
    while True:
        try:
            # 获取系统资源使用情况
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            logger.info(f"当前资源使用: 内存={memory.percent}%, 交换={swap.percent}%, CPU={cpu_percent}%")
            
            # 检查是否有任何资源超过阈值
            if memory.percent >= config.MEMORY_THRESHOLD:
                logger.warning(f"内存使用率达到{memory.percent}%，超过阈值{config.MEMORY_THRESHOLD}%")

                logger.warning(f"检查交换空间使用率")
                if swap.percent >= config.MEMORY_THRESHOLD:
                    logger.warning(f"交换空间使用率达到{swap.percent}%，超过阈值{config.MEMORY_THRESHOLD}%")
                    handle_resource_alert('memory')
                    handle_resource_alert('swap')
                
            if cpu_percent >= config.CPU_THRESHOLD:
                logger.warning(f"CPU使用率达到{cpu_percent}%，超过阈值{config.CPU_THRESHOLD}%")
                handle_resource_alert('cpu')
            
            # 等待指定的监控间隔
            time.sleep(config.MONITOR_INTERVAL)
                
        except Exception as e:
            logger.error(f"监控过程中出错: {e}", exc_info=True)
            time.sleep(60)  # 出错后等待一分钟再继续
            
def handle_resource_alert(resource_type):
    """处理资源警报"""
    try:
        # 找出占用最多资源的用户
        username, processes = find_highest_resource_user(resource_type)
        if not username:
            logger.warning(f"无法确定占用{resource_type}资源最多的用户")
            return
            
        logger.info(f"用户 {username} 在 {resource_type} 资源上使用率最高")
        
        # 发送通知邮件
        result = send_notification_email(username, resource_type, processes)
        if result:
            logger.info(f"成功发送通知邮件给用户 {username}")
        else:
            logger.error(f"发送通知邮件给用户 {username} 失败")
    except Exception as e:
        logger.error(f"处理资源警报时出错: {e}", exc_info=True)

if __name__ == "__main__":
    monitor_system_resources()
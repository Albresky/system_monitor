import psutil
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def find_highest_resource_user(resource_type):
    """
    找出占用指定资源最多的用户及其进程
    
    参数:
        resource_type: 'memory', 'swap', 或 'cpu'
        
    返回:
        (username, processes): 用户名和该用户的进程列表
    """
    logger.info(f"查找占用{resource_type}最多的用户")
    user_resources = defaultdict(float)
    user_processes = defaultdict(list)
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            info = proc.info
            username = info.get('username')
            
            if not username:
                continue
                
            if resource_type == 'memory' or resource_type == 'swap':
                usage = info.get('memory_percent', 0)
            elif resource_type == 'cpu':
                usage = info.get('cpu_percent', 0)
            else:
                logger.error(f"不支持的资源类型: {resource_type}")
                continue
                
            user_resources[username] += usage
            user_processes[username].append(info)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.debug(f"获取进程信息时出错: {e}")
            continue
    
    if not user_resources:
        logger.warning("未找到任何用户的资源使用情况")
        return None, []
        
    # 找出资源使用最多的用户
    highest_user = max(user_resources, key=user_resources.get)
    processes = user_processes[highest_user]
    
    logger.info(f"用户{highest_user}占用{resource_type}最多，总使用率: {user_resources[highest_user]:.2f}%")
    
    # 对进程按资源使用率排序
    if resource_type == 'memory' or resource_type == 'swap':
        processes.sort(key=lambda p: p.get('memory_percent', 0), reverse=True)
    else:
        processes.sort(key=lambda p: p.get('cpu_percent', 0), reverse=True)
        
    return highest_user, processes

def get_user_processes(username, resource_type):
    """获取指定用户占用特定资源的所有进程"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            if proc.info['username'] == username:
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    # 按资源使用率排序
    if resource_type == 'memory' or resource_type == 'swap':
        processes.sort(key=lambda p: p.get('memory_percent', 0), reverse=True)
    else:
        processes.sort(key=lambda p: p.get('cpu_percent', 0), reverse=True)
        
    return processes

def format_process_info(processes, resource_type):
    """将进程信息格式化为可读的文本（仅显示前10个进程）"""
    formatted_info = []
    
    # 只处理前10个进程
    top_processes = processes[:10]
    
    for proc in top_processes:
        pid = proc.get('pid', 'N/A')
        name = proc.get('name', 'unknown')
        
        if resource_type == 'memory' or resource_type == 'swap':
            usage = proc.get('memory_percent', 0)
            formatted_info.append(f"PID: {pid}, 进程名称: {name}, {resource_type} 占用: {usage:.2f}%")
        else:
            usage = proc.get('cpu_percent', 0)
            formatted_info.append(f"PID: {pid}, 进程名称: {name}, CPU 使用: {usage:.2f}%")
    
    # 如果原进程列表超过10个，添加提示信息
    if len(processes) > 10:
        formatted_info.append(f"... 还有 {len(processes) - 10} 个进程未显示")
            
    return "\n".join(formatted_info)
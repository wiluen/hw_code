# 定义一个函数来提取时间列和日志级别列
def extract_time_and_level(log_file_path):
    # 打开日志文件
    with open(log_file_path, 'r') as file:
        # 逐行读取文件内容
        lines = file.readlines()
    
    # 初始化一个列表来存储提取的结果
    extracted_data = []
    
    # 遍历每一行
    for line in lines:
        # 去掉行尾的换行符并按列分割
        columns = line.strip().split()
        
        # 检查列数是否足够
        if len(columns) >= 6:
            # 提取时间列（第二列）和日志级别列（第五列）
            time = columns[1]
            level = columns[4]
            # 将提取的数据添加到结果列表中
            extracted_data.append((time, level))
    
    return extracted_data

# 指定日志文件路径
log_file_path = 'log.txt'

# 调用函数并打印结果
extracted_data = extract_time_and_level(log_file_path)
for item in extracted_data:
    print(f"Time: {item[0]}, Level: {item[1]}")



import csv
from datetime import datetime, timedelta
from collections import defaultdict

# 定义一个函数来统计多个时间窗口内不同日志级别的数量，并将结果写入 CSV 文件
def count_logs_in_multiple_time_windows(log_file_path, start_time_str, output_csv_path, time_window_minutes=1):
    # 将起始时间字符串转换为 datetime 对象
    start_time = datetime.strptime(start_time_str, '%H:%M:%S.%f')
    
    # 初始化一个字典来存储每个时间窗口的计数
    counts = defaultdict(lambda: {'I': 0, 'W': 0, 'E': 0})
    
    # 打开日志文件
    with open(log_file_path, 'r') as file:
        # 逐行读取文件内容
        lines = file.readlines()
    
    # 遍历每一行
    for line in lines:
        # 去掉行尾的换行符并按列分割
        columns = line.strip().split()
        
        # 检查列数是否足够
        if len(columns) >= 6:
            # 提取时间列（第二列）和日志级别列（第五列）
            time_str = columns[1]
            level = columns[4]
            
            # 将时间字符串转换为 datetime 对象
            time = datetime.strptime(time_str, '%H:%M:%S.%f')
            
            # 计算当前时间所在的窗口
            window_start = start_time + timedelta(minutes=(time.minute // time_window_minutes) * time_window_minutes)
            
            # 检查时间是否在某个窗口内
            if start_time <= time:
                # 根据日志级别更新计数器
                if level in counts[window_start]:
                    counts[window_start][level] += 1
    
    # 将结果写入 CSV 文件
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Time Window', 'I', 'W', 'E']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for window_start, levels in sorted(counts.items()):
            writer.writerow({
                'Time Window': window_start.strftime('%H:%M:%S'),
                'I': levels['I'],
                'W': levels['W'],
                'E': levels['E']
            })

# 指定日志文件路径和输出 CSV 文件路径
log_file_path = 'log.txt'
output_csv_path = 'log_counts.csv'
start_time_str = '19:35:16.016'

# 调用函数并生成 CSV 文件
count_logs_in_multiple_time_windows(log_file_path, start_time_str, output_csv_path)





import matplotlib.pyplot as plt
import csv

# 读取 CSV 文件并提取数据
time_windows = []
counts_I = []
counts_W = []
counts_E = []

with open('log_counts.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        time_windows.append(row['Time Window'])
        counts_I.append(int(row['I']))
        counts_W.append(int(row['W']))
        counts_E.append(int(row['E']))

# 绘制折线图
plt.figure(figsize=(10, 6))

# 绘制 I 级别的折线图
plt.plot(time_windows, counts_I, label='I', marker='o', linestyle='-')

# 绘制 W 级别的折线图
plt.plot(time_windows, counts_W, label='W', marker='o', linestyle='-')

# 绘制 E 级别的折线图
plt.plot(time_windows, counts_E, label='E', marker='o', linestyle='-')

# 添加标题和标签
plt.title('Log Level Counts per Time Window')
plt.xlabel('Time Window')
plt.ylabel('Count')
plt.xticks(rotation=45)  # 旋转 x 轴标签以便更好地显示
plt.legend(title='Log Level')

# 显示图形
plt.tight_layout()  # 调整布局
plt.show()

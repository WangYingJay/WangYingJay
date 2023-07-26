import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

def get_github_snk_data(username):
    url = f"https://api.github.com/users/{username}/events"

    response = requests.get(url)
    if response.status_code == 200:
        events = response.json()
        contributions = [0] * 365
        for event in events:
            if event["type"] == "PushEvent":
                date_str = event["created_at"][:10]
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                day_of_year = date.timetuple().tm_yday - 1  # tm_yday is 1-indexed
                contributions[day_of_year] += len(event["payload"]["commits"])
                print(contributions[day_of_year])
        return contributions
    else:
        print(f"Failed to fetch contributions for {username}")
        return []


def plot_snk_chart(data):
    # 创建一个6x53的矩阵来表示一周的贪吃蛇图
    snk_matrix = np.zeros((7, 53), dtype=int)

    # 将数据填充到贪吃蛇图矩阵中
    for item in data:
        x = item['x']
        y = item['y']
        count = item['count']
        level = item['level']
        snk_matrix[y, x] = count if count > 0 else level

    # 定义颜色映射表
    cmap = plt.get_cmap('viridis')

    # 绘制贪吃蛇图
    plt.imshow(snk_matrix, cmap=cmap, aspect='auto', interpolation='none')

    # 隐藏x轴和y轴刻度标签
    plt.xticks([])
    plt.yticks([])

    # 添加标题和颜色条
    plt.title("GitHub Contributions - Snake Chart")
    plt.colorbar(label="Contributions")

    # 显示图像
    plt.show()


def main():
    username = "WangYingJay"
    snk_data = get_github_snk_data(username)

    if snk_data:
      print(snk_data)
        # 在这里，你可以处理获取到的SVG数据，如保存到本地文件，显示图像等
        # 这里只是一个示例 打印出SVG数据
        # plot_snk_chart(snk_data)


if __name__ == "__main__":
    main()

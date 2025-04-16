import requests
import random
from datetime import datetime, timedelta

# API端点
login_url = "https://run.ecust.edu.cn/api/userLogin/"
run_url = "https://run.ecust.edu.cn/api/createLine/"
update_url = "https://run.ecust.edu.cn/api/updateRecord/"


def login_and_run():
    # 创建session对象以保持会话
    session = requests.Session()

    # 登录信息
    login_data = {
        "iphone": "你的手机号",
        "password": "你的密码"
    }

    # 发送登录请求
    login_response = session.post(login_url, json=login_data)

    # 检查登录是否成功
    if login_response.status_code == 200:
        login_result = login_response.json()
        if login_result["code"] == 1:  # 成功代码为1
            print("登录成功！")
            student_id = login_result["data"]["id"]  # 获取学生ID
            print(f"学生ID: {student_id}")

            # 记录开始时间
            start_time = datetime.now()
            start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"开始时间: {start_time_str}")

            # 跑步路线数据
            run_data = {
                "pass_point": [
                    {
                        "lat": 30.832999,
                        "lng": 121.509337,
                        "name": "单双杠练习场"
                    },
                    {
                        "lat": 30.827536,
                        "lng": 121.503933,
                        "name": "38"
                    },
                    {
                        "lat": 30.829844,
                        "lng": 121.507996,
                        "name": "体育馆主馆"
                    }
                ],
                "student_id": str(student_id)  # 确保student_id是字符串类型
            }

            # 发送跑步请求
            run_response = session.post(run_url, json=run_data)

            # 检查跑步请求是否成功
            if run_response.status_code == 200:
                run_result = run_response.json()
                if run_result["code"] == 1:  # 成功代码为1
                    record_id = run_result["data"]["record_id"]
                    print(f"跑步记录创建成功！Record ID: {record_id}")

                    # 生成随机的结束时间和运行时间
                    random_seconds = random.randint(15*60, 25*60)  # 转换为秒
                    end_time = start_time + timedelta(seconds=random_seconds)

                    print(f"模拟跑步时间: {random_seconds}秒")

                    # 更新记录
                    return update_record(session, student_id, record_id, start_time, end_time, random_seconds)
                else:
                    print(f"跑步记录创建失败: {run_result['message']}")
            else:
                print(f"跑步API请求失败，状态码: {run_response.status_code}")
        else:
            print(f"登录失败: {login_result['message']}")
    else:
        print(f"登录API请求失败，状态码: {login_response.status_code}")

    return None


def update_record(session, student_id, record_id, start_time, end_time, running_time):
    # 格式化时间字符串
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    print(f"开始时间: {start_time_str}")
    print(f"结束时间: {end_time_str}")
    print(f"运行时间: {running_time}秒")

    # 随机生成数据
    mileage = random.randint(2000, 3000)  # 2000-3000之间的随机数
    pace = random.randint(300, 400)  # 300-400之间的随机数
    step_count = int(mileage * 1.1)  # 步数大约是里程的1.1倍

    # 更新记录数据
    update_data = {
        "end_time": end_time_str,
        "mileage": mileage,
        "pace": pace,
        "pass_point": 3,
        "record_id": str(record_id),
        "running_time": running_time,
        "start_time": start_time_str,
        "step_count": step_count,
        "student_id": str(student_id)
    }

    # 发送更新请求
    update_response = session.post(update_url, json=update_data)

    # 检查更新是否成功
    if update_response.status_code == 200:
        update_result = update_response.json()
        if update_result["code"] == 1:  # 成功代码为1
            print("跑步记录更新成功！")
            print(f"里程: {mileage}米")
            print(f"配速: {pace}")
            print(f"步数: {step_count}")
            return record_id
        else:
            print(f"跑步记录更新失败: {update_result['message']}")
    else:
        print(f"更新API请求失败，状态码: {update_response.status_code}")

    return None


if __name__ == "__main__":
    record_id = login_and_run()
    if record_id:
        print(f"完整流程成功执行，record_id: {record_id}")
    else:
        print("流程执行失败")


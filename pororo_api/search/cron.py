import requests
import json
from datetime import datetime, timedelta
import os
import shutil  # 파일 복사 라이브러리

########################################## get_log batch ############################################
def get_log(date):
    # input값 입력
    collection_list = 'cpu,memory,traffic'
    # collection_list = 'cpu'
    pod_name = 'homepage'  # homepage or daitso
    log_type = 'metric'
    step_value = '60'
    save_db = 'true'
    start_date = date
    end_date = date

    # url = "http://211.62.204.12:9000/01_get_log"
    # url = "http://172.19.0.3:9000/01_get_log"
    url = "http://localhost:9000/01_get_log"

    # 1. avg 값 저장##########
    pod_calculation = 'avg'
    payload = {'collection_list': collection_list,
               'pod_name': pod_name,
               'log_type' : log_type,
               'pod_calculation': pod_calculation,
               'start_date': start_date,
               'end_date': end_date,
               'step_value': step_value,
               'save_db': save_db}
    response1 = requests.request("POST", url, data=payload)

    # 1. avg 값 저장##########
    pod_calculation = 'sum'
    payload = {'collection_list': collection_list,
               'pod_name': pod_name,
               'log_type': log_type,
               'pod_calculation': pod_calculation,
               'start_date': start_date,
               'end_date': end_date,
               'step_value': step_value,
               'save_db': save_db}
    response2 = requests.request("POST", url, data=payload)

    result_avg = response1.text
    result_avg = json.loads(result_avg)

    result_sum = response2.text
    result_sum = json.loads(result_sum)

    print("result_avg값", result_avg)
    print("result_sum값", result_sum)

# 데이터 수집 및 elk 적재 - 매일 00시 05분
def crontab_get_log_job():
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    # yesterday_date = (datetime.now() - timedelta(days = 1) + timedelta(hours = 9)).strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M:%S')
    # now_time = (datetime.now() + timedelta(hours = 9)).strftime('%H:%M:%S')

    print(now_time)
    get_log(yesterday_date)

########################################## analyze_batch ############################################
def send_mattermost(message):
    # url = "https://talk.digitalkds.co.kr/hooks/x9hzf1ukxjgy3yjwg5shdh7x6r"
    url = "https://dh.digitalkds.co.kr/hooks/oqqgp8pks7n6f8dxmefpm793ky"

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'text': message
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    print(res)

# 실시간 분석 - 매 분
def crontab_analyze_job():

    # if datetime.now().strftime("%S") == '20':
    # input값 입력
    collection_list = 'cpu,memory,traffic'
    pod_name = 'homepage'  # homepage or daitso
    model = 'cluster'

    # url = "http://211.62.204.12:9000/06_analyze"
    # url = "http://172.19.0.3:9000/06_analyze"
    url = "http://localhost:9000/06_analyze"

    payload = {'collection_list': collection_list,
               'pod_name': pod_name,
               'model': model
               }

    response = requests.request("POST", url, data=payload)
    result = json.loads(response.text)

    if result['result']['outlier'] == 1:
        cluster_message = result['result']['date_time'][:10] + ' ' + result['result']['date_time'][
                                                                     11:16] + '에 이상치가 감지되었습니다.'
        send_mattermost(cluster_message)
    # else:
    #     cluster_message = "감지 X"
    #     send_mattermost(cluster_message)

########################################## create_model batch ############################################

# 모델 배포 - 매주 월요일 00시 10분
def crontab_model_deploy_job():
    pod_name = 'homepage'
    log_type = 'metric'
    pod_calculation = 'sum'
    start_date = '2020-01-15'
    end_date = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")

    # url = "http://211.62.204.12:9000/05_build_model"
    url = "http://localhost:9000/05_build_model"

    payload = {'pod_name': pod_name,
               'log_type': log_type,
               'pod_calculation': pod_calculation,
               'start_date': start_date,
               'end_date': end_date
               }
    response = requests.request("POST", url, data=payload)
    result = json.loads(response.text)

    print(result)

# 모델 파일 이름 변경 - 매주 월요일 01시 00분 -------------------> batch를 두 번 해야 하는 문제 때문에 주석처리함.
def crontab_modify_model_name_job():
    pod_name = 'homepage'
    pod_calculation = 'sum'

    # folder = 'model/'
    folder = os.getcwd() + '/workspace/adamas-log/pororo_api/model/'
    model_name = pod_name + '_' + 'prd' + '_' + pod_calculation + '_' + 'anal'
    save_model_date = '_' + (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")

    manage_date_file_path = folder + model_name + save_model_date + '.pkl'
    analyze_file_path = folder + model_name + '.pkl'

    print(analyze_file_path)
    print(manage_date_file_path)
    print(os.path.isfile(manage_date_file_path))

    if os.path.isfile(manage_date_file_path): ####################### vm에서 실행
        print("file is in")
        if os.path.isfile(analyze_file_path): ########################## vm에서 실행
            os.remove(analyze_file_path) # analyze_model 파일 삭제
        shutil.copyfile(manage_date_file_path, analyze_file_path) ########################## vm에서 실행


    # while True:
    #     if os.path.isfile(manage_date_file_path): ####################### vm에서 실행
    #     # if os.path.isfile("../" + manage_date_file_path):  # 파일이 만들어질 때까지 while True로 실행
    #         print("file is in")
    #         if os.path.isfile(analyze_file_path): ########################## vm에서 실행
    #         # if os.path.isfile("../" + analyze_file_path):
    #             os.remove(analyze_file_path) # analyze_model 파일 삭제
    #         shutil.copyfile(manage_date_file_path, analyze_file_path) ########################## vm에서 실행
    #         # shutil.copyfile("../" + manage_date_file_path, "../" + analyze_file_path)
    #         break
    #     print("operating XXXXXXXX")






    # if os.path.isfile(manage_date_file_path):
    #
    #     # analyze_model_name 파일 삭제
    #     if os.path.isfile(analyze_file_path):
    #         os.remove(analyze_file_path)
    #
    #     # analyze_model_name 파일 복사
    #     shutil.copyfile(manage_date_file_path, analyze_file_path)

if __name__ == "__main__":
    #crontab_deploy_model_job()
    crontab_modify_model_name_job()

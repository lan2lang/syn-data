# coding=utf-8
import json
import requests
import os

from six import string_types
from six.moves.urllib.parse import urlencode, urlunparse  # noqa
from datetime import datetime, timedelta
from lark_oapi.api.bitable.v1 import *
import lark_oapi as lark
def build_url(path, query=""):
    # type: (str, str) -> str
    """
    Build request URL
    :param path: Request path
    :param query: Querystring
    :return: Request URL
    """
    scheme, netloc = "https", "api.oceanengine.com"
    return urlunparse((scheme, netloc, path, "", query, ""))

def post(json_str):
    # type: (str) -> dict
    """
    Send POST request
    :param json_str: Args in JSON format
    :return: Response in JSON format
    """
    url = build_url(PATH)
    args = json.loads(json_str)
    headers = {
        "Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    rsp = requests.post(url, headers=headers, json=args)
    return rsp.json()
    
def get(json_str,token,path):
    # type: (str) -> dict
    """
    Send GET request
    :param json_str: Args in JSON format
    :return: Response in JSON format
    """

    args = json.loads(json_str)
    query_string = urlencode({k: v if isinstance(v, string_types) else json.dumps(v) for k, v in args.items()})
    url = build_url(path, query_string)

    # 获取token
    headers = {
        "Access-Token": token,
    }
    rsp = requests.get(url, headers=headers)
    return rsp.json()

def get_refresh_token():
    # 创建client
    client = lark.Client.builder() \
        .app_id(os.getenv('FEISHU_APP_ID')) \
        .app_secret(os.getenv('FEISHU_APP_SECRET')) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求对象
    request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder() \
    .app_token("L2Dzb3J5eazLrQs38HacUacqntd") \
        .table_id("tblFgCluGlHpF4o8") \
        .page_size(20) \
        .request_body(SearchAppTableRecordRequestBody.builder()
                       
            .build()) \
        .build()

    # 发起请求
    response: SearchAppTableRecordResponse = client.bitable.v1.app_table_record.search(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    return json.loads(lark.JSON.marshal(response.data, indent=4))['items'][0]['fields']['文本'][0]['text']


def get_token():
    url = "https://api.oceanengine.com/open_api/oauth2/refresh_token/"

    # 读取refresh_token
    # with open('token.txt','r') as f:
    refresh_token= get_refresh_token()



    payload = json.dumps({
    "app_id": app_id,
    "secret": secret,
    "refresh_token": refresh_token
    })

    headers = {
    "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    # 写入refresh_token
    # with open('token.txt','w') as f:
    #     f.write(json.loads(response.text)['data']['refresh_token'])

    update_refresh_token(json.loads(response.text)['data']['refresh_token'])

    return json.loads(response.text)['data']['access_token']

def get_account_info(local_account_id,token):
    """
    获取昨天的数据
    """
    # token=get_token()
    path='/open_api/v3.0/local/report/account/get/'
    # print(token)

    # 本地推账户ID
    # local_account_id = '1838520591214027'

    # 时间粒度: "DAILY" 每日 / "HOURLY" 每小时
    time_granularity = "TIME_GRANULARITY_DAILY"
    # 开始日期 格式: "2024-01-01"

    yesterday = datetime.now() - timedelta(days=1)

    start_date = date
    # 结束日期
    end_date = date
    # 排序方式: "ASC" / "DESC"
    order_type = "DESC"
    # 排序字段
    order_field = "stat_cost"
    # 指标列表 - 根据需要选择
    # 常用指标: stat_cost(花费), show_cnt(展示), click_cnt(点击), ctr, convert_cnt(转化), pay_convert_cnt(付费转化)
    metrics_list = [
        "stat_cost",
        "show_cnt",
        "click_cnt",
        "ctr",
        'cpc_platform',
        'cpm_platform',
        'form_cnt',
         'clue_message_count',
          'phone_confirm_cnt',
        "convert_cnt",
        "conversion_cost",
        "conversion_rate"
    ]
    metrics = json.dumps(metrics_list)

    # 过滤条件 - 可选参数根据需求取消注释
    filtering = {}
   
    # 分页参数
    page = 1
    page_size = 100
    # =================================================

    # 构建参数 - 包含完整过滤条件
    if filtering:
        my_args = json.dumps({
            "local_account_id": local_account_id,
            "time_granularity": time_granularity,
            "start_date": start_date,
            "end_date": end_date,
            "order_type": order_type,
            "order_field": order_field,
            "metrics": metrics_list,
            "filtering": filtering,
            "page": page,
            "page_size": page_size
        })
    else:
        # 不使用过滤条件
        my_args = json.dumps({
            "local_account_id": local_account_id,
            # "time_granularity": time_granularity,
            "start_date": start_date,
            "end_date": end_date,
            "order_type": order_type,
            "order_field": order_field,
            "metrics": metrics_list,
            "page": page,
            "page_size": page_size
        })

    # print("请求参数:")
    # print(my_args)
    # print("\n请求结果:")
    result = get(my_args,token,path)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    return result

def update_refresh_token(token):
    # 创建client
    client = lark.Client.builder() \
        .app_id(os.getenv('FEISHU_APP_ID')) \
        .app_secret(os.getenv('FEISHU_APP_SECRET')) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象


     # 构造请求对象
    request: UpdateAppTableRecordRequest = UpdateAppTableRecordRequest.builder() \
    .app_token("L2Dzb3J5eazLrQs38HacUacqntd") \
        .table_id("tblFgCluGlHpF4o8") \
        .record_id('recvgbhADzCPK6')\
        .request_body(AppTableRecord.builder()
            .fields({'文本':token})
            .build()) \
        .build()

    # 发起请求
    response: UpdateAppTableRecordResponse = client.bitable.v1.app_table_record.update(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def upload_feishu(record):
    # 创建client
    client = lark.Client.builder() \
        .app_id(os.getenv('FEISHU_APP_ID')) \
        .app_secret(os.getenv('FEISHU_APP_SECRET')) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateAppTableRecordRequest = CreateAppTableRecordRequest.builder() \
        .app_token("L2Dzb3J5eazLrQs38HacUacqntd") \
        .table_id("tbl03OMtscmnaZ1z") \
        .request_body(record) \
        .build()

    # 发起请求
    response: CreateAppTableRecordResponse = client.bitable.v1.app_table_record.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

def gen_record(id,name,data):
    fields={'账号id':'000'}

    fields["账号id"]=id#岩天下CT3
    fields["账号名"]=name #岩天下CT3
    fields["展示次数"]=data['show_cnt'] 
    fields["消耗(元)"]=data['stat_cost'] 
    fields["点击次数"]=data['click_cnt'] 
    fields["点击率"]=data['ctr'] /100
    fields["点击均价(元)"]=data['cpc_platform'] 
    fields["平均千次展示费用(元)"]=data['cpm_platform'] 
    fields["转化数"]=data['convert_cnt'] 
    fields["转化率"]=data['conversion_rate'] /100
    fields["转化成本"]=data['conversion_cost'] 
    fields["表单提交数"]=data['form_cnt'] 
    fields["私信留资数"]=data['clue_message_count'] 
    fields["电话拨打数"]=data['phone_confirm_cnt'] 

    # yesterday = datetime.now() - timedelta(days=1)
    
    # fields["日期"]=yesterday.strftime('%Y-%m-%d')
    fields["日期"]=date

    record={'fields':fields}
    return record

if __name__ == '__main__':
    app_id = '1860693444062348'
    secret = '6ff21f5d04ee34937ad67eb3945aaf70608cb5b1'

    # 优化token获取,refresh_token存入文件
    token = get_token()

    # 

    # yesterday = datetime.now() - timedelta(days=1)
    yesterday = datetime.now()
    
    date=yesterday.strftime('%Y-%m-%d')

    # date='2026-04-09'
    account={'1838520591214027':'岩天下CT3',
             '1839857432169472':'冠睿艺术家居CT1'
             ,'1859165271300295':'科姆纳德建材-CT',
             '1859161008663561':'鑫岩汇岩板-CT'
             ,'1861164114127872':'鑫素颜陶瓷-CT',
             '1838520567278665':'岩天下CT2',
             '1838515264256011':'岩天下CT1',
             '1858801864450076':'万亿建材-ZX',
             '1860527940799751':'筑嘉陶瓷B端招商CT',
             '1860825649941516':'科姆纳德建材-CT-2',
             '1859627056547146':'营进建材-CT',
             '1859165271300295':'CIA瓷砖总部C端CT1',
             '1860825649941516':'CIA瓷砖经销商C端CT2',
             '1861798224039178':'鑫岩汇岩板-CT-2',
             }


    for id,name in account.items():
        print (id,name)
        data=get_account_info(id,token)['data']['data_list'][0]
        if data['stat_cost']==0:
            continue
        print(data)
       
        upload_feishu(gen_record(id,name,data))





    # 如果消耗=0，不上传

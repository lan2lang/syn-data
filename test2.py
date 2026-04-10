

    
    # # 从环境变量读取敏感信息（在GitHub Secrets中配置）
    # app_id = 'cli_a935c6cd8f385bd3'
    # app_secret = 'k5wMHHaXfj8AdHXosAKPMe0gcUhIVCd2'
    # app_token ='L2Dzb3J5eazLrQs38HacUacqntd' # 多维表格的token
    # table_id ='tblFgCluGlHpF4o8'  # 表格ID


import json

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a935c6cd8f385bd3") \
        .app_secret("k5wMHHaXfj8AdHXosAKPMe0gcUhIVCd2") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象


     # 构造请求对象
    request: UpdateAppTableRecordRequest = UpdateAppTableRecordRequest.builder() \
    .app_token("L2Dzb3J5eazLrQs38HacUacqntd") \
        .table_id("tblFgCluGlHpF4o8") \
        .record_id('recvgbhADzCPK6')\
        .request_body(AppTableRecord.builder()
            .fields({'文本':'1'})
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


if __name__ == "__main__":
    main()
    # recvgbhADzCPK6
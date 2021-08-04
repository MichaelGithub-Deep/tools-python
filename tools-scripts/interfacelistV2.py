from common.apigcctool import GetInterfaceFromSwagger
from common.exceltool import ExcelUtil
import os



if __name__ == '__main__':
        service_name = "p-purchase-app"

        # get the token of the target service
        url1 = r'http://qa.swagger.gongkongsaas.com/swagger-resources'
        header1 = {
                'Content-Type': 'application/json;charset=UTF-8',
        }

        get_token = GetInterfaceFromSwagger(url1,header1)
        service_token = get_token.get_service_token_from_list(service_name)

        # get the interface list of the service from swagger
        url = r'http://qa.swagger.gongkongsaas.com/v2/api-docs?group='
        header = {
                'Content-Type': 'application/json;charset=UTF-8',
                'knfie4j-gateway-request': service_token
        }
        get = GetInterfaceFromSwagger(url,header)
        data = get.get_interface_list_from_json(service_name)
        for interface in data:
                print(str(interface))

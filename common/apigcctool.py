import json

from common.httptool import  Runrequst

class GetInterfaceFromSwagger:
    """
    read the json file and extract the data
    created by yanghai
    """
    def __init__(self,url,header):
        # http://qa.swagger.gongkongsaas.com/v2/api-docs?group=order-app
        self.url = url
        self.headers = header
        # {
        #     'Content-Type': 'application/json;charset=UTF-8',
        #     'knfie4j-gateway-request': '2b3cb1e19707f14e6761fd1ac5ba2dbe'
        # }

    def extractor_json(self,service_name):
        """
        extrator the json file
        :param path:
        :param service_name:
        :return:
        """
        # service_name = service_name+".json"
        print(self.url+service_name)
        run = Runrequst(self.url+service_name, self.headers)
        response = json.loads(run.run_requst(method='GET'))
        return response

    def get_interface_list_from_json(self,service_name):
        """
        get the interface list from swagger
        :param service_name:
        :return:
        """
        dict_data = self.extractor_json(service_name)
        items = dict_data.get('paths')
        # print(items)
        interface_list = []
        for item in items:
            # interfaces = item['item']
            # for interface in interfaces:
            #     interface_list.append(interface['request']['url']['path'])
            interface_list.append(item)
        return interface_list

    def get_service_token_list(self):
        """
        get the token list from the swagger service
        :param service_name:
        :return:
        """
        run = Runrequst(self.url, self.headers)
        response = json.loads(run.run_requst(method='GET'))
        return response

    def get_service_token_from_list(self,service_name):
        """
        get the token of the service from the token list
        :param service_name:
        :return:
        """
        result = self.get_service_token_list()
        token = ''
        for i in range(len(result)):
            if result[i].get('name') == service_name:
                token = result[i].get('header')
        return token

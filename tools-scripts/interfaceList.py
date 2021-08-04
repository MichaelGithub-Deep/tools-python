import requests

import json
import time
import os
from common.exceltool import ExcelUtil


class Runrequst:
    """
    created by yanghai
    """
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def send_get(self, params):
        """
        method for the http/https get
        :param params:
        :return:
        """
        response = requests.get(url=self.url, params=params, headers=self.headers).json()
        return json.dumps(response, sort_keys=True, indent=4)

    def send_post(self, data):
        """
        method for the http/https post
        :param data:
        :return:
        """
        response = requests.post(url=self.url, headers=self.headers, json=data).json()
        return json.dumps(response, sort_keys=True, indent=4)

    def run_requst(self, params=None, data=None, method='POST'):
        """
        call the request based on the context of the params, data and method
        :param params:
        :param data:
        :param method:
        :return:
        """
        response = None
        if method == 'GET':
            response = self.send_get(params)
        else:
            response = self.send_post(data)
        return response

class Skywalking:
    """
    created by yanghai
    """
    def __init__(self):
        self.url = "http://qa.skywalking.gongkongsaas.com/graphql"
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'Hm_lvt_2a62041b665218eded38c01e7036991d=1616079045; _ga=GA1.1.594663117.1616731300; _ga_Z1ET54G2TN=GS1.1.1617689409.4.0.1617689409.0'

        }

    def get_services_list(self):
        """
        get the services list from the skywalking
        :return:
        """
        today = time.strftime("%Y-%m-%d")
        data = {
            "query": "query queryServices($duration: Duration!,$keyword: String!) {\n    services: searchServices(duration: $duration, keyword: $keyword) {\n      key: id\n      label: name\n    }\n  }",
            "variables": {
                "duration": {
                    "start": today+" 0001",
                    "end": today+" 2359",
                    "step": "MINUTE"
                },
                "keyword": ""
            }
        }

        # get the data by the graphql
        run = Runrequst(self.url, self.headers)
        response = json.loads(run.run_requst(data=data, method='POST'))
        services_list = response['data']['services']
        print("get the services list form the skywalking: "+str(services_list))
        return services_list

    def get_service_id_by_service_name(self, service_name=None):
        """
        get the service id based on the serbice name
        :param service_name:
        :return:
        """
        services_list = self.get_services_list()
        for service in services_list:
            if service_name == service['label']:
                print('the target service id '+service['key']+' ,when the service name == '+ service_name)
                return service['key']


    def get_interface_list_by_service_id_with_default_size(self, start_time, end_time, service_id):
        """
        get the interface list based on the start time, end time and service id and default 15
        :param start_time:
        :param end_time:
        :param service_id:
        :return:
        """

        return self.get_interface_list_by_service_id(start_time, end_time, service_id, 15)

    def get_interface_list_by_service_id(self, start_time, end_time, service_id, page_size):
        """
        get the interface list based on the start time, end time and service id
        :param start_time:
        :param end_time:
        :param service_id:
        :return:
        """
        data = {
                "query": "query queryTraces($condition: TraceQueryCondition) {\n  data: queryBasicTraces(condition: $condition) {\n    traces {\n      key: segmentId\n      endpointNames\n      duration\n      start\n      isError\n      traceIds\n    }\n    total\n  }}",
                "variables": {
                    "condition": {
                        "queryDuration": {
                            "start": start_time,
                            "end": end_time,
                            "step": "MINUTE"
                        },
                        "traceState": "ALL",
                        "paging": {
                            "pageNum": 1,
                            "pageSize": page_size,
                            "needTotal": True
                        },
                        "queryOrder": "BY_DURATION",
                        "serviceId": service_id
                    }
                }
            }

        run = Runrequst(self.url, self.headers)
        response = json.loads(run.run_requst(data=data, method='POST'))
        interfaces_list = response['data']['data']['traces']
        print("get the interface list form the skywalking: "+str(interfaces_list))
        interfaces_sum = response['data']['data']['total']
        print("get the interface sum form the skywalking: "+str(interfaces_sum))
        return response['data']['data']

    def get_interface_list_without_repeat(self,start_time, end_time, service_id):
        """
        get interface list and remove duplicate
        :param start_time:
        :param end_time:
        :param service_id:
        :return:
        """

        interface_dict = self.get_interface_list_by_service_id_with_default_size(start_time, end_time, service_id)
        interface_sum = interface_dict['total']
        # get all interface list with the page size = total
        interface_dict = self.get_interface_list_by_service_id(start_time, end_time, service_id, interface_sum)
        interface_list = interface_dict['traces']
        #print(str(interface_list))
        interface_set = set()
        print("start to get the interface list without repeat, the sum of the interface list :" + str(interface_sum))
        for interface in interface_list:
           # print(interface)
            for endpoint_name in interface['endpointNames']:
                if endpoint_name.startswith(r'//'):
                    endpoint_name = endpoint_name.replace('//','/')
                if endpoint_name.startswith(r'/'):
                    interface_set.add(endpoint_name)
                # temp = endpoint_name.split("}")
                # print(str(temp))
                # interface_set.add(temp[1])


        print("end to get the interface list without repeat, the sum of the interface set :" + str(len(interface_set)))
        return  interface_set

class ApigccExtractor:
    """
    read the json file and extract the data
    created by yanghai
    """
    def __init__(self):
        pass

    def extractor_json(self,path,file_name):
        """
        extrator the json file
        :param path:
        :param file_name:
        :return:
        """
        if file_name.endswith('.json'):
            path = os.path.join(path,file_name)
        else:
            path = os.path.join(path,file_name+".json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                dict_data = json.loads(f.read())
                return dict_data

    def get_interface_list_from_json(self,path,file_name):
        """
        get the interface list from json file
        :param path:
        :param file_name:
        :return:
        """
        dict_data = self.extractor_json(path,file_name)
        items = dict_data['item']
        interface_list = []
        for item in items:
            interfaces = item['item']
            for interface in interfaces:
                interface_list.append(interface['request']['url']['path'])
        return interface_list



if __name__ == '__main__':


    # 1.get the all interface list from the interface_file
    # path = r'D:\software\apache-tomcat-9.0.44\webapps\ROOT\interface'
    # file_name = '{}.json'.format(target_service)
    # read = ApigccExtractor()
    # data = read.get_interface_list_from_json(path, file_name)
    # print(f'The following interfaces are the whole list of {file_name}:')
    # for interface in data:
    #     print(str(interface))
    target_service = 'order-app'
    start_time = "2021-07-14 1340"
    end_time = "2021-07-14 1559"
    # 2.get the called interface list form skywalking during start_time to end_time
    print('<<<====================seperator=================================>>>')
    sky = Skywalking()
    service_id = sky.get_service_id_by_service_name(service_name=target_service)
    list_set = sky.get_interface_list_without_repeat(start_time, end_time, service_id)
    print(f'The following interfaces were called during the:{start_time} - {end_time}:')
    for trace in list_set:
        print(trace)

    # 3. get the uncalled interface list
    # print('<<<====================seperator=================================>>>')
    # list_uncalled = data.copy()
    # for element in list_set:
    #     try:
    #         list_uncalled.remove(element)
    #     except ValueError as e:
    #         print(str(e))
    # print(f'The following interfaces are uncalled during the:{start_time} - {end_time}:')
    #
    # for element_uncalled in list_uncalled:
    #     print(element_uncalled)

    # 4. summary
    print('<<<====================seperator=================================>>>')
    # print(f'The sum of interface euquals {str(len(data))}')
    print(f'The sum of called interface during the:{start_time} - {end_time} euquals {str(len(list_set))}')
    # print(f'The sum of uncalled interface during the:{start_time} - {end_time} euquals {str(len(list_uncalled))}')

    current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(current_path,'testresult','interface-list-order.xls')
    print(target_path)

    excel_handler = ExcelUtil()

    excel_handler.update_interface_list_tested(target_path, target_service, list(list_set))


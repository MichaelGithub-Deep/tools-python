import time
import json

import httptool

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
        run = httptool.Runrequst(self.url, self.headers)
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

        run = httptool.Runrequst(self.url, self.headers)
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
                if endpoint_name.startswith(r'/'):
                    interface_set.add(endpoint_name)
                # temp = endpoint_name.split("}")
                # print(str(temp))
                # interface_set.add(temp[1])


        print("end to get the interface list without repeat, the sum of the interface set :" + str(len(interface_set)))
        return  interface_set
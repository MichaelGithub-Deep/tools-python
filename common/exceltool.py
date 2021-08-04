import xlrd
import xlwt
from xlutils.copy import copy

class ExcelUtil:
    """
    Excel operation methods
    created by yanghai
    """
    def __init__(self):
        pass

    def path_is_exist(self, path):
        """
        Does the workbook exist in the given path
        :param path:
        :return:
        """
        try:
            xlrd.open_workbook(path, formatting_info=True)
        except FileNotFoundError as e:
            return False
        return True

    def sheet_name_is_exist(self,path,sheet_name):
        """
        Does the sheet name exist in the given path
        :param path:
        :param sheet_name:
        :return:
        """
        path_exist = self.path_is_exist(path)
        if path_exist:
            workbook = xlrd.open_workbook(path)
            sheets = workbook.sheet_names()
            if sheet_name in sheets:
                return True
        return False

    def create_sheet(self, path, sheet_name, value):
        """
        create a new sheet
        :param path:
        :param sheet_name:
        :param value:
        :return:
        """
        if self.path_is_exist(path):
            workbook = xlrd.open_workbook(path, formatting_info=True)
            if self.sheet_name_is_exist(path, sheet_name):
                print(f'The given sheet name:{sheet_name} already exist in the given path {path}')
                return False
            else:
                index = len(value)
                wb = copy(workbook)
                sheet = wb.add_sheet(sheet_name)
                for i in range(0, index):
                    for j in range(0, len(value[i])):
                        sheet.write(i, j, value[i][j])
                wb.save(path)
                print("xls write success!!!")
                return True
        else:
            index = len(value)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet(sheet_name)
            for i in range(0, index):
                for j in range(0, len(value[i])):
                    sheet.write(i, j, value[i][j])
            workbook.save(path)
            print("xls write success with creating new sheet!!!")
            return True

    def create_sheet_with_column(self, path, sheet_name, value,index=0):
        """
        create a new sheet
        :param path:
        :param sheet_name:
        :param value:
        :return:
        """
        if self.path_is_exist(path):
            workbook = xlrd.open_workbook(path, formatting_info=True)
            if self.sheet_name_is_exist(path, sheet_name):
                print(f'The given sheet name:{sheet_name} already exist in the given path {path}')
                return False
            else:
                wb = copy(workbook)
                sheet = wb.add_sheet(sheet_name)
                for i in range(0, index):
                    for j in range(0, len(value[i])):
                        sheet.write(i, j, value[i][j])
                wb.save(path)
                print("xls write success!!!")
                return True
        else:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet(sheet_name)
            for i in range(0, index):
                for j in range(0, len(value[i])):
                    sheet.write(i, j, value[i][j])
            workbook.save(path)
            print("xls write success with creating new sheet!!!")
            return True

    def sheet_append_data(self, path, sheet_name, value):
        """
        append data into the same sheet
        :param path:
        :param sheet_name:
        :param value:
        :return:
        """
        if self.path_is_exist(path):
            if self.sheet_name_is_exist(path, sheet_name):
                index = len(value)  # get the rows of the given data
                workbook = xlrd.open_workbook(path)
                worksheet = workbook.sheet_by_name(sheet_name)  # get the target sheet with the sheet name
                rows_old = worksheet.nrows  # get the existed rows
                new_workbook = copy(workbook)  # exchange the xlrd object into xlwt object
                new_worksheet = new_workbook.get_sheet(sheet_name)  # get the target sheet after exchanging
                for i in range(0, index):
                    for j in range(0, len(value[i])):
                        new_worksheet.write(i + rows_old, j, value[i][j])  # append the data
                new_workbook.save(path)
                print(f"Append data into sheet name：{sheet_name} success!!!")
            else:
                print(f'The given sheet_name:{sheet_name} does not exist!!!')
        else:
            print(f'The given path:{path} does not exist!!!')

    def sheet_read(self, path, sheet_name):
        """
        read the first tow columns from the given path
        :param path:
        :param sheet_name:
        :return:
        """
        if self.path_is_exist(path):
            if self.sheet_name_is_exist(path, sheet_name):
                workbook = xlrd.open_workbook(path)
                worksheet = workbook.sheet_by_name(sheet_name)
                interface_data = []
                interface_list = []
                interface_list_tested = []
                for i in range(0, worksheet.ncols):
                    for j in range(0, worksheet.nrows):
                        if not str(worksheet.cell_value(0, 0)).strip(' ').find('interface-list'):
                            if j >0 :
                                interface_list.append(worksheet.cell_value(j, 0))

                        if not str(worksheet.cell_value(0, 1)).strip(' ').find('interface-list-tested'):
                            if j >0 :
                                interface_list_tested.append(worksheet.cell_value(j, 1))

                interface_data.append(interface_list)
                interface_data.append(interface_list_tested)
                return interface_data
            else:
                print(f'The given sheet_name:{sheet_name} does not exist!!!')
        else:
            print(f'The given path:{path} does not exist!!!')


    def update_interface_list_tested(self, path, sheet_name, interface_list_tested):
        """

        """
        if self.path_is_exist(path):
            if self.sheet_name_is_exist(path, sheet_name):

                workbook = xlrd.open_workbook(path)
                worksheet = workbook.sheet_by_name(sheet_name)
                new_workbook = copy(workbook)
                new_worksheet = new_workbook.get_sheet(sheet_name)
                for i in range(0, worksheet.nrows):
                    if interface_list_tested.count(worksheet.cell_value(i, 0)):
                        new_worksheet.write(i, 1, worksheet.cell_value(i, 0))
                new_workbook.save(path)

            else:
                print(f'The given sheet_name:{sheet_name} does not exist!!!')
        else:
            print(f'The given path:{path} does not exist!!!')

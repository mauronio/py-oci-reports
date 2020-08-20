import xlsxwriter
import os

from base_writer import ReportWriter

class SpreadSheetWriter(ReportWriter):

    def __init__(self, working_path, config):

        self.settings = config['spreadsheet-settings']
        self.workbook = xlsxwriter.Workbook(os.path.join(working_path, self.settings['file-name']))
        self.current_coordinates = {}
        for report in config['reports']:
            report_name = report['name']
            self.workbook.add_worksheet(report_name)
            self.current_coordinates[report_name] = self.settings['start-coordinates'].copy()


    def write_table(self, report_name, title, column_list, row_list):

        current_coordinates = self.current_coordinates[report_name]
        worksheet = self.workbook.get_worksheet_by_name(report_name)

        row = current_coordinates['row']
        col = current_coordinates['col']

        worksheet.write(row, col, title)
        row += 1

        for column in column_list:
            column_name = column['name']
            worksheet.write(row, col, column_name)
            col += 1 

        row += 1
        col = current_coordinates['col']

        for row_data in row_list:
            col = current_coordinates['col']
            for col_data in row_data:
                worksheet.write(row, col, col_data)
                col += 1
            row += 1 

        row += 1 

        current_coordinates['row'] = row
        
    def close(self):

        self.workbook.close()


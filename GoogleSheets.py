import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


class GoogleSheets:

    def getAllLessons(self):
        CREDENTIALS_FILE = 'client.json'  # имя файла с закрытым ключом
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())

        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        spreadsheet_id = '1wIyGRvHLc7ljy_9txoy-ec__ks4fapkP3HgYLVYHk2o'  # TODO: Update placeholder value.

        # The ranges to retrieve from the spreadsheet.
        ranges = 'A:B'  # TODO: Update placeholder value.

        # True if grid data should be returned.
        # This parameter is ignored if a field mask was set in the request.
        include_grid_data = False  # TODO: Update placeholder value.

        value_render_option = 'FORMATTED_VALUE'  # TODO: Update placeholder value.

        # How dates, times, and durations should be represented in the output.
        # This is ignored if value_render_option is
        # FORMATTED_VALUE.
        # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
        date_time_render_option = 'SERIAL_NUMBER'  # TODO: Update placeholder value.
        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=ranges,
                                                      valueRenderOption=value_render_option,
                                                      dateTimeRenderOption=date_time_render_option)
        # request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
        response = request.execute()
        pprint(response)

        # TODO: Change code below to process the `response` dict:
        return response

    def addNewPerson(self, user_information):
        CREDENTIALS_FILE = 'client.json'  # имя файла с закрытым ключом
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())

        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        spreadsheet_id = '1wIyGRvHLc7ljy_9txoy-ec__ks4fapkP3HgYLVYHk2o'  # TODO: Update placeholder value.
        list = []
        for i in user_information.split():
            list.append([i])

        resource = {
            "majorDimension": "COLUMNS",
            "values": list
        }
        range = "A1:E1"
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range,
            body=resource,
            valueInputOption="USER_ENTERED"
        ).execute()

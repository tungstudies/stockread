# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


try:
    import sys

    print('System Version: {}'.format(sys.version))

    from data.ggsheets import GoogleSheets
    from social.youtube.youtube_chn import Channel

except ModuleNotFoundError as err:
    print('Some modules are missing: {}'.format(err))
    sys.exit()


def main():
    # Use a breakpoint in the code line below to debug your script.
    # Press ⌘F8 to toggle the breakpoint.

    spreadsheet_id = "1iUg_IBkq64BuFBrL0QHSxTo7Ew7tofFCQYGvL8c15LU"  # Please set the Spreadsheet ID.
    worksheet_name = "SelectedChannels"  # Please set the sheet name.

    ggs = GoogleSheets(spreadsheet_id=spreadsheet_id, worksheet_name=worksheet_name)
    selected_channels = set(ggs.get_data_by_headers(['Channel ID']))
    channels = [Channel(channel_id).to_dict() for channel_id in selected_channels]
    ggs.create(channels, 'DetailedSelectedChannels', has_sequence=False)
    ggs.worksheet.sort((8, 'des'))


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

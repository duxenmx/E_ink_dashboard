

from oauth2client.service_account import ServiceAccountCredentials
import gspread
from modules import d_functions as d_f
import os

# define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# log file to check previous data
csv_a_values = []
csv_b_values = []


def get_tasklist(gsheetjson, sheetname, creddir):
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        str(os.path.join(creddir, str(gsheetjson))), scope)
    client = gspread.authorize(creds)
    sheet = client.open(str(sheetname))
    sheet_instance = sheet.get_worksheet(0)
    csv_a_values = sheet_instance.col_values(1)[:30]
    csv_b_values = sheet_instance.col_values(2)[:30]

    return csv_a_values, csv_b_values


def draw_tasklist_mod(t_s_x, t_s_y, draw, csv_a_values, csv_b_values, color):
    draw.text((t_s_x, t_s_y), "To-Do:                                        Groceries:",
              font=d_f.font_size(24), fill=color)
    t_s_y = t_s_y+32
    t_s_y_0 = t_s_y
    x = 1
    y = 1
    for i in range(1, len(csv_b_values)):
        if str(csv_b_values[i]) != "":
            if x <= 6:
                draw.text((t_s_x, t_s_y), '- ' +
                          str(csv_b_values[i]), font=d_f.font_size(18), fill=color)
                t_s_y = t_s_y + 25
                x = x+1
    t_s_y = t_s_y_0
    for i in range(1, len(csv_a_values)):
        if str(csv_a_values[i]) != "":
            if y <= 7:
                draw.text((t_s_x+240, t_s_y), '- ' +
                          str(csv_a_values[i]), font=d_f.font_size(18), fill=color)
                t_s_y = t_s_y + 25
                y = y+1


def run_tasklist_mod(gsheetjson, sheetname, creddir, mod_tl_s_x, mod_tl_s_y, draw, color):
    csv_a_values, csv_b_values = get_tasklist(gsheetjson, sheetname, creddir)
    draw_tasklist_mod(mod_tl_s_x, mod_tl_s_y, draw, csv_a_values, csv_b_values, color)
    csv_a_values.clear()
    csv_b_values.clear()

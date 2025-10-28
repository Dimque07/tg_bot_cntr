import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def save_booking(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("CNTR Bookings").sheet1

    row = [
        data["name"],
        data["date"],
        data["time"],
        data["guests"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    sheet.append_row(row)

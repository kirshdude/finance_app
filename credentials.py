import gspread

SHEET_ID = '1j2U5ea1bUKI66Bum-ATuQL4tqURJXWjujcBSFFiz9eo'
gc = gspread.service_account('/Users/eyalk/Downloads/personal-finance-401213-68f83b5d5a73.json')
spreadsheet = gc.open_by_key(SHEET_ID)

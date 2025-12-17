def save_result(level, score):
    try:
        client = get_client()
        sheet = client.open_by_key("1f9nZ2SW43Q86UEH1hiAeAn10ZNf-jYWfiQbl65SB2C0").sheet1
        sheet.append_row([level, score])
    except Exception as e:
        print("=== SHEETS ERROR ===")
        print(e)
        raise

from datetime import datetime

timestamp = datetime.now().isoformat()
sheet.append_row([
    timestamp,
    email,
    level,
    score
])

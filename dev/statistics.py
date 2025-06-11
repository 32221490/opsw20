from tinydb import TinyDB
import pathlib
from collections import Counter, defaultdict

SAVE_DIR = pathlib.Path(__file__).parent / "save_files"

# 모든 슬롯의 플레이어를 불러옴
def load_all_players():
    players = []
    for slot_num in [1, 2, 3]:
        db_path = SAVE_DIR / f"slot_{slot_num}.json"
        if db_path.exists():
            db = TinyDB(db_path)
            data = db.all()
            if data:
                players.append(data[0])
            db.close()
    return players

# 통계 리포트 생성
def generate_statistics_report():
    players = load_all_players()
    if not players:
        return "No saved player data to generate statistics."

    weapon_counter = Counter()
    passive_counter = Counter()
    slot_count = len(players)

    for player in players:
        weapon_counter[player["weapon"]] += 1
        passive_counter[player["passive"]] += 1

    report_lines = []
    report_lines.append("===== PLAYER STATISTICS REPORT =====")
    report_lines.append(f"Total Slots Analyzed: {slot_count}")
    report_lines.append("")

    report_lines.append("Weapon Usage:")
    for weapon, count in weapon_counter.items():
        report_lines.append(f"- {weapon}: used in {count} slot(s)")

    report_lines.append("")
    report_lines.append("Passive Item Usage:")
    for passive, count in passive_counter.items():
        report_lines.append(f"- {passive}: used in {count} slot(s)")

    return "\n".join(report_lines)

from tinydb import TinyDB, Query
from collections import Counter

battle_history_db = TinyDB('battle_history.json')

def save_battle_history(data):
    battle_history_db.insert(data)

def get_battle_history():
    return battle_history_db.all()

def clear_battle_history():
    battle_history_db.truncate()

def show_battle_statistics():
    history = get_battle_history()
    if not history:
        print("아직 전투 기록이 없습니다.")
        return

    total_battles = len(history)
    total_victories = sum(1 for record in history if record.get("survived"))
    total_defeats = total_battles - total_victories
    total_enemies_defeated = sum(record.get("enemies_defeated", 0) for record in history)

    print("\n===== 전투 통계 =====")
    print(f"총 전투 수: {total_battles}")
    print(f"승리한 전투: {total_victories}")
    print(f"패배한 전투: {total_defeats}")
    print(f"처치한 적의 수: {total_enemies_defeated}")

def show_detailed_statistics():
    history = get_battle_history()
    if not history:
        print("아직 전투 기록이 없습니다.")
        return

    total_battles = len(history)
    total_victories = sum(1 for record in history if record.get("survived"))
    total_defeats = total_battles - total_victories

    monster_names = []
    for record in history:
        if "monster" in record:
            monster_names.append(record["monster"])
    most_common_monster = Counter(monster_names).most_common(1)

    total_enemies_defeated = sum(record.get("enemies_defeated", 0) for record in history)
    avg_enemies_defeated = total_enemies_defeated / total_battles

    print("\n===== 전투 상세 통계 =====")
    print(f"총 전투 수: {total_battles}")
    print(f"승리: {total_victories}회, 패배: {total_defeats}회")
    print(f"평균 처치 적 수: {avg_enemies_defeated:.2f}")

    if most_common_monster:
        print(f"가장 자주 만난 몬스터: {most_common_monster[0][0]} ({most_common_monster[0][1]}회)")

    print("============================")

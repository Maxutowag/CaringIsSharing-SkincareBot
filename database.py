import json, os

def save_routine(user_id, answers, routine):
    db = {}
    if os.path.exists("routines.json"):
        with open("routines.json") as f:
            db = json.load(f)
    db[str(user_id)] = {"answers": answers, "routine": routine}
    with open("routines.json", "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_routine(user_id):
    if not os.path.exists("routines.json"):
        return None
    with open("routines.json") as f:
        db = json.load(f)
    return db.get(str(user_id))

def delete_routine(user_id):
    if not os.path.exists("routines.json"):
        return False
    with open("routines.json") as f:
        db = json.load(f)
    if str(user_id) in db:
        del db[str(user_id)]
        with open("routines.json", "w") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        return True
    return False

import json


def new_game():
    return {"items": {}, "load": 0, "capacity": 2, "stock": 100, "metric": 100, "day": 1, "id": 0, "fault": False, "resource": 10, "rate": 2, "clock": 0, "paused": False, "settled": False}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def add(state, item_id, amount):
    if state["settled"]:
        return False
    if item_id in state["items"]:
        return False
    if amount <= 0 or amount > state["stock"]:
        return False
    state["items"][item_id] = amount
    state["stock"] -= amount
    return True


def receive(state, item_id):
    if state["settled"]:
        return False
    if state["load"] >= state["capacity"]:
        return False
    state["load"] += 1
    return True


def fee(state, item_id, end_day):
    return max(0, end_day - state["day"]) * state["rate"]


def cancel(state, item_id):
    if state["settled"]:
        return False
    if item_id not in state["items"]:
        return False
    state["stock"] += state["items"].pop(item_id)
    return True


def produce(state, amount):
    if state["settled"]:
        return False
    if state["fault"]:
        return False
    return True


def event(state):
    if state["settled"]:
        return state["metric"]
    state["metric"] = max(0, state["metric"] - 10)
    return state["metric"]


def guard(state, item_id):
    if state["settled"]:
        return False
    return state["resource"] > 0


def tick(state):
    if state["paused"] or state["settled"]:
        return state["clock"]
    state["clock"] += 1
    return state["clock"]


def settle(state):
    state["settled"] = True
    return True


def main():
    state = new_game()
    print("命令: add/receive/fee/cancel/produce/event/guard/tick/settle/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        try:
            if cmd == "add" and len(args) == 2:
                print(add(state, int(args[0]), int(args[1])))
            elif cmd == "receive" and len(args) == 1:
                print(receive(state, int(args[0])))
            elif cmd == "fee" and len(args) == 2:
                print(fee(state, int(args[0]), int(args[1])))
            elif cmd == "cancel" and len(args) == 1:
                print(cancel(state, int(args[0])))
            elif cmd == "produce" and len(args) == 1:
                print(produce(state, int(args[0])))
            elif cmd == "event" and not args:
                print(event(state))
            elif cmd == "guard" and len(args) == 1:
                print(guard(state, int(args[0])))
            elif cmd == "tick" and not args:
                print(tick(state))
            elif cmd == "settle" and not args:
                print(settle(state))
            else:
                print("ok")
        except ValueError:
            print("ok")


if __name__ == "__main__":
    main()

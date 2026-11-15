"""Parking Management System (PS No. 49)

Console parking system for a small lot of 5 slots.
Rates: car Rs.20/hour, bike Rs.10/hour. Hours are rounded up, minimum 1 hour.
Data is saved to parking.txt after every change.
"""

import math
import os
import re

TOTAL_SLOTS = 5
RATES = {"car": 20, "bike": 10}
DATA_FILE = "parking.txt"
VEHICLE_PATTERN = re.compile(r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$")

# slots[i] is None (free) or a dict {"number": ..., "type": ...}
slots = [None] * TOTAL_SLOTS


# ---------- file handling ----------
def save_data():
    """Write every slot to parking.txt (one line per slot)."""
    with open(DATA_FILE, "w") as f:
        for i, v in enumerate(slots, start=1):
            if v is None:
                f.write(f"{i},EMPTY\n")
            else:
                f.write(f"{i},{v['number']},{v['type']}\n")


def load_data():
    """Load slots from parking.txt if it exists."""
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE) as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3 and parts[0].isdigit():
                idx = int(parts[0]) - 1
                if 0 <= idx < TOTAL_SLOTS and parts[2] in RATES:
                    slots[idx] = {"number": parts[1], "type": parts[2]}


# ---------- helpers ----------
def free_count():
    return slots.count(None)


def find_vehicle(number):
    """Return the slot index of a parked vehicle, or -1."""
    for i, v in enumerate(slots):
        if v is not None and v["number"] == number:
            return i
    return -1


def valid_vehicle_number(number):
    return bool(VEHICLE_PATTERN.match(number))


def calculate_fee(vehicle_type, hours):
    """Return (hours_charged, fee, note). Rounds up; minimum 1 hour."""
    if hours < 1:
        charged, note = 1, " (minimum)"
    else:
        charged = math.ceil(hours)
        note = " (rounded up)" if charged != hours else ""
    return charged, charged * RATES[vehicle_type], note


# ---------- features ----------
def entry():
    number = input("Vehicle: ").strip().upper()
    if not valid_vehicle_number(number):
        print("Invalid vehicle number. Format example: MH12AB1234")
        return
    if find_vehicle(number) != -1:
        print(f"Vehicle {number} is already parked.")
        return
    vtype = input("Type: ").strip().lower()
    if vtype not in RATES:
        print("Invalid type. Enter car or bike.")
        return
    if free_count() == 0:
        print("Parking lot is full.")
        return
    idx = slots.index(None)
    slots[idx] = {"number": number, "type": vtype}
    save_data()
    print(f"Vehicle {number} parked in slot {idx + 1}. Slots free: {free_count()}")


def exit_vehicle():
    number = input("Vehicle: ").strip().upper()
    idx = find_vehicle(number)
    if idx == -1:
        print(f"Vehicle {number} not found.")
        return
    try:
        hours = float(input("Hours: "))
    except ValueError:
        print("Invalid hours. Enter a number.")
        return
    if hours <= 0:
        print("Invalid hours. Must be greater than 0.")
        return
    charged, fee, note = calculate_fee(slots[idx]["type"], hours)
    slots[idx] = None
    save_data()
    print(f"Hours charged: {charged}{note} \u2502 Fee: {fee}")
    print(f"Slot {idx + 1} is now free.")


def status():
    for i, v in enumerate(slots, start=1):
        if v is None:
            print(f"Slot {i}: free")
        else:
            print(f"Slot {i}: {v['number']} ({v['type']})")
    print(f"Slots free: {free_count()} of {TOTAL_SLOTS}")


def main():
    load_data()
    while True:
        print("\n1 Entry  2 Exit  3 Status  4 Quit")
        choice = input("Menu option: ").strip()
        if choice == "1":
            entry()
        elif choice == "2":
            exit_vehicle()
        elif choice == "3":
            status()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()

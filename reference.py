import sys
from typing import NamedTuple, Any

stations = ["garibaldi", "universita", "municipio", "toledo", "dante", "museo", "materdei", "vanvitelli", "augusteo",
            "fuga", "mergellina", "manzoni"]


class State(NamedTuple):
    cards: dict[str, int]
    trips: dict[str, int]
    pendings: list[str]

def positive(word: str) -> bool:
    return word.isascii() and word.isalpha()

def ifTapIsValid(s: State, card : str, station : str) -> tuple[str, State] | None:
    if station not in stations:
        return f"ERROR unknown station {station}", s
    cardExists = s.trips[card]
    if cardExists == card:
        return f"ERROR already in {card}", s
    if positive(card) and positive(station):
        s.cards[card] += 2
        s.trips[station] += 1
        s.pendings.append(card)
        return "OK", s
    return None

def ifTapoutIsValid(s: State, card : str, station : str) -> tuple[str, State] | None:
    if station not in stations:
        return f"ERROR unknown station {station}", s
    if card not in s.cards or card not in s.trips[card]:
        return f"ERROR not in {card}", s
    s.pendings.remove(card)
    return "OK", s

def printStatus(s):
    return s.pendings

def payForUser(s, card):
    return s.cards[card]

def mostTripsForStation(s, station):
    sortTrips = sorted(s.trips.items(), key=lambda pair: (-pair[1], pair[0]))
    return " ".join(f"{station} {n}" for station, n in sortTrips) or "none"

def step(words: list[str], s: State) -> tuple[str, State]:
    match words:
        case ["TAPIN", card, station]:
            return ifTapIsValid(s, card, station)
        case ["TAPOUT", card, station]:
            return ifTapoutIsValid(s, card, station)
        case ["PENDING"]:
            return printStatus(s)
        case ["FARE", card]:
            return payForUser(s, card)
        case ["REGULARS", station]:
            return mostTripsForStation(s, station)
        case _:
            return f"ERROR invalid command", s

def main() -> None:
    state = State({}, {}, [])
    for line in sys.stdin:
        words = line.split()
        if words:
            answer, state = step(words, state)
            print(answer)

if __name__ == '__main__':
    main()
from typing import List

class Unit:
    def __init__(self, name, unit_class, hp, armor, melee_damage=0, ranged_damage=0, ammo=-1, atk_seq=[]):
        self.name = name
        self.unit_class = unit_class
        self.hp = hp
        self.armor = armor
        self.melee_damage = melee_damage
        self.ranged_damage = ranged_damage
        self.ammo = ammo
        self.atk_seq = atk_seq  # preferred target sequence

    def take_damage(self, incoming_damage):
        actual_damage = max(0, incoming_damage - self.armor)
        self.hp -= actual_damage
        return actual_damage

    def is_alive(self):
        return self.hp > 0

class Slot:
    def __init__(self, unit_class, size):
        self.unit_class = unit_class
        self.size = size
        self.units: List[Unit] = []

    def populate_slot(self, units: List[Unit]):
        for unit in units:
            if self.size > 0 and unit.unit_class == self.unit_class:
                self.units.append(unit)
                self.size -= 1

    def is_empty(self):
        return all(not unit.is_alive() for unit in self.units)

class Field:
    def __init__(self, slots: List[Slot]):
        self.slots = slots

    def redistribute_damage(self):
        total_damage = sum(max(0, unit.hp) for slot in self.slots for unit in slot.units if not unit.is_alive())
        alive_units = [unit for slot in self.slots for unit in slot.units if unit.is_alive()]
        if alive_units:
            avg_damage = total_damage / len(alive_units)
            for unit in alive_units:
                unit.hp -= avg_damage  # Apply average damage evenly across alive units

class Battle:
    def __init__(self, field_a: Field, field_b: Field):
        self.field_a = field_a
        self.field_b = field_b

    def simulate_round(self):
        for attacker_field, defender_field in [(self.field_a, self.field_b), (self.field_b, self.field_a)]:
            for slot in attacker_field.slots:
                for unit in slot.units:
                    if unit.is_alive():
                        targets = self.select_targets(unit, defender_field)
                        for target in targets:
                            damage = unit.ranged_damage if unit.ammo > 0 else unit.melee_damage
                            unit.ammo -= 1 if unit.ammo > 0 else 0
                            actual_damage = target.take_damage(damage)
                            print(f"{unit.name} deals {actual_damage} to {target.name}")
                            if not target.is_alive():
                                print(f"{target.name} has died")
                            if not unit.is_alive():  # Stop if attacker is dead
                                break
                    if slot.is_empty():
                        break

            defender_field.redistribute_damage()

    def select_targets(self, attacker: Unit, defender_field: Field):
        targets = []
        for preferred_class in attacker.atk_seq:
            targets += [unit for slot in defender_field.slots for unit in slot.units if unit.unit_class == preferred_class and unit.is_alive()]
            if targets:
                break
        return targets if targets else [unit for slot in defender_field.slots for unit in slot.units if unit.is_alive()]

# Initialize a battle with example units

# Define unit templates
steam_giant = Unit("Steam Giant", "Heavy Infantry", hp=500, armor=50, melee_damage=40)
swordsman = Unit("Swordsman", "Light Infantry", hp=200, armor=10, melee_damage=20)
archer = Unit("Archer", "Long-Range Fighter", hp=100, armor=5, ranged_damage=30, ammo=10)

# Define slots for both sides
slots_a = [Slot("Heavy Infantry", 2), Slot("Light Infantry", 2), Slot("Long-Range Fighter", 2)]
slots_b = [Slot("Heavy Infantry", 2), Slot("Light Infantry", 2), Slot("Long-Range Fighter", 2)]

# Populate slots with units
slots_a[0].populate_slot([steam_giant, steam_giant])
slots_a[1].populate_slot([swordsman, swordsman])
slots_a[2].populate_slot([archer, archer])

slots_b[0].populate_slot([steam_giant, steam_giant])
slots_b[1].populate_slot([swordsman, swordsman])
slots_b[2].populate_slot([archer, archer])

# Create Fields
field_a = Field(slots_a)
field_b = Field(slots_b)

# Initialize Battle
battle = Battle(field_a, field_b)
battle.simulate_round()

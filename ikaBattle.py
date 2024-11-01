from typing import Any


class Unit:
    def __init__(self, name, unit_class, hp=1, armor=0, size=1, melee_damage=0, ranged_damage=-1, ammo=-1, atk_seq=[]):
        # 'Hoplite', 'Sulfur Carabineer', 'Mortar' etc.
        self.name = name

        # 'Frontline', 'Ranged', 'Artillery', etc.
        self.unit_class = unit_class
        self.hp = hp                        # maximum hitpoint of unit
        self.armor = armor                  # armor of unit
        self.size = size                    # size of unit
        self.melee_damage = melee_damage    # melee attack damage of unit
        self.ranged_damage = ranged_damage  # ranged attack damage of unit
        self.ammo = ammo                    # ammo for ranged attack damage

        # list of target unit classes. first is preferred, then second and so on
        self.atk_seq = atk_seq

        # TODO self.speed

    def take_damage(self, incoming_damage):
        actual_damage = max(0, incoming_damage - self.armor)
        self.hp -= actual_damage
        if self.hp <= 0:
            self.hp = 0


type batch = list[Unit]


class Wave:
    def __init__(self, units: batch):
        self.unit_types = []
        self.unit_counts = []
        # TODO self.speed

        for unit in units:
            if unit.name in self.unit_types:
                # if not the first unit of this type increase unit count
                self.unit_counts[self.unit_types.index(unit.name)] += 1
            else:
                # if first of this type add type to list
                self.unit_types.append(unit.name)
                self.unit_counts.append(1)  # set unit count to 1


class Slot:
    def __init__(self, unit_class, size):
        self.unit_class = unit_class
        self.size = size
        self.units : batch = []

    def populate_slot(self,units:batch):
        starting_size = self.size
        for unit in units:
            if unit.unit_class == self.unit_class:
                if self.size >= unit.size:
                    self.size -= unit.size
                    self.units.append(units.pop(units.index(unit)))
            else:
                self.size = starting_size
                self.units.clear()
                return False
        return True


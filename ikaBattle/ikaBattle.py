from typing import Any

type formation = list[Slot]
type batch = list[Unit]

class Unit:
    def __init__(self, name, unit_class, hp=1, armor=0, size=1, melee_damage=0, ranged_damage=-1, ammo=-1):
        # 'Hoplite', 'Sulfur Carabineer', 'Mortar' etc.
        self.name = name

        # 'Heavy Infantry', 'LongRange', 'Artillery', etc.
        self.unit_class = unit_class
        self.hp = hp                        # maximum hitpoint of unit
        self.armor = armor                  # armor of unit
        self.size = size                    # size of unit
        self.melee_damage = melee_damage    # melee attack damage of unit
        self.ranged_damage = ranged_damage  # ranged attack damage of unit
        self.ammo = ammo                    # ammo for ranged attack damage

       

        # TODO self.speed

    def take_damage(self, incoming_damage):
        actual_damage = max(0, incoming_damage - self.armor)
        self.hp -= actual_damage
        if self.hp <= 0:
            self.hp = 0

    def get_power(self):
        return self.hp + max(self.melee_damage, self.ranged_damage) + self.armor


class Wave:
    def __init__(self, units: batch):
        self.units_dict = {}
        for unit in units:
            power = unit.get_power()
            if unit.name not in self.units_dict:
                # Initialize with count, units list, and calculated power
                
                self.units_dict[unit.name] = {
                    "count": 1,
                    "units": [unit],
                    "power": power
                }
            else:
                # Update existing entry
                self.units_dict[unit.name]["count"] += 1
                self.units_dict[unit.name]["units"].append(unit)


class Slot:
    
    def __init__(self, slot_class, size):
        self.slot_class = slot_class
        self.size = size
        self.units : batch = []
        self.power = -1
        self.set_atk_seq()
        self.set_fill_rules()


    def set_atk_seq(self):
         # list of target unit classes. first is preferred, then second and so on
        if self.slot_class == "Frontline":
            self.atk_seq = ["Frontline","LongRange","Artillery","Flanks"]
        elif self.slot_class == "Flanks":
            self.atk_seq = ["Flanks","LongRange","Artillery","Frontline"]
        elif self.slot_class == "LongRange":
            self.atk_seq = ["Frontline","Flanks","LongRange"]
        elif self.slot_class == "Artillery":
            self.atk_seq = ["Frontline","Flanks"]
        elif self.slot_class == "Bombers":
            self.atk_seq = ["Artillery","LongRange","Frontline","Flanks"]
        elif self.slot_class == "AirDefence":
            self.atk_seq = ["Bombers","AirDefence"]
        else:
            self.atk_seq = []

    def set_fill_rules(self):
        if self.slot_class == "Frontline":
            self.preferred_unit_class = ["Heavy Infantry","Light Infantry","Long-Range Fighter"]
            self.strongest = False
        elif self.slot_class == "Flanks":
            self.preferred_unit_class = ["Light Infantry"]
            self.strongest = True
        elif self.slot_class == "LongRange":
            self.preferred_unit_class = ["Long-Range Fighter"]
            self.strongest = True
        elif self.slot_class == "Artillery":
            self.preferred_unit_class = ["Artillery"]
            self.strongest = True
        elif self.slot_class == "Bombers":
            self.preferred_unit_class = ["Bomber"]
            self.strongest = False
        elif self.slot_class == "AirDefence":
            self.preferred_unit_class = ["Fighter Pilot"]
            self.strongest = True

    def populate_slot(self,units:batch):
        #TODO AAAAAAAAAAAA
        current_unit_name = ""
        units.sort(reverse=(not self.strongest),key=Unit.get_power)
        for cls in self.preferred_unit_class:
            for unit in units:
                if current_power != -1 and current_unit_name == unit.name:
                    if self.size >= unit.size:
                            self.size -= unit.size
                            #.append(unit)
                            current_power += unit.get_power()
                elif unit.unit_class == cls:
                    if self.slot_class == "Frontline" and unit.unit_class == "Long-Range Fighter" and unit.ammo != 0:
                        continue
                    if self.size >= unit.size:
                        self.size -= unit.size
                        # .append()
                        current_unit_name = unit.name
                        self.power = unit.get_power()
            
            #units.pop(units.index(unit))


class Field:
    def __init__(self,level=25,is_sea=False):
        self.level = min(max(level,1),25)
        self.formations : list[formation] = []
        self.waves : list[Wave] = []
        if not is_sea:
            if level < 5:
                self.formations.append(self.prepare_formations("Frontline",30,3))
                self.formations.append(self.prepare_formations("LongRange",30,3))
                self.formations.append(self.prepare_formations("Artillery",30,1))
                self.formations.append(self.prepare_formations("Bombers",10,1))
                self.formations.append(self.prepare_formations("AirDefence",10,1))
            elif level >= 5 and level < 10:
                self.formations.append(self.prepare_formations("Frontline",30,5))
                self.formations.append(self.prepare_formations("LongRange",30,5))
                self.formations.append(self.prepare_formations("Artillery",30,2))
                self.formations.append(self.prepare_formations("Flanks",30,2))
                self.formations.append(self.prepare_formations("Bombers",20,1))
                self.formations.append(self.prepare_formations("AirDefence",20,1))
            elif level >= 10 and level < 17:
                self.formations.append(self.prepare_formations("Frontline",30,7))
                self.formations.append(self.prepare_formations("LongRange",30,7))
                self.formations.append(self.prepare_formations("Artillery",30,3))
                self.formations.append(self.prepare_formations("Flanks",30,4))
                self.formations.append(self.prepare_formations("Bombers",30,1))
                self.formations.append(self.prepare_formations("AirDefence",30,1))
            elif level >= 17 and level < 25:
                self.formations.append(self.prepare_formations("Frontline",40,7))
                self.formations.append(self.prepare_formations("LongRange",40,7))
                self.formations.append(self.prepare_formations("Artillery",30,4))
                self.formations.append(self.prepare_formations("Flanks",30,6))
                self.formations.append(self.prepare_formations("Bombers",20,2))
                self.formations.append(self.prepare_formations("AirDefence",20,2))
            elif level >= 25:
                self.formations.append(self.prepare_formations("Frontline",50,7))
                self.formations.append(self.prepare_formations("LongRange",50,7))
                self.formations.append(self.prepare_formations("Artillery",30,5))
                self.formations.append(self.prepare_formations("Flanks",40,6))
                self.formations.append(self.prepare_formations("Bombers",30,2))
                self.formations.append(self.prepare_formations("AirDefence",30,2))
        else:
            placeholder=""

    def add_wave(self,wave:Wave):
        self.waves.append(wave)

    def prepare_formations(self,slot_class,size,count):
        formation = []
        for _ in range(count):
            formation.append(Slot(slot_class,size))
        return formation
    
    def fill_formations(self):
        for wave in self.waves:
            for line in self.lines:
                for slot in line:
                    slot.populate_slot(wave)



def generate_land_wave(hop=0,sg=0,sword=0,spear=0,gun=0,archer=0,slinger=0,ram=0,cata=0,mortar=0,gyro=0,balloon=0,doctor=0,cook=30,spartan=0,wall=0):
    wave : batch = []
    for i in range(hop):
        wave.append(Unit("Hoplite","Heavy Infantry",56,1,1,18))

    for i in range(sg):
        wave.append(Unit("Steam Giant","Heavy Infantry",184,3,3,42))

    for i in range(sword):
        wave.append(Unit("Swordsman","Light Infantry",18,0,1,10))
    
    for i in range(spear):
        wave.append(Unit("Spearman","Light Infantry",13,0,1,4))

    for i in range(gun):
        wave.append(Unit("Sulfur Carabineer","Long-Range Fighter",12,0,4,3,29,3))
    for i in range(archer):
        wave.append(Unit("Archer","Long-Range Fighter",16,0,1,5,5,3))
    for i in range(slinger):
        wave.append(Unit("Slinger","Long-Range Fighter",8,0,1,2,3,5))

    for i in range(ram):
        wave.append(Unit("Ram","Artillery",88,1,5,12,80,-1))
    for i in range(cata):
        wave.append(Unit("Catapult","Artillery",54,0,5,4,133,5))
    for i in range(mortar):
        wave.append(Unit("Mortar","Artillery",32,0,5,10,270,3))

    for i in range(gyro):
        wave.append(Unit("Gyrocopter","Fighter Pilot",29,0,1,0,17,4))
        
    for i in range(balloon):
        wave.append(Unit("Balloon-Bombardier","Bomber",40,0,2,0,48,2))
    
    for i in range(spartan):
        wave.append(Unit("Spartan","Heavy Infantry",60,6,1,28))

    for i in range(min(wall,7)):
        #TODO implement wall levels. now wall is level20
        wave.append(Unit("Town wall","Wall",1100,80,-1,250))
    
    return Wave(wave)
    
    
def generate_sea_wave(ram=0,fire=0,steam=0,ballista=0,cata=0,mortar=0,rocket=0,dive=0,paddle=0,carrier=0,tender=10):
    wave : batch = []
    #TODO

def generate_land_field()


'''
locations = {
        "mainline": Location(5, 30, [73, 74], strongest=False),
        "ranged": Location(5, 30, [75], strongest=True),
        "artillery": Location(2, 30, [76], strongest=True),
        "flank": Location(2, 30, [74], strongest=True),
        "air": Location(1, 20, [78], strongest=False),
        "air_fighter": Location(1, 20, [77], strongest=True),
        "support": Location(1, 10, [79], strongest=True, hide=True),
        "transporter": Location(0, 0, [79], strongest=True, hide=True)
    }
'''

#main battle


'''
steps of rounds (both sides simultaneously): 
    collect all waves on both sides
    populate slots with units
    populate field with slots
    realize attack order
    loop until no more formations to attack with:
        create a batch of targets, based on unit.atk_seq
        loop until no more units to attack with:
            if attacker not alive continue to next attacker
            get first element of batch of targets
            current unit shoots target
            if enemy dies move it from target batch to dead batch
            go to next unit
        loop thru dead batch:
            realize damage, update enemy units
            ...
        go to next formation
    redistribute damage
            


1. Initialize:
    Collect waves of units for both sides.
    Populate slots in the battlefield for each unit type according to available spaces.

2. Battlefield Setup:
    Assign units to their designated battlefield formations (e.g., frontline, flanks, ranged).
    Populate these formations based on unit type and battlefield size (i.e., heavy infantry fills frontline first).

3. Resolve Attack Order:
    Follow the attack sequence: Air units, Bombers, Artillery, Long-range units, Frontline, and Flanks.
    For each formation:
        Create Target Batch: Based on each unit's preferred target sequence (stored in unit.atk_seq).
        Attack Loop: Loop through attacking units.
            If an attacker is alive, target the first element in the batch.
            Execute attack: Apply damage, considering armor and other modifiers.
            If the target dies, remove it from the batch, marking it as “dead.”

4. Process Casualties:
    After each formation's attacks, update units in the “dead batch,” officially marking them as casualties.
    Adjust morale or other metrics if morale-boosting or -reducing effects are present.

5. Damage Redistribution:
    Redistribute excess damage across remaining units according to Reserve-Redistribution (RR), Slot-Redistribution (SR), and Immediate-Redistribution (IR) rules.

6. End Round:
    Check if either side’s frontline has broken or morale is too low. If so, end the battle.
    If both sides are still standing, start the next round.
'''




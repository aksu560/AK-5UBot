# -*- coding: utf-8 -*-
class spirit:

    def __init__(self, force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills, powers,
                 opt_powers, meat_init, astral_init, stype, source, special="", weakness=""):
        self.force = int(force)
        self.body = int(body)
        self.agility = int(agility)
        self.reaction = int(reaction)
        self.strength = int(strength)
        self.willpower = int(willpower)
        self.logic = int(logic)
        self.intuition = int(intuition)
        self.charisma = int(charisma)
        self.magic = int(force)
        self.essence = int(force)
        self.edge = force // 2 + (force % 2 > 0)
        self.skills = skills
        self.powers = list(powers)
        self.powers.sort()
        self.opt_powers = list(opt_powers)
        self.opt_powers.sort()
        self.type = stype
        self.weakness = weakness
        self.special = special
        self.meat_initiative = meat_init
        self.astral_initiative = astral_init
        self.source = source

        self.attributes = []

        for a in self.__dict__:
            if not a.startswith("__") and not a.endswith("__"):
                self.attributes.append(a)

        for a in self.attributes:
            try:
                b = int(self.__dict__[a])
            except ValueError:
                break
            if b < 1:
                self.__dict__[a] = 1

        if self.edge < 1:
            self.edge = 1

    def __str__(self):

        self.output = '```css\n' \
            f'Type: {self.type}\n' \
            f'Force: {self.force}\n' \
            f'Body: {self.body}\n' \
            f'Agility: {self.agility}\n' \
            f'Reaction: {self.reaction}\n' \
            f'Strength: {self.strength}\n' \
            f'Willpower: {self.willpower}\n' \
            f'Logic: {self.logic}\n' \
            f'Intuition: {self.intuition}\n' \
            f'Charisma: {self.charisma}\n' \
            f'Magic: {self.magic}\n' \
            f'Essence: {self.essence}\n' \
            f'Edge: {self.edge}\n' \
            f'Initiative: {self.meat_initiative}\n' \
            f'Astral Initiative: {self.astral_initiative}\n\n' \
            f'Skills: {", ".join(self.skills)}\n' \
            f'Powers: {", ".join(self.powers)}\n' \
            f'Optional Powers: {", ".join(self.opt_powers)}\n'

        if self.weakness != "":
            self.output += f'Weakness: {self.weakness}\n'

        if self.special != "":
            self.output += f'Special: {self.special}\n'

        self.output += f'Source: {self.source}\n'
        self.output += "```"

        return self.output


class basic(spirit):
    def __init__(self, force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills, powers,
                 opt_powers, meat_init, astral_init, source, special="", weakness="", **kwargs):
        self.stype = "Basic"
        self.powers = powers
        self.powers.extend(["Materialization", "Sapience", "Astral Form"])
        self.skills = skills
        self.skills.extend(["Assensing", "Astral Combat", "Perception", "Unarmed Combat"])

        super().__init__(force, body, agility, reaction, strength, willpower, logic, intuition, charisma, self.skills,
                         self.powers, opt_powers, meat_init, astral_init, self.stype, source, special, weakness)


class air(basic):
    def __init__(self, force, **kwargs):
        self.force = force
        self.body = self.force - 2
        self.agility = self.force + 3
        self.reaction = self.force + 4
        self.strength = self.force - 3
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 4}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon", "Running"]
        self.powers = ["Accident", "Concealment", "Confusion", "Engulf", "Movement", "Search"]
        self.opt_powers = ["Elemental Attack", "Energy Aura", "Fear", "Guard", "Noxious Breath", "Psychokinesis"]
        self.special = "Spirits of Air get +10 meters per hit when Sprinting"
        self.source = "CRB:303"

        if 'mental_reduction' in kwargs:
            self.mental_reduction = kwargs["mental_reduction"]
            self.willpower -= self.mental_reduction
            self.logic -= self.mental_reduction
            self.intuition -= self.mental_reduction
            self.charisma -= self.mental_reduction

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source, self.special)


class airelemental(air):
    def __init__(self, force):
        self.force = force
        self.mental_reduction = int(self.force/2)

        super().__init__(self.force, mental_reduction=self.mental_reduction)


class beasts(basic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 2
        self.agility = self.force + 1
        self.reaction = self.force
        self.strength = self.force + 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = []
        self.powers = ["Animal Control", "Astral Form", "Enhanced Senses(Hearing, Low-Light Vision, Smell)", "Fear",
                       "Movement"]
        self.opt_powers = ["Concealment", "Confusion", "Guard", f"Natural Weapon(Drain = {self.force} Physical damage, AP-)",
                           "Noxious breath", "Search", "Venom"]
        self.source = "CRB:303"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class earth(basic):
    def __init__(self, force, **kwargs):
        self.force = force
        self.body = self.force + 4
        self.agility = self.force - 2
        self.reaction = self.force - 1
        self.strength = self.force + 4
        self.willpower = self.force
        self.logic = self.force - 1
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 - 1}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon", ]
        self.powers = ["Astral Form", "Binding", "Guard", "Movement", "Search"]
        self.opt_powers = ["Concealment", "Confusion", "Engulf", "Elemental Attack", "Fear"]
        self.source = "CRB:303"

        if 'mental_reduction' in kwargs:
            self.mental_reduction = kwargs["mental_reduction"]
            self.willpower -= self.mental_reduction
            self.logic -= self.mental_reduction
            self.intuition -= self.mental_reduction
            self.charisma -= self.mental_reduction

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class earthelemental(air):
    def __init__(self, force):
        self.force = force
        self.mental_reduction = int(self.force/2)

        super().__init__(self.force, mental_reduction=self.mental_reduction)


class fire(basic):
    def __init__(self, force, **kwargs):
        self.force = force
        self.body = self.force + 1
        self.agility = self.force + 2
        self.reaction = self.force + 3
        self.strength = self.force - 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force + 1
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 3}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon"]
        self.powers = ["Accident", "Astral Form", "Confusion", "Elemental Attack", "Energy Aura", "Engulf"]
        self.opt_powers = ["Fear", "Guard", "Noxious Breath", "Search"]
        self.special = "Spirits of Fire get +5 meters per hit when Sprinting"
        self.weakness = "Allergy(Water, Severe)"
        self.source = "CRB:303"

        if 'mental_reduction' in kwargs:
            self.mental_reduction = kwargs["mental_reduction"]
            self.willpower -= self.mental_reduction
            self.logic -= self.mental_reduction
            self.intuition -= self.mental_reduction
            self.charisma -= self.mental_reduction

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source, self.special)


class fireelemental(air):
    def __init__(self, force):
        self.force = force
        self.mental_reduction = int(self.force/2)

        super().__init__(self.force, mental_reduction=self.mental_reduction)


class man(basic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 1
        self.agility = self.force
        self.reaction = self.force + 2
        self.strength = self.force - 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force + 1
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Spellcasting"]
        self.powers = ["Accident", "Concealment", "Confusion", "Enhanced Senses(Low-Light, Thermographic Vision)",
                       "Guard", "Influence", "Search"]
        self.opt_powers = ["Fear", "Movement", "Psychokinesis",
                           "Innate Spell(any one spell known by the summoner; Force is limited to spirits magic)"]
        self.source = "CRB:304"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class water(basic):
    def __init__(self, force, **kwargs):
        self.force = force
        self.body = self.force
        self.agility = self.force + 1
        self.reaction = self.force + 2
        self.strength = self.force
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon"]
        self.powers = ["Concealment", "Confusion", "Engulf", "Movement", "Search"]
        self.opt_powers = ["Accident", "Binding", "Elemental Attack", "Energy Aura", "Guard", "Weather Control"]
        self.weakness = "Allergy(Fire, Severe)"
        self.special = "Spirits of Water move twice as fast when in water."
        self.source = "CRB:304"

        if 'mental_reduction' in kwargs:
            self.mental_reduction = kwargs["mental_reduction"]
            self.willpower -= self.mental_reduction
            self.logic -= self.mental_reduction
            self.intuition -= self.mental_reduction
            self.charisma -= self.mental_reduction

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


class waterelemental(air):
    def __init__(self, force):
        self.force = force
        self.mental_reduction = int(self.force/2)

        super().__init__(self.force, mental_reduction=self.mental_reduction)


class guardian(basic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 1
        self.agility = self.force + 2
        self.reaction = self.force + 3
        self.strength = self.force + 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 1}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Blades", "Clubs", "Counterspelling", "Exotic Ranged Weapon"]
        self.powers = ["Fear", "Guard", "Magical Guard", "Movement"]
        self.opt_powers = ["Animal Control", "Concealment", f"Natural Weaponry(DV = {self.force + 2})", "Psychokinesis",
                           "Skill(Choose any combat skill)",
                           "Elemental Attack(Summoner chooses element during summoning)"]
        self.source = "SG:193"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class guidance(basic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 3
        self.agility = self.force - 1
        self.reaction = self.force + 2
        self.strength = self.force + 1
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Arcana", "Counterspelling"]
        self.powers = ["Confusion", "Divining", "Guard", "Magical Guard", "Search", "Shadow Cloak"]
        self.opt_powers = ["Engulf", "Enhanced Senses(Hearing, Low-Light Vision, Thermographic Vision, or Smell)",
                           "Fear", "Influence"]
        self.source = "SG:193"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class plant(basic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 2
        self.agility = self.force - 1
        self.reaction = self.force
        self.strength = self.force + 1
        self.willpower = self.force
        self.logic = self.force - 1
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Counterspelling", "Exotic Ranged Weapon"]
        self.powers = ["Concealment", "Engulf", "Fear", "Guard", "Magical Guard"]
        self.opt_powers = ["Accident", "Confusion", "Movement", "Noxius Breath", "search"]
        self.source = "SG:193"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class task(basic):
    def __init__(self, force):
        self.force = force
        self.body = self.force
        self.agility = self.force
        self.reaction = self.force + 2
        self.strength = self.force + 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Artisan"]
        self.powers = ["Accident", "Binding", "Movement", "Search"]
        self.opt_powers = ["Concealment", "Enhanced Senses (Hearing, Low-Light Vision, Thermographic Vision, or Smell)",
                           "Influence", "Psychokinesis", "Skill (Choose any Technical or Physical skill)"]
        self.source = "SG:193"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class toxic(spirit):
    def __init__(self, force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills, powers,
                 opt_powers, meat_init, astral_init, source, special="", weakness=""):
        self.stype = "Toxic"
        self.powers = powers
        self.powers.extend(["Materialization", "Sapience", "Astral Form"])
        self.skills
        self.skills.extend(["Assensing", "Astral Combat", "Perception", "Unarmed Combat"])

        super().__init__(force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills,
                         powers,
                         opt_powers, meat_init, astral_init, self.stype, source, special, weakness)


class noxius(toxic):
    def __init__(self, force):
        self.force = force
        self.body = self.force - 2
        self.agility = self.force + 3
        self.reaction = self.force + 4
        self.strength = self.force - 3
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 4}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon", "Running"]
        self.powers = ["Accident", "Concealment", "Confusion", "Engulf(Air)", "Movement", "Search"]
        self.opt_powers = ["Fear", "Guard", "Noxius Breath", "Psychokinesis", "Weather Control"]
        self.source = "SG:87"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class abomination(toxic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 2
        self.agility = self.force + 1
        self.reaction = self.force
        self.strength = self.force + 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon", "Gymnastics", "Running"]
        self.powers = ["Animal Control (Toxic Critters)", "Enhanced Senses (Hearing, Low-Light Vision, Smell)",
                       "Movement", "Mutagen", f"Natural Weapon (DV = ({self.force}) Physical damage,AP —)", "Pestilence"]
        self.opt_powers = ["Concealment", "Corrosive Spit", "Fear", "Guard", "Mimicry", "Search", "Venom"]
        self.source = "SG:87"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source)


class barren(toxic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 4
        self.agility = self.force - 2
        self.reaction = self.force - 1
        self.strength = self.force + 4
        self.willpower = self.force
        self.logic = self.force - 1
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 - 1}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon"]
        self.powers = ["Binding", "Elemental Attack(Pollutant)", "Engulf(Earth)", "Movement", "Search"]
        self.opt_powers = ["Accident", "Concealment", "Confusion", "Fear", "Guard"]
        self.weakness = "Allergy(Clean Earth, Severe)"
        self.special = ""
        self.source = "SG:88"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


class nuclear(toxic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 1
        self.agility = self.force + 2
        self.reaction = self.force + 3
        self.strength = self.force - 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force + 1
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 3}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon", "Flight"]
        self.powers = ["Elemental Attack(Radiation)", "Energy Aura(Radiation)", "Enguf(Fire)"]
        self.opt_powers = ["Confusion", "Fear", "Guard", "Search"]
        self.source = "SG:88"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source)


class plague(toxic):
    def __init__(self, force):
        self.force = force
        self.body = self.force
        self.agility = self.force
        self.reaction = self.force + 2
        self.strength = self.force - 2
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force + 1
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Spellcasting"]
        self.powers = ["Accident", "Desire Reflection", "Enhanced Senses (Low-Light, Thermographic Vision)", "Fear",
                       "Mutagen", "Pestilence", "Search"]
        self.opt_powers = ["Confusion", "Fear", "Guard", "Search"]
        self.source = "SG:88"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source)


class sludge(toxic):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 1
        self.agility = self.force + 1
        self.reaction = self.force + 2
        self.strength = self.force
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Exotic Ranged Weapon"]
        self.powers = ["Binding", "Elemental Attack(Pollutant)", "Engulf(Water)", "Movement", "Mutagen", "Search"]
        self.opt_powers = ["Accident", "Concealment", "Confusion", "Fear", "Guard"]
        self.source = "SG:88"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source)


class blood(spirit):
    def __init__(self, force):
        self.stype = "Blood"
        self.force = force
        self.body = self.force + 2
        self.agility = self.force + 2
        self.reaction = self.force
        self.strength = self.force + 2
        self.willpower = self.force
        self.logic = self.force - 1
        self.intuition = self.force + 1
        self.charisma = self.force
        self.meat_initiative = f"{force * 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Assensing", "Astral Combat", "Perception", "Running", "Unarmed Combat"]
        self.powers = ["Astral Form", "Binding", "Energy Drain(Essence, Touch, Physical Damage)", "Fear",
                       "Materialization"]
        self.opt_powers = ["Concealment", "Confusion", "Guard", "Movement", "Noxious breath",
                           f"Natural Weapon(DV=({self.force}) Physical Damage, AP-)"]
        self.weakness = "Essence Loss (1 point per day)"
        self.special = ""
        self.source = "SG:88"

        super().__init__(self.force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.stype, self.source, self.special, self.weakness)


class shadow(spirit):
    def __init__(self, force, powers):
        self.stype = "Shadow"
        self.force = force
        self.body = self.force
        self.agility = self.force + 3
        self.reaction = self.force + 2
        self.strength = self.force
        self.willpower = self.force + 1
        self.logic = self.force
        self.intuition = self.force + 1
        self.charisma = self.force + 2
        self.meat_initiative = f"{force * 2 + 3}+2d6"
        self.astral_initiative = f"{force * 2 + 1}+3d6"
        self.powers = powers
        self.powers.extend(
            ["Astral Form", "Banishing Resistance", "Energy Drain(Karma, LOS, Stun Damage)", "Influence",
             "Magical Guard", "Materialization", "Sapience", "Spirit Pact"])
        self.skills = ["Assensing", "Astral Combat", "Con", "Gymnastics", "Intimidation", "Perception",
                       "Unarmed Combat"]
        self.source = "SG:92"

        super().__init__(self.force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers, self.meat_initiative,
                         self.astral_initiative, self.stype, self.source, self.special, self.weakness)


class muse(shadow):
    def __init__(self, force):
        self.powers = ["Compulsion(Creation)", "Mind Link", "Realistic Form"]

        super().__init__(force, self.powers)


class nightmare(shadow):
    def __init__(self, force):
        self.powers = ["Fear", "Mind Link", "Shadow Cloak"]

        super().__init__(force, self.powers)


class shade(shadow):
    def __init__(self, force):
        self.powers = ["Compulsion(Sorrow)", "Shadow Cloak", "Silence"]

        super().__init__(force, self.powers)


class succubus(shadow):
    def __init__(self, force):
        self.powers = ["Compulsion(Lust)", "Desire Reflection", "Mutable Form", "Realistic Form"]

        super().__init__(force, self.powers)


class wraith(shadow):
    def __init__(self, force):
        self.powers = ["Compulsion(Homicidal Rage)", "Confusion", "Fear"]

        super().__init__(force, self.powers)


class Shedim(spirit):
    def __init__(self, force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills, powers,
                 opt_powers, meat_init, astral_init, source, special="", weakness=""):
        self.stype = "Shedim"
        self.powers = powers
        self.powers.extend(["Sapience", "Energy Drain(Karma, Touch Range, Physical Damage)", "Fear",
                                     "Immunity(Age, Pathogens, Toxins)", "Possession(Dead or Abandoned Vessels)"])
        self.skills = skills
        self.skills.extend(["Assensing", "Astral Combat", "Perception", "Unarmed Combat"])

        super().__init__(force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills,
                         powers,
                         opt_powers, meat_init, astral_init, self.stype, source, special, weakness)


class shedim(Shedim):
    def __init__(self, force):
        self.force = force
        self.body = self.force
        self.agility = self.force
        self.reaction = self.force + 2
        self.strength = self.force + 1
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = []
        self.powers = ["Paralyzing Touch"]
        self.opt_powers = ["Accident", "Aura Masking", "Compulsion", "Regeneration", "Search", "Shadow Cloak"]
        self.source = "SG:93"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source)


class master_shedim(Shedim):
    def __init__(self, force):
        self.force = force
        self.body = self.force
        self.agility = self.force
        self.reaction = self.force + 2
        self.strength = self.force + 1
        self.willpower = self.force + 1
        self.logic = self.force + 1
        self.intuition = self.force + 1
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 3}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Counterspelling", "Gymnastics", "Spellcasting"]
        self.powers = ["Astral Gateway", "Aura Masking", "banishing Resistance", "Compulsion", "Deathly Aura",
                       "Regeneration", "Shadow Cloak", "Spirit Pact"]
        self.opt_powers = ["Accident", "Noxious Breath", "Search", "Silence"]
        self.source = "SG:93"

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source)


class bug(spirit):
    def __init__(self, force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills, powers,
                 opt_powers, meat_init, astral_init, source, special="", weakness=""):
        self.stype = "Bug"
        self.powers = powers
        self.powers.extend(["Animal Control(Insect Type)", "Astral Form", "Hive Mind"])
        self.skills = skills
        self.skills.extend(["Assensing", "Astral Combat", "Perception", "Unarmed Combat"])
        self.weakness = "Allergy (Insecticides, Severe)" + weakness

        super().__init__(force, body, agility, reaction, strength, willpower, logic, intuition, charisma, skills,
                         powers,
                         opt_powers, meat_init, astral_init, self.stype, source, special, weakness)


class caretaker(bug):
    def __init__(self, force):
        self.force = force
        self.body = self.force
        self.agility = self.force + 1
        self.reaction = self.force + 1
        self.strength = self.force
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 1}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Leadership"]
        self.powers = ["Guard", "Innate Spell(Physical Barrier)"]
        self.opt_powers = ["Binding", "Confusion", "Enhanced Senses(Smell, Thermographic Vision, or Ultrasound)"]
        self.source = "SG:98"
        self.weakness = "Evanescence"
        self.special = ""

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


class nymph(bug):
    def __init__(self, force):
        self.force = force
        self.body = self.force - 1
        self.agility = self.force
        self.reaction = self.force + 3
        self.strength = self.force - 1
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 3}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Gymnastics", "Spellcasting"]
        self.powers = ["Enhanced Senses(Smell, Thermographic Vision, or Ultrasound)",
                       "Innate Spell(Any Spell known to the summoner)"]
        self.opt_powers = ["Compulsion", "Fear"]
        self.source = "SG:98"
        self.weakness = "Evanescence"
        self.special = ""

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


class scout(bug):
    def __init__(self, force):
        self.force = force
        self.body = self.force
        self.agility = self.force + 2
        self.reaction = self.force + 2
        self.strength = self.force
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Gymnastics", "Sneaking"]
        self.powers = ["Concealment", "Enhanced Senses(Smell, Thermographic Vision, or Ultrasound)", "Movement",
                       "Search"]
        self.opt_powers = ["Confusion", "Guard", f"Natural Weapon(DV=({self.force}) Physical Damage, AP 0)", "Noxious Breath"]
        self.source = "SG:98"
        self.weakness = "Evanescence"
        self.special = ""

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


class soldier(bug):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 3
        self.agility = self.force + 1
        self.reaction = self.force + 1
        self.strength = self.force + 3
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 1}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Counterspelling", "Exotic Ranged Weapon", "Gymnastics"]
        self.powers = ["Enhanced Senses(Smell, Thermographic Vision)", "Movement"]
        self.opt_powers = ["Concealment", "Enhanced Senses(Ultrasound)",
                           "Skill (a worker spirit may be given additional Technical or Physical skill instead of an "
                           "optional power))", "Venom"]
        self.source = "SG:98"
        self.weakness = "Evanescence"
        self.special = ""

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


class worker(bug):
    def __init__(self, force):
        self.force = force
        self.body = self.force
        self.agility = self.force
        self.reaction = self.force
        self.strength = self.force + 1
        self.willpower = self.force
        self.logic = self.force
        self.intuition = self.force
        self.charisma = self.force
        self.meat_initiative = f"{force * 2}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Counterspelling", "Exotic Ranged Weapon", "Gymnastics"]
        self.powers = ["Enhanced Senses(Smell, Thermographic Vision)", "Movement"]
        self.opt_powers = ["Concealment", "Enhanced Senses(Ultrasound)",
                           "Skill (a worker spirit may be given additional Technical or Physical skill instead of an "
                           "optional power))", "Venom"]
        self.source = "SG:98"
        self.weakness = "Evanescence"
        self.special = ""

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


class queen(bug):
    def __init__(self, force):
        self.force = force
        self.body = self.force + 5
        self.agility = self.force + 3
        self.reaction = self.force + 4
        self.strength = self.force + 5
        self.willpower = self.force + 1
        self.logic = self.force + 1
        self.intuition = self.force + 1
        self.charisma = self.force
        self.meat_initiative = f"{force * 2 + 5}+2d6"
        self.astral_initiative = f"{force * 2}+3d6"
        self.skills = ["Con", "Counterspelling", "Gymnastics", "Leadership", "Negotiation", "Spellcasting"]
        self.powers = ["Astral Gateway", "banishing Resistance", "Compulsion",
                       "Enhanced Senses(Smell, Thermographic Vision, or Ultrasound)", "Fear", "Search", "Spirit Pact",
                       "Wealth"]
        self.opt_powers = ["Concealment", "Guard", "Noxious Breath",
                           f"Natural Weapon (DV =({self.force + 3}) Physical damage, AP –1)", "Venom"]
        self.source = "SG:98"
        self.weakness = "Evanescence"
        self.special = ""

        super().__init__(force, self.body, self.agility, self.reaction, self.strength, self.willpower, self.logic,
                         self.intuition, self.charisma, self.skills, self.powers, self.opt_powers,
                         self.meat_initiative,
                         self.astral_initiative, self.source, self.special, self.weakness)


spirit.index = {
    "air": air,
    "beast": beasts,
    "earth": earth,
    "fire": fire,
    "guardian": guardian,
    "guidance": guidance,
    "man": man,
    "plant": plant,
    "task": task,
    "water": water,
    "noxius": noxius,
    "abomination": abomination,
    "barren": barren,
    "nuclear": nuclear,
    "plague": plague,
    "sludge": sludge,
    "blood": blood,
    "muse": muse,
    "nightmare": nightmare,
    "shade": shade,
    "succubus": succubus,
    "wraith": wraith,
    "shedim": shedim,
    "master": master_shedim,
    "caretaker": caretaker,
    "nymph": nymph,
    "scout": scout,
    "soldier": soldier,
    "worker": worker,
    "queen": queen,
    "airelemental": airelemental,
    "earthelemental": fireelemental,
    "fireelemental": fireelemental,
    "waterelemental": waterelemental
}

"""
    This file is part of tolyn.

    tolyn is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from enum import Enum, unique, auto


@unique
class Tag(Enum):
    """
    Everything is a tag.
    """

    NIGHT_OF_THE_ZEALOT = auto()

    PLAYER = auto()
    INVESTIGATOR = auto()
    ASSET = auto()
    EVENT = auto()
    SKILL = auto()
    LOCATION = auto()

    GUARDIAN = auto()
    SEEKER = auto()
    MYSTIC = auto()
    ROGUE = auto()
    SURVIVOR = auto()

    NEUTRAL = auto()

    BASIC_WEAKNESS = auto()
    WEAKNESS = auto()
    TREACHERY = auto()
    ELITE = auto()

    ENEMY = auto()
    GHOUL = auto()
    HAZARD = auto()
    HUNTER = auto()
    HUMANOID = auto()
    OMEN = auto()
    MONSTER = auto()
    TERROR = auto()
    RETALIATE = auto()

    ALLY = auto()
    ARMOR = auto()
    CHARM = auto()
    CREATURE = auto()
    CRIMINAL = auto()
    FIREARM = auto()
    FORTUNE = auto()
    ILLICIT = auto()
    INNATE = auto()
    INSIGHT = auto()
    ITEM = auto()
    MELEE = auto()
    PRACTICED = auto()
    RELIC = auto()
    SCIENCE = auto()
    SORCERER = auto()
    SPELL = auto()
    SPIRIT = auto()
    SUPPLY = auto()
    TACTIC = auto()
    TALENT = auto()
    TOOL = auto()
    WEAPON = auto()

    AMMO = auto()
    CHARGE = auto()
    CLUE = auto()
    DOOM = auto()
    RESOURCE = auto()
    SECRET = auto()

    HEALTH = auto()
    HORROR = auto()
    COST = auto()

    AGILITY = auto()
    COMBAT = auto()
    INTELLECT = auto()
    WILLPOWER = auto()
    WILDCARD = auto()

    BODY_SLOT = auto()
    ALLY_SLOT = auto()
    ACCESSORY_SLOT = auto()
    HAND_LEFT_SLOT = auto()
    HAND_RIGHT_SLOT = auto()
    HAND_BOTH_SLOT = auto()
    ARCANE_1_SLOT = auto()
    ARCANE_2_SLOT = auto()
    ARCANE_BOTH_SLOT = auto()


CAMPAIGNS = {Tag.NIGHT_OF_THE_ZEALOT}
CARD_TOKENS = {Tag.AMMO, Tag.CHARGE, Tag.CLUE, Tag.DOOM, Tag.HEALTH, Tag.HORROR, Tag.RESOURCE, Tag.SECRET, }
SKILL_TAGS = {Tag.AGILITY, Tag.COMBAT, Tag.INTELLECT, Tag.WILDCARD, Tag.WILLPOWER }
SLOT_TAGS = {Tag.ACCESSORY_SLOT, Tag.ALLY_SLOT, Tag.ARCANE_1_SLOT, Tag.ARCANE_2_SLOT, Tag.ARCANE_BOTH_SLOT, Tag.BODY_SLOT, Tag.HAND_BOTH_SLOT, Tag.HAND_LEFT_SLOT, Tag.HAND_RIGHT_SLOT}


class Card:
    """
    Represents a card of AH LCG
    """
    KWARGS_TAKE_VALUE = {'title', 'subtitle', 'description', 'campaign_index', 'campaign_subindex', 'campaign_subindex_of'}
    CARDS = dict()

    def __new__(cls, *args, **kwargs):
        campaign_index = kwargs.get('campaign_index')
        campaign: set[Tag] = {tag for tag in args if tag in CAMPAIGNS}
        if campaign is None or campaign_index is None or len(campaign) != 1:
            raise ValueError('Card can not be created if campaign_index and/or campaign are not filled in correctly')
        card_index = f"{campaign.pop().name}_{campaign_index}"
        card = cls.CARDS.get(card_index, None)
        if card is None:
            card = super().__new__(cls)
            cls.CARDS[card_index] = card
            return card
        else:
            raise ValueError(f'Card {args} {kwargs} already exists')

    def __init__(self, *args, **kwargs):

        self.title = None
        self.subtitle = None
        self.description = None
        self.campaign_index = None
        self.campaign_subindex = None
        self.campaign_subindex_of = None
        self.exhausted = False
        self.flipped = False
        self.counters = {tag: 0 for tag in CARD_TOKENS}
        self.thresholds = {tag: 0 for tag in CARD_TOKENS}
        self.linked_cards = []
        self.tags = {tag for tag in args if isinstance(tag, Tag)}

        for key, value in kwargs.items():
            if key in Card.KWARGS_TAKE_VALUE:
                setattr(self, key, value)
                continue
            if key.startswith("T_"):
                key = key[2:]
                target = self.thresholds
            else:
                target = self.counters
            key = Tag[key]
            target[key] = value

    def __repr__(self):
        return f"{vars(self)}"

    def add_token(self, tag: Tag, counter=1):
        if tag in CARD_TOKENS:
            self.counters[tag] += counter

    def remove_token(self, tag: Tag, counter=1):
        self.add_token(tag, -counter)

    def exhaust(self):
        self.exhausted = True

    def ready(self):
        self.exhausted = False

    def flip(self):
        self.flipped = True

    def unflip(self):
        self.flipped = False


class InvestigatorCard(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(Tag.INVESTIGATOR, *args, **kwargs)

    def __repr__(self):
        return f"Player {self.title} - {self.subtitle} -   --  HEALTH:{self.counters[Tag.HEALTH]}/{self.thresholds[Tag.HEALTH]} | HORROR: {self.counters[Tag.HORROR]}/{self.thresholds[Tag.HORROR]}  --  W:{self.counters[Tag.WILLPOWER]} I:{self.counters[Tag.INTELLECT]} C:{self.counters[Tag.COMBAT]} A:{self.counters[Tag.AGILITY]}  "


class PlayerCard(Card):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        card_types: set[Tag] = {tag for tag in args if tag in (tag.ASSET, Tag.EVENT, Tag.SKILL)}
        if len(card_types) != 1:
            raise ValueError("A player card must be exactly one of these tags: ASSET, EVENT, SKILL")
        self.card_type = card_types.pop()

    def __repr__(self):
        skill_text = ", ".join([f'{tag.name}={counter}' for tag, counter in self.counters.items() if tag in SKILL_TAGS and counter > 0])
        return f"PlayerCard {self.title} ({self.subtitle})  {self.card_type.name} ({self.counters[Tag.COST]}) -- {skill_text}"


class Deck(list[Card]):
    def __init__(self):
        list.__init__(self)


if __name__ == "__main__":
    Agnes = InvestigatorCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.SEEKER, Tag.SORCERER, campaign_index=3, title="Agnes Baker", subtitle="The Waitress", T_HEALTH=6, T_HORROR=8, WILLPOWER=5, INTELLECT=2, COMBAT=2, AGILITY=3)
    Skids = InvestigatorCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.CRIMINAL, campaign_index=4, title="\"Skids\" O\'Toole", subtitle="The Ex-Con", T_HEALTH=8, T_HORROR=7, WILLPOWER=2, INTELLECT=3, COMBAT=3, AGILITY=4)
    Scavaging = PlayerCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.NEUTRAL, Tag.PLAYER, Tag.TALENT, Tag.ASSET, campaign_index=73, INTELLECT=1, title="Scavaging")
    DarkMemory = PlayerCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.SPELL, Tag.EVENT, Tag.WEAKNESS, campaign_index=13, title="Dark Memory", subtitle="No... not again!")
    Heirloom = PlayerCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.NEUTRAL, Tag, Tag.ITEM, Tag.SPELL, Tag.ASSET, Tag.ACCESSORY_SLOT, campaign_index=12, title= "Heirloom of Hyperborea", subtitle="Artefact from another life", INTELLECT=1, COMBAT=1, WILDCARD=1, COST =3)
    print(Heirloom)

from enum import Enum, unique, auto


@unique
class Tag(Enum):
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

    AGILITY = auto()
    COMBAT = auto()
    INTELLECT = auto()
    WILLPOWER = auto()

    BODY = auto()
    ALLY  = auto()
    ACCESSORY = auto()
    HAND_LEFT  = auto()
    HAND_RIGHT = auto()
    HAND_BOTH = auto()
    ARCANE_1  = auto()
    ARCANE_2 =  auto()
    ARCANE_BOTH= auto()


CAMPAIGNS = {Tag.NIGHT_OF_THE_ZEALOT}
CARD_TOKENS = {Tag.AMMO, Tag.CHARGE, Tag.CLUE, Tag.DOOM, Tag.HEALTH, Tag.HORROR, Tag.RESOURCE, Tag.SECRET, }


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
    # def __repr__(self):
    #     return f"Player {self.title} ({self.subtitle}) --  HEALTH:{self.counters[Tag.HEALTH]}/{self.thresholds[Tag.HEALTH]} | HORROR: {self.counters[Tag.HORROR]}/{self.thresholds[Tag.HORROR]}  --  W:{self.counters[Tag.WILLPOWER]} I:{self.counters[Tag.INTELLECT]} C:{self.counters[Tag.COMBAT]} A:{self.counters[Tag.AGILITY]}  "
    pass


class Deck(list[Card]):
    def __init__(self):
        list.__init__(self)


if __name__ == "__main__":
    Agnes = InvestigatorCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.SEEKER, Tag.SORCERER, campaign_index=3, title="Agnes Baker", subtitle="The Waitress", T_HEALTH=6, T_HORROR=8, WILLPOWER=5, INTELLECT=2, COMBAT=2, AGILITY=3)
    Skids = InvestigatorCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.CRIMINAL, campaign_index=4, title="\"Skids\" O\'Toole", subtitle="The Ex-Con", T_HEALTH=8, T_HORROR=7, WILLPOWER=2, INTELLECT=3, COMBAT=3, AGILITY=4)
    Scavaging = PlayerCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.NEUTRAL, Tag.PLAYER, Tag.TALENT, Tag.ASSET, campaign_index=73, INTELLECT=1, title="Scavaging")
    DarkMemory = PlayerCard(Tag.NIGHT_OF_THE_ZEALOT, Tag.SPELL, Tag.EVENT, Tag.WEAKNESS, campaign_index=13, title="Dark Memory", subtitle="No... not again!")
    print(Agnes)
    print(Skids)
    print('COMBAT' in Tag)
    print('EE' in Tag)
    print(Card.CARDS)

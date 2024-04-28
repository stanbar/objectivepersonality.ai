import re
from dataclasses import dataclass

PATTERN = re.compile(
    r"([FMx?])([FMx?])-([SNFTx?][iex])\/([SNFTx?][iex])-([SPBCx?])([SPBCx?])\/([SPBCx?])\(([SPBCx?])\)(?: \[(\d)\])?"
)

MASCULINE = "M"
FEMININE = "F"
INTRO = "Intro"
EXTRO = "Extro"
ENERGY = "Energy"
INFO = "Info"
CONSUME = "Consume"
BLAST = "Blast"
SLEEP = "Sleep"
PLAY = "Play"
THINKING = "T"
FEELING = "F"
INTUITION = "N"
SENSING = "S"
OI = "Oi"
OE = "Oe"
DE = "De"
DI = "Di"
OBSERVER = "Observer"
DECIDER = "Decider"
SPECIALISATION = "Specialisation"
GENERALISATION = "Generalisation"
FLEX = "Flex"
FRIENDS = "Friends"

mSeCoin = "mSe"
mDeCoin = "mDe"
ObserverDeciderCoin = OBSERVER + DECIDER
DiDeCoin = DI + DE
OiOeCoin = OI + OE
SNCoin = SENSING + INTUITION
TFCoin = THINKING + FEELING
SleepPlayCoin = SLEEP + PLAY
BlastConsumeCoin = BLAST + CONSUME
InfoEnergyCoin = INFO + ENERGY
IntroExtroCoin = INTRO + EXTRO
FlexFriendsCoin = FLEX + FRIENDS
GeneralisationSpecialisationCoin = GENERALISATION + SPECIALISATION

COINS_DICT = {
    mSeCoin: (FEMININE, MASCULINE),
    mDeCoin: (FEMININE, MASCULINE),
    ObserverDeciderCoin: (OBSERVER, DECIDER),
    DiDeCoin: (DI, DE),
    OiOeCoin: (OI, OE),
    SNCoin: (SENSING, INTUITION),
    TFCoin: (THINKING, FEELING),
    SleepPlayCoin: (SLEEP, PLAY),
    BlastConsumeCoin: (BLAST, CONSUME),
    InfoEnergyCoin: (INFO, ENERGY),
    IntroExtroCoin: (INTRO, EXTRO),
}

# Optional
COINS_SOCIAL = {
    FlexFriendsCoin: (FLEX, FRIENDS),
    GeneralisationSpecialisationCoin: (GENERALISATION, SPECIALISATION)
}

COINS_AUXILIARY = {
    "ObserverAxis": ("Se/Ni", "Ne/Si"),
    "DeciderAxis": ("Te/Fi", "Fe/Ti"),
}

@dataclass
class OpsProfile:
    mSe: str
    mDe: str
    ObserverDecider: str
    DiDe: str
    OiOe: str
    SN: str
    TF: str
    SleepPlay: str
    BlastConsume: str
    InfoEnergy: str
    IntroExtro: str
    FlexFriends: str
    ResponsibilitySpecialisation: str


def decode_op_code(ops) -> OpsProfile:
    match = PATTERN.match(ops)
    if match:
        (
            mSe,
            mDe,
            function1,
            function2,
            animal1,
            animal2,
            animal3,
            animal4,
            social,
        ) = match.groups()

        def get_coin_value(check_function1, check_function2, value1, value2):
            if check_function1:
                return value1
            elif check_function2:
                return value2
            else:
                return None

        coins = {
            mSeCoin: get_coin_value(
                mSe == MASCULINE, mSe == FEMININE, MASCULINE, FEMININE
            ),
            mDeCoin: get_coin_value(
                mDe == MASCULINE, mDe == FEMININE, MASCULINE, FEMININE
            ),
            ObserverDeciderCoin: (
                OBSERVER
                if is_observer(function1)
                else DECIDER if is_decider(function1) else None
            ),
            DiDeCoin: get_coin_value(
                is_di(function1) or is_di(function2),
                is_de(function1) or is_de(function2),
                DI,
                DE,
            ),
            OiOeCoin: get_coin_value(
                is_oi(function1) or is_oi(function2),
                is_oe(function1) or is_oe(function2),
                OI,
                OE,
            ),
            SNCoin: get_coin_value(
                is_sensing(function1) or is_sensing(function2),
                is_intuition(function1) or is_intuition(function2),
                SENSING,
                INTUITION,
            ),
            TFCoin: get_coin_value(
                is_thinking(function1) or is_thinking(function2),
                is_feeling(function1) or is_feeling(function2),
                THINKING,
                FEELING,
            ),
            SleepPlayCoin: get_coin_value(
                is_sleep(animal1) or is_sleep(animal2),
                is_play(animal1) or is_play(animal2),
                SLEEP,
                PLAY,
            ),
            BlastConsumeCoin: get_coin_value(
                is_consume(animal1) or is_consume(animal2),
                is_blast(animal1) or is_blast(animal2),
                CONSUME,
                BLAST,
            ),
            InfoEnergyCoin: get_coin_value(
                is_info(animal4), is_energy(animal4), INFO, ENERGY
            ),
            IntroExtroCoin: get_coin_value(
                is_intro(animal4), is_extro(animal4), INTRO, EXTRO
            ),
            FlexFriendsCoin: get_coin_value(
                is_flex(social), is_friends(social), FLEX, FRIENDS
            ),
            GeneralisationSpecialisationCoin: get_coin_value(
                is_specialisation(social),
                is_responsibility(social),
                SPECIALISATION,
                GENERALISATION,
            ),
        }

        return coins
    else:
        raise ValueError(f"Unable to parse ops string: {ops}")



def is_observer(value):
    return value in ["Si", "Se", "Ni", "Ne", "Oe", "Oi", "Sx", "Nx"]


def is_decider(value):
    return value in ["Ti", "Te", "Fi", "Fe", "De", "Di", "Tx", "Fx"]


def is_di(value):
    return value in ["Ti", "Fi", "Di"]


def is_de(value):
    return value in ["Te", "Fe", "De"]


def is_oi(value):
    return value in ["Si", "Ni", "Oi"]


def is_oe(value):
    return value in ["Se", "Ne", "Oe"]


def is_sensing(value):
    return value in ["Si", "Se", "Sx"]


def is_intuition(value):
    return value in ["Ni", "Ne", "Nx"]


def is_thinking(value):
    return value in ["Ti", "Te", "Tx"]


def is_feeling(value):
    return value in ["Fi", "Fe", "Fx"]


def is_sleep(value):
    return value == "S"


def is_play(value):
    return value == "P"


def is_consume(value):
    return value == "C"


def is_blast(value):
    return value == "B"


def is_info(value):
    return value in ["S", "P"]


def is_energy(value):
    return value in ["C", "B"]


def is_intro(value):
    return value in ["P", "B"]


def is_extro(value):
    return value in ["S", "C"]


def is_flex(value):
    return value in ["1", "3"]


def is_friends(value):
    return value in ["2", "4"]


def is_specialisation(value):
    return value in ["3", "4"]


def is_responsibility(value):
    return value in ["1", "2"]


def validate_op_code(ops):
    match = PATTERN.match(ops)
    return match is not None and len(match.groups()) >= 8


def format_coins(coins):
    return f"""Modalities: {coins[mSeCoin]}{coins[mDeCoin]}
ObserverDecider: {coins[ObserverDeciderCoin]}
DiDe: {coins[DiDeCoin]}
OiOe: {coins[OiOeCoin]}
SN: {coins[SNCoin]}
TF: {coins[TFCoin]}
SleepPlay: {coins[SleepPlayCoin]}
BlastConsume: {coins[BlastConsumeCoin]}
InfoEnergy: {coins[InfoEnergyCoin]}
IntroExtro: {coins[IntroExtroCoin]}
"""

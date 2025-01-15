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

ModalitySensoryCoin = "ModalitySensory"
ModalityDeCoin = "ModalityDe"
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
QuadrantCoin = "Quadrant"
MBTICoin = "MBTI"

COINS_DICT = {
    ModalitySensoryCoin: (FEMININE, MASCULINE),
    ModalityDeCoin: (FEMININE, MASCULINE),
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
    GeneralisationSpecialisationCoin: (GENERALISATION, SPECIALISATION),
}

COINS_AUXILIARY = {
    "ObserverAxis": ("Se/Ni", "Ne/Si"),
    "DeciderAxis": ("Te/Fi", "Fe/Ti"),
}


@dataclass
class OpsProfile:
    ModalitySensory: str
    ModalityDe: str
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
    Quadrant: str
    MBTI: str


def decode_op_code(ops) -> OpsProfile:
    match = PATTERN.match(ops)
    if match:
        (
            modalitySensory,
            modalityDe,
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
            ModalitySensoryCoin: get_coin_value(
                modalitySensory == MASCULINE,
                modalitySensory == FEMININE,
                MASCULINE,
                FEMININE,
            ),
            ModalityDeCoin: get_coin_value(
                modalityDe == MASCULINE, modalityDe == FEMININE, MASCULINE, FEMININE
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
            QuadrantCoin: get_quadrant(function1, function2),
            MBTICoin: get_mbti(function1, function2),
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

def is_se_ni(function1, function2):
    return function1 in ["Se", "Ni"] or function2 in ["Se", "Ni"]

def is_ne_si(function1, function2):
    return function1 in ["Si", "Ne"] or function2 in ["Si", "Ne"]

def is_te_fi(function1, function2):
    return function1 in ["Te", "Fi"] or function2 in ["Te", "Fi"]

def is_fe_ti(function1, function2):
    return function1 in ["Fe", "Ti"] or function2 in ["Fe", "Ti"]

def get_quadrant(function1, function2):
    if is_se_ni(function1, function2) and is_te_fi(function1, function2):
        return "Gamma"
    if is_ne_si(function1, function2) and is_te_fi(function1, function2):
        return "Delta"
    if is_se_ni(function1, function2) and is_fe_ti(function1, function2):
        return "Beta"
    if is_ne_si(function1, function2) and is_fe_ti(function1, function2):
        return "Alpha"
    return None

def get_mbti(function1, function2):
    # observers
    if function1 == "Se" and function2 in ["Ti", "Fe"]:
        return "ESTP"
    if function1 == "Se" and function2 in ["Fi", "Te"]:
        return "ESFP"
    if function1 == "Si" and function2 in ["Te", "Fi"]:
        return "ISTJ"
    if function1 == "Si" and function2 in ["Fe", "Ti"]:
        return "ISFJ"
    if function1 == "Ne" and function2 in ["Ti", "Fe"]:
        return "ENTP"
    if function1 == "Ne" and function2 in ["Fi", "Te"]:
        return "ENFP"
    if function1 == "Ni" and function2 in ["Te", "Fi"]:
        return "INTJ"
    if function1 == "Ni" and function2 in ["Fe", "Ti"]:
        return "INFJ"

    # deciders
    if function1 == "Te" and function2 in ["Si", "Ne"]:
        return "ESTJ"
    if function1 == "Te" and function2 in ["Ni", "Se"]:
        return "ENTJ"
    if function1 == "Fe" and function2 in ["Si", "Ne"]:
        return "ESFJ"
    if function1 == "Fe" and function2 in ["Ni", "Se"]:
        return "ENFJ"
    if function1 == "Ti" and function2 in ["Se", "Ni"]:
        return "ISTP"
    if function1 == "Ti" and function2 in ["Ne", "Si"]:
        return "INTP"
    if function1 == "Fi" and function2 in ["Se", "Ni"]:
        return "ISFP"
    if function1 == "Fi" and function2 in ["Ne", "Si"]:
        return "INFP"
    return None

def format_coins(coins):
    return f"""Modalities: {coins[ModalitySensoryCoin]}{coins[ModalityDeCoin]}
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

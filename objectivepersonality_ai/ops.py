import re
from dataclasses import dataclass
from typing import Optional

# Constants (keys and type values)
ModalitySensoryCoin = "ModalitySensory"
ModalityDeCoin = "ModalityDe"
ObserverDeciderCoin = "ObserverDecider"
DiDeCoin = "DiDe"
OiOeCoin = "OiOe"
NSCoin = "NS"
FTCoin = "FT"
SleepPlayCoin = "SleepPlay"
ConsumeBlastCoin = "ConsumeBlast"
InfoEnergyCoin = "InfoEnergy"
IntroExtroCoin = "IntroExtro"
FlexFriendsCoin = "FlexFriends"
GenSpecCoin = "GenSpec"
QuadrantCoin = "Quadrant"
MBTICoin = "MBTI"

MASCULINE = "M"
FEMININE = "F"
OBSERVER = "Observer"
DECIDER = "Decider"
OI = "Oi"
OE = "Oe"
DI = "Di"
DE = "De"
THINKING = "T"
FEELING = "F"
INTUITION = "N"
SENSING = "S"
INTRO = "Intro"
EXTRO = "Extro"
INFO = "Info"
ENERGY = "Energy"
CONSUME = "Consume"
BLAST = "Blast"
SLEEP = "Sleep"
PLAY = "Play"
FLEX = "Flex"
FRIENDS = "Friends"
GENERALISATION = "Generalisation"
SPECIALISATION = "Specialisation"

PATTERN = re.compile(
    r"([FMx])([FMx])-([SNFTx][iex])\/([SNFTx][iex])-([SPBCx])([SPBCx])\/([SPBCx])\(([SPBCx])\)(?: \[(\d)\])?"
)


@dataclass
class OpProfile:
    ModalitySensoryCoin: Optional[str]
    ModalityDeCoin: Optional[str]
    ObserverDecider: Optional[str]
    DiDe: Optional[str]
    OiOe: Optional[str]
    NS: Optional[str]
    FT: Optional[str]
    SleepPlay: Optional[str]
    ConsumeBlast: Optional[str]
    InfoEnergy: Optional[str]
    IntroExtro: Optional[str]
    FlexFriends: Optional[str]
    GenSpec: Optional[str]
    Quadrant: Optional[str]
    MBTI: Optional[str]

    def is_observer(self) -> bool:
        return self.ObserverDecider == OBSERVER

    def is_decider(self) -> bool:
        return self.ObserverDecider == DECIDER

    def is_di(self) -> bool:
        return self.DiDe == DI

    def is_de(self) -> bool:
        return self.DiDe == DE

    def is_oi(self) -> bool:
        return self.OiOe == OI

    def is_oe(self) -> bool:
        return self.OiOe == OE

    def is_sensing(self) -> bool:
        return self.NS == SENSING

    def is_intuition(self) -> bool:
        return self.NS == INTUITION

    def is_thinking(self) -> bool:
        return self.FT == THINKING

    def is_feeling(self) -> bool:
        return self.FT == FEELING

    def is_sleep(self) -> bool:
        return self.SleepPlay == SLEEP

    def is_play(self) -> bool:
        return self.SleepPlay == PLAY

    def is_consume(self) -> bool:
        return self.ConsumeBlast == CONSUME

    def is_blast(self) -> bool:
        return self.ConsumeBlast == BLAST

    def is_info(self) -> bool:
        return self.InfoEnergy == INFO

    def is_energy(self) -> bool:
        return self.InfoEnergy == ENERGY

    def is_intro(self) -> bool:
        return self.IntroExtro == INTRO

    def is_extro(self) -> bool:
        return self.IntroExtro == EXTRO

    def is_flex(self) -> bool:
        return self.FlexFriends == FLEX

    def is_friends(self) -> bool:
        return self.FlexFriends == FRIENDS

    def is_spec(self) -> bool:
        return self.GenSpec == SPECIALISATION

    def is_gen(self) -> bool:
        return self.GenSpec == GENERALISATION


# Utility functions
def is_observer(value: str) -> bool:
    return value in ["Si", "Se", "Ni", "Ne", "Oe", "Oi", "Sx", "Nx"]


def is_decider(value: str) -> bool:
    return value in ["Ti", "Te", "Fi", "Fe", "De", "Di", "Tx", "Fx"]


def is_di(value: str) -> bool:
    return value in ["Ti", "Fi", "Di"]


def is_de(value: str) -> bool:
    return value in ["Te", "Fe", "De"]


def is_oi(value: str) -> bool:
    return value in ["Si", "Ni", "Oi"]


def is_oe(value: str) -> bool:
    return value in ["Se", "Ne", "Oe"]


def is_sensing(value: str) -> bool:
    return value in ["Si", "Se", "Sx"]


def is_intuition(value: str) -> bool:
    return value in ["Ni", "Ne", "Nx"]


def is_thinking(value: str) -> bool:
    return value in ["Ti", "Te", "Tx"]


def is_feeling(value: str) -> bool:
    return value in ["Fi", "Fe", "Fx"]


def is_sleep(value: str) -> bool:
    return value == "S"


def is_play(value: str) -> bool:
    return value == "P"


def is_consume(value: str) -> bool:
    return value == "C"


def is_blast(value: str) -> bool:
    return value == "B"


def is_info(value: str) -> bool:
    return value in ["S", "P"]


def is_energy(value: str) -> bool:
    return value in ["C", "B"]


def is_intro(value: str) -> bool:
    return value in ["P", "B"]


def is_extro(value: str) -> bool:
    return value in ["S", "C"]


def is_flex(value: str) -> bool:
    return value in ["1", "3"]


def is_friends(value: str) -> bool:
    return value in ["2", "4"]


def is_spec(value: str) -> bool:
    return value in ["3", "4"]


def is_gen(value: str) -> bool:
    return value in ["1", "2"]


def is_se_ni(func1: str, func2: str) -> bool:
    return func1 in ["Se", "Ni"] or func2 in ["Se", "Ni"]


def is_ne_si(func1: str, func2: str) -> bool:
    return func1 in ["Si", "Ne"] or func2 in ["Si", "Ne"]


def is_te_fi(func1: str, func2: str) -> bool:
    return func1 in ["Te", "Fi"] or func2 in ["Te", "Fi"]


def is_fe_ti(func1: str, func2: str) -> bool:
    return func1 in ["Fe", "Ti"] or func2 in ["Fe", "Ti"]


def get_quadrant(func1: str, func2: str) -> Optional[str]:
    if is_se_ni(func1, func2) and is_te_fi(func1, func2):
        return "Gamma"
    if is_ne_si(func1, func2) and is_te_fi(func1, func2):
        return "Delta"
    if is_se_ni(func1, func2) and is_fe_ti(func1, func2):
        return "Beta"
    if is_ne_si(func1, func2) and is_fe_ti(func1, func2):
        return "Alpha"
    return None


def get_mbti(func1: str, func2: str) -> Optional[str]:
    if func1 == "Se" and func2 in ["Ti", "Fe"]:
        return "ESTP"
    if func1 == "Se" and func2 in ["Fi", "Te"]:
        return "ESFP"
    if func1 == "Si" and func2 in ["Te", "Fi"]:
        return "ISTJ"
    if func1 == "Si" and func2 in ["Fe", "Ti"]:
        return "ISFJ"
    if func1 == "Ne" and func2 in ["Ti", "Fe"]:
        return "ENTP"
    if func1 == "Ne" and func2 in ["Fi", "Te"]:
        return "ENFP"
    if func1 == "Ni" and func2 in ["Te", "Fi"]:
        return "INTJ"
    if func1 == "Ni" and func2 in ["Fe", "Ti"]:
        return "INFJ"
    if func1 == "Te" and func2 in ["Si", "Ne"]:
        return "ESTJ"
    if func1 == "Te" and func2 in ["Ni", "Se"]:
        return "ENTJ"
    if func1 == "Fe" and func2 in ["Si", "Ne"]:
        return "ESFJ"
    if func1 == "Fe" and func2 in ["Ni", "Se"]:
        return "ENFJ"
    if func1 == "Ti" and func2 in ["Se", "Ni"]:
        return "ISTP"
    if func1 == "Ti" and func2 in ["Ne", "Si"]:
        return "INTP"
    if func1 == "Fi" and func2 in ["Se", "Ni"]:
        return "ISFP"
    if func1 == "Fi" and func2 in ["Ne", "Si"]:
        return "INFP"
    return None


def decode_op_code(ops: str) -> OpProfile:
    """
    Decode an op-code string and return an OpProfile dataclass.
    """
    match = PATTERN.search(ops)
    if match:
        modalitySensory, modalityDe, func1, func2, animal1, animal2, animal3, animal4, social = (
            match.groups()[:9]
        )

        def get_coin_value(
            check1: bool, check2: bool, value1: str, value2: str
        ) -> Optional[str]:
            return value1 if check1 else value2 if check2 else None

        op_profile = OpProfile(
            ModalitySensoryCoin=get_coin_value(
                modalitySensory == MASCULINE, modalitySensory == FEMININE, MASCULINE, FEMININE
            )
            or None,
            ModalityDeCoin=get_coin_value(
                modalityDe == MASCULINE, modalityDe == FEMININE, MASCULINE, FEMININE
            )
            or None,
            ObserverDecider=(
                OBSERVER
                if is_observer(func1)
                else DECIDER if is_decider(func1) else None
            ),
            DiDe=get_coin_value(
                is_di(func1) or is_di(func2), is_de(func1) or is_de(func2), DI, DE
            )
            or None,
            OiOe=get_coin_value(
                is_oi(func1) or is_oi(func2), is_oe(func1) or is_oe(func2), OI, OE
            )
            or None,
            NS=get_coin_value(
                is_sensing(func1) or is_sensing(func2),
                is_intuition(func1) or is_intuition(func2),
                SENSING,
                INTUITION,
            )
            or None,
            FT=get_coin_value(
                is_thinking(func1) or is_thinking(func2),
                is_feeling(func1) or is_feeling(func2),
                THINKING,
                FEELING,
            )
            or None,
            SleepPlay=get_coin_value(
                is_sleep(animal1) or is_sleep(animal2),
                is_play(animal1) or is_play(animal2),
                SLEEP,
                PLAY,
            )
            or None,
            ConsumeBlast=get_coin_value(
                is_consume(animal1) or is_consume(animal2),
                is_blast(animal1) or is_blast(animal2),
                CONSUME,
                BLAST,
            )
            or None,
            InfoEnergy=get_coin_value(
                is_info(animal4), is_energy(animal4), INFO, ENERGY
            )
            or None,
            IntroExtro=get_coin_value(
                is_intro(animal4), is_extro(animal4), INTRO, EXTRO
            )
            or None,
            FlexFriends=get_coin_value(
                is_flex(social), is_friends(social), FLEX, FRIENDS
            )
            or None,
            GenSpec=get_coin_value(
                is_spec(social), is_gen(social), SPECIALISATION, GENERALISATION
            )
            or None,
            Quadrant=get_quadrant(func1, func2) or None,
            MBTI=get_mbti(func1, func2) or None,
        )
        return op_profile
    else:
        raise ValueError(f"Unable to parse ops string: {ops}")


COINS_DICT = {
    ModalitySensoryCoin: (FEMININE, MASCULINE),
    ModalityDeCoin: (FEMININE, MASCULINE),
    ObserverDeciderCoin: (OBSERVER, DECIDER),
    DiDeCoin: (DI, DE),
    OiOeCoin: (OI, OE),
    NSCoin: (INTUITION, SENSING),
    FTCoin: (FEELING, THINKING),
    SleepPlayCoin: (SLEEP, PLAY),
    ConsumeBlastCoin: (CONSUME, BLAST),
    InfoEnergyCoin: (INFO, ENERGY),
    IntroExtroCoin: (INTRO, EXTRO),
}

# Optional
COINS_SOCIAL = {
    FlexFriendsCoin: (FLEX, FRIENDS),
    GenSpecCoin: (GENERALISATION, SPECIALISATION),
}

COINS_AUXILIARY = {
    "ObserverAxis": ("Se/Ni", "Ne/Si"),
    "DeciderAxis": ("Te/Fi", "Fe/Ti"),
}


def format_coins(coins):
    return f"""Modalities: {coins[ModalitySensoryCoin]}{coins[ModalityDeCoin]}
ObserverDecider: {coins[ObserverDeciderCoin]}
DiDe: {coins[DiDeCoin]}
OiOe: {coins[OiOeCoin]}
SN: {coins[NSCoin]}
TF: {coins[FTCoin]}
SleepPlay: {coins[SleepPlayCoin]}
BlastConsume: {coins[ConsumeBlastCoin]}
InfoEnergy: {coins[InfoEnergyCoin]}
IntroExtro: {coins[IntroExtroCoin]}
"""

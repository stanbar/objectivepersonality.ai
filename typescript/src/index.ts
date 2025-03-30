export const mSCoin = "mS" as const;
export const mDeCoin = "mDe" as const;
export const ObserverDeciderCoin = "ObserverDecider" as const;
export const DiDeCoin = "DiDe" as const;
export const OiOeCoin = "OiOe" as const;
export const NSCoin = "NS" as const;
export const FTCoin = "FT" as const;
export const SleepPlayCoin = "SleepPlay" as const;
export const ConsumeBlastCoin = "ConsumeBlast" as const;
export const InfoEnergyCoin = "InfoEnergy" as const;
export const IntroExtroCoin = "IntroExtro" as const;
export const FlexFriendsCoin = "FlexFriends" as const;
export const GenSpecCoin = "GenSpec" as const;
export const QuadrantCoin = "Quadrant" as const;
export const MBTICoin = "MBTI" as const;


type MASCULINE = "M"
type FEMININE = "F"
type OBSERVER = "Observer"
type DECIDER = "Decider"
type Oi = "Oi"
type Oe = "Oe"
type De = "De"
type Di = "Di"
type THINKING = "T"
type FEELING = "F"
type INTUITION = "N"
type SENSING = "S"
type INTRO = "Intro"
type EXTRO = "Extro"
type ENERGY = "Energy"
type INFO = "Info"
type CONSUME = "Consume"
type BLAST = "Blast"
type SLEEP = "Sleep"
type PLAY = "Play"
type FLEX = "Flex"
type FRIENDS = "Friends"
type GEN = "Generalisation"
type SPEC = "Specialisation"


export type OpProfile = {
  [mSCoin]: FEMININE | MASCULINE | null;
  [mDeCoin]: FEMININE | MASCULINE | null;
  [ObserverDeciderCoin]: OBSERVER | DECIDER | null;
  [DiDeCoin]: Di | De | null;
  [OiOeCoin]: Oi | Oe | null;
  [NSCoin]: INTUITION | SENSING | null;
  [FTCoin]: FEELING | THINKING | null;
  [SleepPlayCoin]: SLEEP | PLAY | null;
  [ConsumeBlastCoin]: CONSUME | BLAST | null;
  [InfoEnergyCoin]: INFO | ENERGY | null;
  [IntroExtroCoin]: INTRO | EXTRO | null;
  [FlexFriendsCoin]: FLEX | FRIENDS | null;
  [GenSpecCoin]: SPEC | GEN | null;
  [QuadrantCoin]: "Gamma" | "Delta" | "Beta" | "Alpha" | null;
  [MBTICoin]:
  | "ESTP"
  | "ESFP"
  | "ISTJ"
  | "ISFJ"
  | "ENTP"
  | "ENFP"
  | "INTJ"
  | "INFJ"
  | "ESTJ"
  | "ENTJ"
  | "ESFJ"
  | "ENFJ"
  | "ISTP"
  | "INTP"
  | "ISFP"
  | "INFP"
  | null;
};

export type OpProof = {
  [K in keyof OpProfile as `${K & string}Proof`]: string | null;
};

export type OpResult = OpProfile &
  OpProof;



// FF-Ti/Si-SB/P(C) [1]
const PATTERN_SUBIJECTIVE = /^(?:([FMx])([FMx])-)?([SNFTx][iex])\/([SNFTx][iex])-([SPBCx])([SPBCx])\/([SPBCx])\(([SPBCx])\)(?: \[(\d)\])?$/;
// FF-Ti/Si-SB/P(C) #1
const PATTERN_DS = /^(?:([FMx])([FMx])-)?([SNFTx][iex])\/([SNFTx][iex])-([SPBCx])([SPBCx])\/([SPBCx])\(([SPBCx])\)(?: \[(\d)\])?$/;
// FF-TiSi-SBPC-1
const PATTERN_SIMPLE = /^(?:([FMx])([FMx])-)?([SNFTx][iex])([SNFTx][iex])-([SPBCx])([SPBCx])([SPBCx])([SPBCx])(?:-(\d))?$/;

export function validateOpCode(ops: string) {
  const match = PATTERN_SUBIJECTIVE.exec(ops);
  return match && match.length >= 8
}

const isObserver = (value: string) => ["Si", "Se", "Ni", "Ne", "Oe", "Oi", "Sx", "Nx"].includes(value);
const isDecider = (value: string) => ["Ti", "Te", "Fi", "Fe", "De", "Di", "Tx", "Fx"].includes(value);
const isDi = (value: string) => ["Ti", "Fi", "Di"].includes(value);
const isDe = (value: string) => ["Te", "Fe", "De"].includes(value);
const isOi = (value: string) => ["Si", "Ni", "Oi"].includes(value);
const isOe = (value: string) => ["Se", "Ne", "Oe"].includes(value);
const isSensing = (value: string) => ["Si", "Se", "Sx"].includes(value);
const isIntuition = (value: string) => ["Ni", "Ne", "Nx"].includes(value);
const isThinking = (value: string) => ["Ti", "Te", "Tx"].includes(value);
const isFeeling = (value: string) => ["Fi", "Fe", "Fx"].includes(value);
const isSleep = (value: string) => value === "S";
const isPlay = (value: string) => value === "P";
const isConsume = (value: string) => value === "C";
const isBlast = (value: string) => value === "B";
const isInfo = (value: string) => ["S", "P"].includes(value);
const isEnergy = (value: string) => ["C", "B"].includes(value);
const isIntro = (value: string) => ["P", "B"].includes(value);
const isExtro = (value: string) => ["S", "C"].includes(value);
const isFlex = (value: string) => ["1", "3"].includes(value);
const isFriends = (value: string) => ["2", "4"].includes(value);
const isSpec = (value: string) => ["3", "4"].includes(value);
const isGen = (value: string) => ["1", "2"].includes(value);
const isSeNi = (function1: string, function2: string) => ["Se", "Ni"].includes(function1) || ["Se", "Ni"].includes(function2);
const isNeSi = (function1: string, function2: string) => ["Si", "Ne"].includes(function1) || ["Si", "Ne"].includes(function2);
const isTeFi = (function1: string, function2: string) => ["Te", "Fi"].includes(function1) || ["Te", "Fi"].includes(function2);
const isFeTi = (function1: string, function2: string) => ["Fe", "Ti"].includes(function1) || ["Fe", "Ti"].includes(function2);

/*
* Quadrants
* Alpha: NeSi and FeTi
* Beta: SeNi, FeTi
* Delta: NeSi, TeFi
* Gamma: SeNi, TeFi
*/

const getQuadrant = (function1: string, function2: string) => {
  if (isSeNi(function1, function2) && isTeFi(function1, function2)) return "Gamma";
  if (isNeSi(function1, function2) && isTeFi(function1, function2)) return "Delta";
  if (isSeNi(function1, function2) && isFeTi(function1, function2)) return "Beta";
  if (isNeSi(function1, function2) && isFeTi(function1, function2)) return "Alpha";
  return undefined;
}

const getMBTI = (function1: string, function2: string) => {
  // observers
  if (function1 === "Se" && (function2 === "Ti" || function2 === "Fe")) return "ESTP";
  if (function1 === "Se" && (function2 === "Fi" || function2 === "Te")) return "ESFP";
  if (function1 === "Si" && (function2 === "Te" || function2 === "Fi")) return "ISTJ";
  if (function1 === "Si" && (function2 === "Fe" || function2 === "Ti")) return "ISFJ";
  if (function1 === "Ne" && (function2 === "Ti" || function2 === "Fe")) return "ENTP";
  if (function1 === "Ne" && (function2 === "Fi" || function2 === "Te")) return "ENFP";
  if (function1 === "Ni" && (function2 === "Te" || function2 === "Fi")) return "INTJ";
  if (function1 === "Ni" && (function2 === "Fe" || function2 === "Ti")) return "INFJ";

  //deciders
  if (function1 === "Te" && (function2 === "Si" || function2 === "Ne")) return "ESTJ";
  if (function1 === "Te" && (function2 === "Ni" || function2 === "Se")) return "ENTJ";
  if (function1 === "Fe" && (function2 === "Si" || function2 === "Ne")) return "ESFJ";
  if (function1 === "Fe" && (function2 === "Ni" || function2 === "Se")) return "ENFJ";
  if (function1 === "Ti" && (function2 === "Se" || function2 === "Ni")) return "ISTP";
  if (function1 === "Ti" && (function2 === "Ne" || function2 === "Si")) return "INTP";
  if (function1 === "Fi" && (function2 === "Se" || function2 === "Ni")) return "ISFP";
  if (function1 === "Fi" && (function2 === "Ne" || function2 === "Si")) return "INFP";
  return undefined;
}


const MASCULINE = "M"
const FEMININE = "F"
const OBSERVER = "Observer"
const DECIDER = "Decider"
const Oi = "Oi"
const Oe = "Oe"
const De = "De"
const Di = "Di"
const THINKING = "T"
const FEELING = "F"
const INTUITION = "N"
const SENSING = "S"
const INTRO = "Intro"
const EXTRO = "Extro"
const ENERGY = "Energy"
const INFO = "Info"
const CONSUME = "Consume"
const BLAST = "Blast"
const SLEEP = "Sleep"
const PLAY = "Play"
const FLEX = "Flex"
const FRIENDS = "Friends"
const GENERALISATION = "Generalisation"
const SPECIALISATION = "Specialisation"
const MBTI = "MBTI"

function parseOpsCode(ops: string): string[] {
  let match = PATTERN_SIMPLE.exec(ops);
  if (!match)
    match = PATTERN_SUBIJECTIVE.exec(ops);
  if (!match)
    match = PATTERN_DS.exec(ops);
  if (!match)
    throw new Error(`Unable to parse ops code: ${ops}, please use a following format FF-TiSi-SBPC-1`);

  return match.slice(1, 10);
}

// Helper function to reduce repetition
const getCoinValue = <T extends string>(checkFunction1: boolean, checkFunction2: boolean, value1: T, value2: T): T | undefined => {
  return checkFunction1 ? value1 : checkFunction2 ? value2 : undefined;
}

export function decodeOpCode(ops: string): OpProfile {
  const [mS, mDe, function1, function2, animal1, animal2, animal3, animal4, social] = parseOpsCode(ops);

  const opProfile: OpProfile = {
    [mSCoin]: getCoinValue(mS === MASCULINE, mS === FEMININE, MASCULINE, FEMININE) ?? null,
    [mDeCoin]: getCoinValue(mDe === MASCULINE, mDe === FEMININE, MASCULINE, FEMININE) ?? null,
    [ObserverDeciderCoin]: isObserver(function1) ? OBSERVER : isDecider(function1) ? DECIDER : null,
    [DiDeCoin]: getCoinValue(isDi(function1) || isDi(function2), isDe(function1) || isDe(function2), Di, De) ?? null,
    [OiOeCoin]: getCoinValue(isOi(function1) || isOi(function2), isOe(function1) || isOe(function2), Oi, Oe) ?? null,
    [NSCoin]: getCoinValue(isSensing(function1) || isSensing(function2), isIntuition(function1) || isIntuition(function2), SENSING, INTUITION) ?? null,
    [FTCoin]: getCoinValue(isThinking(function1) || isThinking(function2), isFeeling(function1) || isFeeling(function2), THINKING, FEELING) ?? null,
    [SleepPlayCoin]: getCoinValue(isSleep(animal1) || isSleep(animal2), isPlay(animal1) || isPlay(animal2), SLEEP, PLAY) ?? null,
    [ConsumeBlastCoin]: getCoinValue(isConsume(animal1) || isConsume(animal2), isBlast(animal1) || isBlast(animal2), CONSUME, BLAST) ?? null,
    [InfoEnergyCoin]: getCoinValue(isInfo(animal4), isEnergy(animal4), INFO, ENERGY) ?? null,
    [IntroExtroCoin]: getCoinValue(isIntro(animal4), isExtro(animal4), INTRO, EXTRO) ?? null,
    [FlexFriendsCoin]: getCoinValue(isFlex(social), isFriends(social), FLEX, FRIENDS) ?? null,
    [GenSpecCoin]: getCoinValue(isSpec(social), isGen(social), SPECIALISATION, GENERALISATION) ?? null,
    [QuadrantCoin]: getQuadrant(function1, function2) ?? null,
    [MBTICoin]: getMBTI(function1, function2) ?? null,
  };
  return opProfile;
}

export function breakdownOpCode(ops: string): string {
  const [mS, mDe, function1, function2, animal1, animal2, animal3, animal4, social] = parseOpsCode(ops);

  const observerDecider = isObserver(function1) ? "Observer" : isDecider(function1) ? "Decider" : null;
  const diDe = getCoinValue(isDi(function1) || isDi(function2), isDe(function1) || isDe(function2), "Di", "De") ?? null;
  const oiOe = getCoinValue(isOi(function1) || isOi(function2), isOe(function1) || isOe(function2), "Oi", "Oe") ?? null;
  const ns = getCoinValue(isSensing(function1) || isSensing(function2), isIntuition(function1) || isIntuition(function2), "Sensory", "Intuitive") ?? null;
  const ft = getCoinValue(isThinking(function1) || isThinking(function2), isFeeling(function1) || isFeeling(function2), 'Thinker', "Feeler") ?? null;
  const sleepPlay = getCoinValue(isSleep(animal1) || isSleep(animal2), isPlay(animal1) || isPlay(animal2), "Sleep", "Play") ?? null;
  const consumeBlast = getCoinValue(isConsume(animal1) || isConsume(animal2), isBlast(animal1) || isBlast(animal2), "Consume", "Blast") ?? null;
  const infoEnergy = getCoinValue(isInfo(animal4), isEnergy(animal4), INFO, ENERGY) ?? null;
  const introExtro = getCoinValue(isIntro(animal4), isExtro(animal4), "Introvert", "Extrovert") ?? null;
  const flexFriends = getCoinValue(isFlex(social), isFriends(social), "Flex (Self-motivated)", "Friends (Tribe-motivated)") ?? null;
  const genSpec = getCoinValue(isSpec(social), isGen(social), "Specialisation", "Generalisation") ?? null;

  let lastAnimal = "";
  if (infoEnergy === INFO && introExtro === "Introvert") {
    lastAnimal = "Play last"
  } else if (infoEnergy === INFO && introExtro === "Extrovert") {
    lastAnimal = "Sleep last"
  } else if (infoEnergy === ENERGY && introExtro === "Introvert") {
    lastAnimal = "Blast last"
  } else if (infoEnergy === ENERGY && introExtro === "Extrovert") {
    lastAnimal = "Consume last"
  }

  let breakdown = `${observerDecider}, ${observerDecider == OBSERVER ? oiOe : diDe}, ${observerDecider == OBSERVER ? diDe : oiOe}, ${lastAnimal}, ${ft}, ${ns}, ${function1}, ${function2}, ${sleepPlay}, ${consumeBlast}, ${introExtro}`
  if (flexFriends) {
    breakdown = `${breakdown}, ${flexFriends}`;
  }
  if (genSpec) {
    breakdown = `${breakdown}, ${genSpec}`;
  }
  return breakdown
}

export function validateProperties(properties: { [key: string]: any }) {
  try {
    const mSe = properties[mSCoin];
    if (mSe !== "M" && mSe !== "F" && mSe !== undefined) throw new Error(`mSe is not valid, ${mSe}`);
    const mDe = properties[mDeCoin];
    if (mDe !== "M" && mDe !== "F" && mDe !== undefined) throw new Error(`mDe is not valid, ${mDe}`);
    const ObserverDecider = properties[ObserverDeciderCoin];
    if (ObserverDecider !== OBSERVER && ObserverDecider !== DECIDER && ObserverDecider !== undefined) throw new Error(`ObserverDecider is not valid, ${ObserverDecider}`);
    const DiDe = properties[DiDeCoin];
    if (DiDe !== Di && DiDe !== De && DiDe !== undefined) throw new Error(`DiDe is not valid, ${DiDe}`);
    const OiOe = properties[OiOeCoin];
    if (OiOe !== Oi && OiOe !== Oe && OiOe !== undefined) throw new Error(`OiOe is not valid, ${OiOe}`);
    const SN = properties[NSCoin];
    if (SN !== SENSING && SN !== INTUITION && SN !== undefined) throw new Error(`NS is not valid, ${SN}`);
    const TF = properties[FTCoin];
    if (TF !== THINKING && TF !== FEELING && TF !== undefined) throw new Error(`FT is not valid, ${TF}`);
    const SleepPlay = properties[SleepPlayCoin];
    if (SleepPlay !== SLEEP && SleepPlay !== PLAY && SleepPlay !== undefined) throw new Error(`SleepPlay is not valid, ${SleepPlay}`);
    const BlastConsume = properties[ConsumeBlastCoin];
    if (BlastConsume !== BLAST && BlastConsume !== CONSUME && BlastConsume !== undefined) throw new Error(`ConsumeBlast is not valid, ${BlastConsume}`);
    const InfoEnergy = properties[InfoEnergyCoin];
    if (InfoEnergy !== INFO && InfoEnergy !== ENERGY && InfoEnergy !== undefined) throw new Error(`InfoEnergy is not valid, ${InfoEnergy}`);
    const IntroExtro = properties[IntroExtroCoin];
    if (IntroExtro !== INTRO && IntroExtro !== EXTRO && IntroExtro !== undefined) throw new Error(`IntroExtro is not valid, ${IntroExtro}`);
    const FlexFriends = properties[FlexFriendsCoin];
    if (FlexFriends !== FLEX && FlexFriends !== FRIENDS && FlexFriends !== undefined) throw new Error(`FlexFriends is not valid, ${FlexFriends}`);
    const GeneralisationSpecialisation = properties[GenSpecCoin];
    if (GeneralisationSpecialisation !== SPECIALISATION && GeneralisationSpecialisation !== GENERALISATION && GeneralisationSpecialisation !== undefined) throw new Error(`GeneralisationSpecialisation is not valid, ${GeneralisationSpecialisation}`);
  } catch (error) {
    return false;
  }
  return true;
}

export function calculateOpCode(profile: OpProfile) {
  const mS = profile[mSCoin];
  const mDe = profile[mDeCoin];
  const ObserverDecider = profile[ObserverDeciderCoin];
  const DiDe = profile[DiDeCoin];
  const OiOe = profile[OiOeCoin];
  const SN = profile[NSCoin];
  const TF = profile[FTCoin];
  const SleepPlay = profile[SleepPlayCoin];
  const BlastConsume = profile[ConsumeBlastCoin];
  const InfoEnergy = profile[InfoEnergyCoin];
  const IntroExtro = profile[IntroExtroCoin];
  const FlexFriends = profile[FlexFriendsCoin];
  const GeneralisationSpecialisation = profile[GenSpecCoin];

  // Calculate observer and decider functions
  const observerFunction: "Si" | "Se" | "Ni" | "Ne" | "Ox" = SN === SENSING ? (OiOe === "Oi" ? "Si" : "Se")
    : SN === INTUITION ? (OiOe === "Oi" ? "Ni" : "Ne")
      : "Ox";
  const deciderFunction: "Ti" | "Te" | "Fi" | "Fe" | "Dx" = TF === THINKING ? (DiDe === "Di" ? "Ti" : "Te")
    : TF === FEELING ? (DiDe === "Di" ? "Fi" : "Fe")
      : "Dx";

  // Must be set
  if (ObserverDecider !== OBSERVER && ObserverDecider !== DECIDER) throw new Error(`ObserverDecider is not valid, ${ObserverDecider}`);
  const [function1, function2] = ObserverDecider === DECIDER ? [deciderFunction, observerFunction] : [observerFunction, deciderFunction];

  // Calculate animals
  const firstAnimal = OiOe === Oi ? (DiDe === Di ? SLEEP : BLAST) : (DiDe === Di ? CONSUME : PLAY)
  const secondAnimal = firstAnimal === SleepPlay ? BlastConsume : SleepPlay;

  const lastAnimal = InfoEnergy === INFO ? (IntroExtro === INTRO ? PLAY : SLEEP) : (IntroExtro === INTRO ? BLAST : CONSUME);

  // Calculate the missing animal
  const allAnimals = [SLEEP, BLAST, PLAY, CONSUME];
  const existingAnimals = [firstAnimal, secondAnimal, lastAnimal];
  const missingAnimal = allAnimals.find(animal => !existingAnimals.includes(animal))!;


  const socialType = FlexFriends === FLEX ? (
    GeneralisationSpecialisation === GENERALISATION ? "1"
      : (GeneralisationSpecialisation === SPECIALISATION ? "3"
        : undefined))
    : (FlexFriends === FRIENDS ? (
      GeneralisationSpecialisation === GENERALISATION ? "2"
        : GeneralisationSpecialisation === SPECIALISATION ? "4"
          : undefined)
      : undefined);

  // Construct the op-code
  const functions = `${function1}${function2}`;
  const animals = `${firstAnimal[0]}${(secondAnimal ?? "X")[0]}${missingAnimal[0]}${lastAnimal[0]}`;
  const opCode = `${mS ?? "x"}${mDe ?? "x"}-${functions}${animals}${socialType ? `-${socialType}` : ""}`;

  return opCode;
}

export function normalizeName(name: string): string {
  // Step 1: Normalize and remove diacritics
  let result = name.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  // Step 2: Replace whitespace with _
  result = result.replace(/\s/g, '_');
  // Step 3: Remove quotes, parentheses, and hyphens
  result = result.replace(/['"()\-]/g, '');
  // Step 4: Replace &, . and both / and \ with _
  result = result.replace(/&/g, '_')
    .replace(/\./g, '_')
    .replace(/[\\/]/g, '_');
  // Step 5: Consolidate multiple _ into a single _ and trim leading/trailing _
  result = result.replace(/_+/g, '_').replace(/^_+|_+$/g, '');
  return result;
}
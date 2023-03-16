class Tone:
    name=""
    index=-1
    freqs=[]
    
    def __init__(self, name, index, freqs):
        self.name = name
        self.index = index
        self.freqs = freqs


toneNames = {
    16.35 : "C",
    17.32 : "C#",
    18.35 : "D",
    19.45 : "D#",
    20.60 : "E",
    21.83 : "F",
    23.12 : "F#",
    24.50 : "G",
    25.96 : "G#",
    27.50 : "A",
    29.14 : "A#",
    30.87 : "B",

    32.70 : "C",
    34.65 : "C#",
    36.71 : "D",
    38.89 : "D#",
    41.20 : "E",
    43.65 : "F",
    46.25 : "F#",
    49.00 : "G",
    51.91 : "G#",
    55.00 : "A",
    58.27 : "A#",
    61.74 : "B",

    65.41 : "C",
    69.30 : "C#",
    73.42 : "D",
    77.78 : "D#",
    82.41 : "E",
    87.31 : "F",
    92.50 : "F#",
    98.00 : "G",
    103.83 : "G#",
    110.00 : "A",
    116.54 : "A#",
    123.47 : "B",

    130.81 : "C",
    138.59 : "C#",
    146.83 : "D",
    155.56 : "D#",
    164.81 : "E",
    174.61 : "F",
    185.00 : "F#",
    196.00 : "G",
    207.65 : "G#",
    220.00 : "A",
    233.08 : "A#",
    246.94 : "B",

    261.63 : "C",
    277.18 : "C#",
    293.66 : "D",
    311.13 : "D#",
    329.63 : "E",
    349.23 : "F",
    369.99 : "F#",
    392.00 : "G",
    415.30 : "G#",
    440.00 : "A",
    466.16 : "A#",
    493.88 : "B",

    523.25 : "C",
    554.37 : "C#",
    587.33 : "D",
    622.25 : "D#",
    659.25 : "E",
    698.46 : "F",
    739.99 : "F#",
    783.99 : "G",
    830.61 : "G#",
    880.00 : "A",
    932.33 : "A#",
    987.77 : "B",

    1046.50 : "C",
    1108.73 : "C#",
    1174.66 : "D",
    1244.51 : "D#",
    1318.51 : "E",
    1396.91 : "F",
    1479.98 : "F#",
    1567.98 : "G",
    1661.22 : "G#",
    1760.00 : "A",
    1864.66 : "A#",
    1975.53 : "B",

    2093.00 : "C",
    2217.46 : "C#",
    2349.32 : "D",
    2489.02 : "D#",
    2637.02 : "E",
    2793.83 : "F",
    2959.96 : "F#",
    3135.96 : "G",
    3322.44 : "G#",
    3520.00 : "A",
    3729.31 : "A#",
    3951.07 : "B",
    
    4186.01 : "C",
    4439.92 : "C#",
    4698.63 : "D",
    4978.03 : "D#",
    5274.04 : "E",
    5587.65 : "F",
    5919.91 : "F#",
    6271.93 : "G",
    6644.88 : "G#",
    7040.00 : "A",
    7458.62 : "A#",
    7902.13 : "B",
}

universalTones = {
    
    "C" : Tone("C", 0, [16.35,
                        32.70,
                        65.41,
                        130.81,
                        261.63,
                        523.25,
                        1046.50,
                        2093.00,
                        4186.01]),
    "C#" : Tone("C#", 1,[ 17.32,
                         34.65,
                         69.30,
                         138.59,
                         277.18,
                         554.37,
                         1108.73,
                         2217.46,
                         4439.92]),
    "D" : Tone("D", 2, [18.35,
                        36.71,
                        73.42,
                        146.83,
                        293.66,
                        587.33,
                        1174.66,
                        2349.32,
                        4698.63]),
    "D#" : Tone("D#", 3, [19.45,
                          38.89,
                          77.78,
                          155.56,
                          311.13,
                          622.25,
                          1244.51,
                          2489.02,
                          4978.03]),
    "E" : Tone("E", 4, [20.60,
                        41.20,
                        82.41,
                        164.81,
                        329.63,
                        659.25,
                        1318.51,
                        2637.02,
                        5274.04]),
    "F" : Tone("F", 5, [21.83,
                        43.65,
                        87.31,
                        174.61,
                        349.23,
                        698.46,
                        1396.91,
                        2793.83,
                        5587.65]),
    "F#" :  Tone("F#", 6, [23.12,
                           46.25,
                           92.50,
                           185.00,
                           369.99,
                           739.99,
                           1479.98,
                           2959.96,
                           5919.91]),
    "G" : Tone("G", 7, [24.50,
                        49.00,
                        98.00,
                        196.00,
                        392.00,
                        783.99,
                        1567.98,
                        3135.96,
                        6271.93]),
    "G#" : Tone("G#", 8, [25.96,
                          51.91,
                          103.83,
                          207.65,
                          415.30,
                          830.61,
                          1661.22,
                          3322.44,
                          6644.88]),
    "A" : Tone("A", 9, [27.50,
                        55.00,
                        110.00,
                        220.00,
                        440.00,
                        880.00,
                        1760.00,
                        3520.00,
                        7040.00]),
    "A#" : Tone("A#", 10, [29.14,
                           58.27,
                           116.54,
                           233.08,
                           466.16,
                           932.33,
                           1864.66,
                           3729.31,
                           7458.62]),
    "B" : Tone("B",11,[30.87,
                       61.74,
                       123.47,
                       246.94,
                       493.88,
                       987.77,
                       1975.53,
                       3951.07,
                       7902.13])
}

def findTone(freq):
    lastf = 16.35 #frequency of C0
    target = -1
    for f in toneNames.keys():
        if(f>freq):
            if(abs(f-freq)<abs(lastf-freq)):
                target = f
            else:
                target = lastf
            break
        else:
            lastf = f
    if target == -1:
        target = 7902.13 #frequency of B8
    
    return universalTones[toneNames[target]]


def findInterval(tone1: Tone, tone2: Tone):
    return abs(tone1.index - tone2.index)


testTone = findTone(32.70)
testTone2 = findTone(30.87)
print(testTone.name, testTone.index)
print(testTone2.name, testTone2.index)

print(findInterval(testTone2, testTone))
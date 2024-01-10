from machine import Pin, time_pulse_us
import utime
import time

# Constants
totallength = 22
channelstart = 0
commandstart = 4
channellength = 4
commandlength = 18
headerlower = 2300
headernom = 2550
headerupper = 2800
zerolower = 300
zeronom = 380
zeroupper = 650
onelower = 800
onenom = 850
oneupper = 1100
highnom = 630

# Button codes
forward = 898819
backward = 964611
sideright = 703491
sideleft = 637699
fleft = 1030403
fright = 571907
bleft = 834819
bright = 900611
fclockwise = 966403
fcounter = 1032195
bclockwise = 573699
bcounter = 639491
headleft = 907015
headright = 775948
leanforward = 841478
leanback = 1038081
lpunch = 922368
r12 = 661248
lchop = 858368
sidechopl = 663040
combopunch = 597248
rpunch = 988160
rchop = 924160
l12 = 792576
sidechopr = 728832
lbackhand = 529664
doublechop = 989952
doublebackhand = 925952
slapping = 860160
rbackhand = 595456
upperchop = 531456
roundhousel = 991744
roundhouser = 533248
forwardkickl = 599040
forwardkickr = 664832
sidekickl = 730624
roundhouselr = 666624
forwardkicklr = 732416
combokick = 798208
sidekickr = 796416
backkickl = 927744
backkickr = 993536
highkickl = 864000
highkickr = 995328
splits1 = 536832
guardl = 602624
guardr = 668416
doubleguard1 = 734208
doubleguard2 = 800000
dodgel = 865792
dodger = 931584
duck = 604160
swayback = 669952
upblock = 735744
splits2 = 801536
comboblock = 867328
zero = 1034752
homeposition = 775424
soundoff = 840451
affirm = 540416
disagree = 803328
goodmorning = 934912
greet1 = 1000704
greet2 = 608000
greet3 = 739328
greet4 = 805120
bye1 = 870912
bye2 = 936704
bye3 = 1002496
bye4 = 544000
bye5 = 542208
respect = 869120
thanks1 = 609792
thanks2 = 675584
love1 = 872704
love2 = 938496
love3 = 1004288
standupfront = 933120
standupback = 998912
excited1 = 743168
excited2 = 874496
excited3 = 940288
excited4 = 618752
party = 677376
amazed = 750336
regret1 = 547584
regret2 = 744960
regret3 = 810752
worry = 679168
pain1 = 1007872
pain2 = 615168
beg1 = 942080
beg2 = 880128
merry = 552960
hilarious = 1013504
hidenseek = 613376
youlike = 682752
mystery5 = 748544
tipsy = 814336
tickleme = 686080
tiredfeet = 751872
needabreak = 817664
wave1 = 883456
wave2 = 949248
applause = 947712
mystery6 = 945920
toosexy = 1015040
clink = 556544
relax = 753664
soccer1 = 885248
soccer2 = 600832
soccer3 = 535040
lift = 819456
countonme = 951040
articulation = 1016832
showoff1 = 558336
showoff2 = 624128
showoff3 = 689920
showoff4 = 821248
cominthrough = 887040
catch = 1006080
pose1 = 771840
pose2 = 903168
pose3 = 968960
mystery1 = 684544
mystery2 = 816128
mystery3 = 881920
mystery4 = 549376
forwardsomersault = 952832
headstandexercises = 1018624
exercises = 560128
airdrum = 625920
airguitar = 691712
randomperformance1 = 954624
randomanimal = 627712
tropicaldance = 825088
giantrobot = 956416
western = 1022208
randomperformance2 = 629504


class Isobot:
    def __init__(self, txpin, rxpin=None):
        self.TXpin = Pin(txpin, Pin.OUT)
        if rxpin is not None:
            self.RXpin = Pin(rxpin, Pin.IN)
        self.bit2 = [0] * 22

    def oscWrite(self, time):
        for _ in range(time // 134 - 1):  # prescaler at 134 for 133MHz
            self.TXpin.value(1)
            utime.sleep_us(13)
            self.TXpin.value(0)
            utime.sleep_us(13)

    def power2(self, power):
        return 2**power

    def compute_checksum(self, hdr, cmd1, cmd2, cmd3):
        # first sum up all bytes
        s = hdr + cmd1 + cmd2 + cmd3
        # then sum up the result, 3 bits at a time
        s = (s & 7) + ((s >> 3) & 7) + ((s >> 6) & 7)
        # return 3 lower bits of the sum
        return s & 7

    def compute_checksum_and_combine(self, hdr, cmd1, cmd2, cmd3):
        checksum = self.compute_checksum(hdr, cmd1, cmd2, cmd3)
        # Combine the header, command bytes, and checksum into a single integer
        return (hdr << 18) | (cmd1 << 12) | (cmd2 << 6) | cmd3 | checksum

    def buttonwrite(self, integer, numoftimes=1):
        self.ItoB(integer, 22)
        for _ in range(numoftimes):
            self.oscWrite(headernom)
            for i in range(totallength):
                utime.sleep_us(zeronom if self.bit2[i] == 0 else onenom)
                self.oscWrite(highnom)
            utime.sleep_ms(205)

    def ItoB(self, integer, length):
        for i in range(length):
            if integer // self.power2(length - 1 - i) == 1:
                integer -= self.power2(length - 1 - i)
                self.bit2[i] = 1
            else:
                self.bit2[i] = 0

    def BtoI(self, start, numofbits, bit):
        integer = 0
        i = start
        n = 0
        while n < numofbits:
            integer += bit[i] * self.power2((numofbits - n - 1))
            i += 1
            n += 1
        return integer

    def receivecode(self):
        bit = [0] * totallength
        plen = [0] * totallength
        i = 0
        while self.RXpin.value() == 1:
            pass
        for i in range(totallength):
            plen[i] = time_pulse_us(self.RXpin, 1)
        for i in range(totallength):
            if zerolower < plen[i] < zeroupper:
                bit[i] = 0
            elif onelower < plen[i] < oneupper:
                bit[i] = 1
        channel = bit[0]
        for i in range(totallength):
            plen[i] = 0
        time.sleep(1)
        return self.BtoI(channelstart, totallength, bit)

    def compute_checksum(hdr, cmd1, cmd2, cmd3):
        # first sum up all bytes
        s = hdr + cmd1 + cmd2 + cmd3
        # then sum up the result, 3 bits at a time
        s = (s & 7) + ((s >> 3) & 7) + ((s >> 6) & 7)
        # return 3 lower bits of the sum
        return s & 7


# Assuming Code is a list of commands
Code = [
    forward,  # 0
    backward,  # 1
    sideright,  # 2
    sideleft,  # 3
    fleft,  # 4
    fright,  # 5
    bleft,  # 6
    bright,  # 7
    fclockwise,  # 8
    fcounter,  # 9
    bclockwise,  # 10
    bcounter,  # 11
    headleft,  # 12
    headright,  # 13
    leanforward,  # 14
    leanback,  # 15
    lpunch,  # 16
    r12,  # 17
    lchop,  # 18
    sidechopl,  # 19
    combopunch,  # 20
    rpunch,  # 21
    rchop,  # 22
    l12,  # 23
    sidechopr,  # 24
    lbackhand,  # 25
    doublechop,  # 26
    doublebackhand,  # 27
    slapping,  # 28
    rbackhand,  # 29
    upperchop,  # 30
    roundhousel,  # 31
    roundhouser,  # 32
    forwardkickl,  # 33
    forwardkickr,  # 34
    sidekickl,  # 35
    roundhouselr,  # 36
    forwardkicklr,  # 37
    combokick,  # 38
    sidekickr,  # 39
    backkickl,  # 40
    backkickr,  # 41
    highkickl,  # 42
    highkickr,  # 43
    splits1,  # 44
    guardl,  # 45
    guardr,  # 46
    doubleguard1,  # 47
    doubleguard2,  # 48
    dodgel,  # 49
    dodger,  # 50
    duck,  # 51
    swayback,  # 52
    upblock,  # 53
    splits2,  # 54
    comboblock,  # 55
    zero,  # 56
    homeposition,  # 57
    soundoff,  # 58
    affirm,  # 59
    disagree,  # 60
    goodmorning,  # 61
    greet1,  # 62
    greet2,  # 63
    greet3,  # 64
    greet4,  # 65
    bye1,  # 66
    bye2,  # 67
    bye3,  # 68
    bye4,  # 69
    bye5,  # 70
    respect,  # 71
    thanks1,  # 72
    thanks2,  # 73
    love1,  # 74
    love2,  # 75
    love3,  # 76
    standupfront,  # 77
    standupback,  # 78
    excited1,  # 79
    excited2,  # 80
    excited3,  # 81
    excited4,  # 82
    party,  # 83
    amazed,  # 84
    regret1,  # 85
    regret2,  # 86
    regret3,  # 87
    worry,  # 88
    pain1,  # 89
    pain2,  # 90
    beg1,  # 91
    beg2,  # 92
    merry,  # 93
    hilarious,  # 94
    hidenseek,  # 95
    youlike,  # 96
    mystery5,  # 97
    tipsy,  # 98
    tickleme,  # 99
    tiredfeet,  # 100
    needabreak,  # 101
    wave1,  # 102
    wave2,  # 103
    applause,  # 104
    mystery6,  # 105
    toosexy,  # 106
    clink,  # 107
    relax,  # 108
    soccer1,  # 109
    soccer2,  # 110
    soccer3,  # 111
    lift,  # 112
    countonme,  # 113
    articulation,  # 114
    showoff1,  # 115
    showoff2,  # 116
    showoff3,  # 117
    showoff4,  # 118
    cominthrough,  # 119
    catch,  # 120
    randomperformance2,  # 121
    western,  # 122
    giantrobot,  # 123
    tropicaldance,  # 124
    randomanimal,  # 125
    randomperformance1,  # 126
    airguitar,  # 127
    airdrum,  # 128
    exercises,  # 129
    headstandexercises,  # 130
    forwardsomersault,  # 131
    mystery4,  # 132
    mystery3,  # 133
    mystery2,  # 134
    mystery1,  # 135
    pose3,  # 136
    pose2,  # 137
    pose1,
]  # 138

isobot = Isobot(5, 0)  # tx is IR OUT pin


def serial_command():
    data1 = input("Please enter the command number")
    i = int(data1)

    if i <= 11:
        for k in range(1):
            print(Code[i])
            isobot.buttonwrite(Code[i], 3)
    else:
        print(Code[i])
        isobot.buttonwrite(Code[i], 3)

    data0 = input("Please enter the command number")
    ir = int(data0)

    if ir <= 11:
        for k in range(1):
            print(Code[ir])
            isobot.buttonwrite(Code[ir], 3)
    else:
        print(Code[ir])
        isobot.buttonwrite(Code[ir], 3)


while True:
    serial_command()
    time.sleep_ms(10)

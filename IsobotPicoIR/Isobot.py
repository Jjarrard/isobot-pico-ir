from Isobot_Module import (
    Isobot,
    forward,
    backward,
    sideright,
    sideleft,
    fleft,
    fright,
    bleft,
    bright,
    fclockwise,
    fcounter,
    bclockwise,
    bcounter,
    headleft,
    headright,
    leanforward,
    leanback,
    lpunch,
    r12,
    lchop,
    sidechopl,
    combopunch,
    rpunch,
    rchop,
    l12,
    sidechopr,
    lbackhand,
    doublechop,
    doublebackhand,
    slapping,
    rbackhand,
    upperchop,
    roundhousel,
    roundhouser,
    forwardkickl,
    forwardkickr,
    sidekickl,
    roundhouselr,
    forwardkicklr,
    combokick,
    sidekickl,
    sidekickr,
    backkickl,
    backkickr,
    highkickl,
    highkickr,
    splits1,
    guardl,
    guardr,
    doubleguard1,
    doubleguard2,
    dodgel,
    dodger,
    duck,
    swayback,
    upblock,
    splits2,
    comboblock,
    zero,
    homeposition,
    soundoff,
    affirm,
    disagree,
    goodmorning,
    greet1,
    greet2,
    greet3,
    greet4,
    bye1,
    bye2,
    bye3,
    bye4,
    bye5,
    respect,
    thanks1,
    thanks2,
    love1,
    love2,
    love3,
    standupfront,
    standupback,
    excited1,
    excited2,
    excited3,
    excited4,
    party,
    amazed,
    regret1,
    regret2,
    regret3,
    worry,
    pain1,
    pain2,
    beg1,
    beg2,
    merry,
    hilarious,
    hidenseek,
    youlike,
    mystery5,
    tipsy,
    tickleme,
    tiredfeet,
    needabreak,
    wave1,
    wave2,
    applause,
    mystery6,
    toosexy,
    clink,
    relax,
    soccer1,
    soccer2,
    soccer3,
    lift,
    countonme,
    articulation,
    showoff1,
    showoff2,
    showoff3,
    showoff4,
    cominthrough,
    catch,
    randomperformance2,
    western,
    giantrobot,
    tropicaldance,
    randomanimal,
    randomperformance1,
    airguitar,
    airdrum,
    exercises,
    headstandexercises,
    forwardsomersault,
    mystery4,
    mystery3,
    mystery2,
    mystery1,
    pose3,
    pose2,
    pose1,
)
from machine import Pin
import time

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

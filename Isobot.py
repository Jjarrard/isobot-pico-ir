from machine import Pin, time_pulse_us
import utime
import time

# Pico MicroPython I-Sobot IR Remote Control by JJarrard.

# Plug IR LED into pin 5 and GND, send commands 0-138 via shell (I used Thonny to test).

# Code analysed and translated/ported from Miles Moody's Isobot Arduino library.
# Thanks Miles for doing the hard work!
# Like Miles's library this is code is free and open to the public to do whatever you want with it.

# Thanks to
# Michal K for some IR explanation https://minkbot.blogspot.com/2009/08/isobot-infrared-remote-protocol-hack.html
# Takaoka Ishii for the teardown https://robot.watch.impress.co.jp/cda/column/2007/11/08/731.html
# and this was kinda interesting too https://i-sobothacking.blogspot.com/2007/12/i-sobot-controller-overview-2.html

# If the links are dead, use waybackmachine, I found myself using it for hours trawling old forums.

# Notes from that Miles' library:
# carrier freq of about 38khz
# header pulse of 2550 micros high
# 22 data bits=4 for channel number, 18 for button number
# highs carry no info and are 550 micros each
# lows are logic 0 if 550 micros, logic 1 if 1050 micros
# at end of stream or in between, 205 millis low
# note: my ir reciever pin goes low when it detects high signal
#      and stays high when nothing is being recieved
#      that could cause some confusion

# Ngl I have no idea what any of this means and I'm just translating the code.
# I tried to keep it as verbose as possible as you can see from the comments.

# Constants
totallength = 22  # number of highs=bits 4 channel +18 command
channelstart = 0
commandstart = 4  # bit where command starts
channellength = 4
commandlength = 18


headerlower = 2300  # lower limit
headernom = 2550  # nominal
headerupper = 2800  # upper limit
zerolower = 300
zeronom = 380
zeroupper = 650
onelower = 800
onenom = 850  # nominal
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
    # initialize an instance of the Isobot class.
    def __init__(self, txpin, rxpin=None):
        # Set the TXpin to the specified pin, configured as an output pin
        self.TXpin = Pin(txpin, Pin.OUT)

        # If an RXpin is specified...
        if rxpin is not None:
            # ...set the RXpin to the specified pin, configured as an input pin
            self.RXpin = Pin(rxpin, Pin.IN)

        # Initialize the bit2 array with 22 zeros
        self.bit2 = [0] * 22

    # Generate a square wave signal on the TXpin for a specified amount of time.
    def oscWrite(self, time):
        # For each cycle in the specified time (divided by 219)...
        # Got this value from calculating the Arduino prescaler.
        # prescaler = (125MHz / 16MHz) * 28 ≈ 218.75
        for _ in range(time // 219 - 1):
            # ...set the TXpin high...
            self.TXpin.value(1)
            # ...wait for 13 microseconds...
            utime.sleep_us(13)
            # ...set the TXpin low...
            self.TXpin.value(0)
            # ...and wait for another 13 microseconds
            utime.sleep_us(13)

    # Calculate 2 to the power of a given number.
    def power2(self, power):
        # Return 2 to the power of the specified number
        return (
            2**power
        )  # The ** operator is used to perform exponentiation in Python.

    # Compute a checksum for a command
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

    def buttonwrite(self, integer):
        # Convert the integer to binary and store it in the bit2 array
        self.integer_to_binary(integer, 22)
        # Write the header signal
        self.oscWrite(headernom)
        # For each bit in the binary representation of the integer...
        for i in range(totallength):
            # ...if the bit is 0, wait for the duration of a 'zero' signal...
            if self.bit2[i] == 0:
                utime.sleep_us(zeronom)
            # ...otherwise, wait for the duration of a 'one' signal
            else:
                utime.sleep_us(onenom)
            # Write a 'high' signal
            self.oscWrite(highnom)
        # Wait for 205 milliseconds
        utime.sleep_ms(205)

    # Send a command to the iSobot robot a specified number of times.
    def buttonwrite(self, integer, numoftimes=1):
        # Convert the integer command to binary and store it in the bit2 array
        self.integer_to_binary(integer, 22)

        # Repeat the following process numoftimes
        for _ in range(numoftimes):
            # Send the header signal
            self.oscWrite(headernom)

            # For each bit in the command...
            for i in range(totallength):
                # ...if the bit is 0, wait for a short time, otherwise wait for a longer time
                utime.sleep_us(zeronom if self.bit2[i] == 0 else onenom)

                # Send a high signal
                self.oscWrite(highnom)

            # Wait for a short time before repeating the process
            utime.sleep_ms(205)

    # Convert an integer into a binary representation and store it in the bit2 array.
    def integer_to_binary(self, integer, length):
        # For each bit in the binary representation...
        for i in range(length):
            # ...if the integer divided by 2 to the power of (length - 1 - i) is 1...
            if integer // self.power2(length - 1 - i) == 1:
                # ...subtract that power of 2 from the integer...
                integer -= self.power2(length - 1 - i)

                # ...and set the corresponding bit in the bit2 array to 1
                self.bit2[i] = 1
            else:
                # ...otherwise, set the corresponding bit in the bit2 array to 0
                self.bit2[i] = 0

    def binary_to_integer(self, start, numofbits, bit):
        # Initialize the integer to 0
        integer = 0
        # Set i to the start index
        i = start
        # Initialize a counter n to 0
        n = 0
        # While n is less than the number of bits...
        while n < numofbits:
            # ...add to the integer the value of the current bit times 2 to the power of (numofbits - n - 1)
            integer += bit[i] * self.power2((numofbits - n - 1))
            # Increment the index and the counter
            i += 1
            n += 1
        # Return the resulting integer
        return integer

    def receivecode(self):
        # Initialize an array of bits and an array of pulse lengths, both of size totallength
        bit = [0] * totallength
        plen = [0] * totallength

        # Wait until the RX pin is low
        while self.RXpin.value() == 1:
            pass

        # Measure the length of each pulse and store it in the plen array
        for i in range(totallength):
            plen[i] = time_pulse_us(self.RXpin, 1)

        # Determine the value of each bit based on the length of the corresponding pulse
        for i in range(totallength):
            if zerolower < plen[i] < zeroupper:
                bit[i] = 0
            elif onelower < plen[i] < oneupper:
                bit[i] = 1

        # The first bit is the channel
        channel = bit[0]

        # Reset the plen array
        for i in range(totallength):
            plen[i] = 0

        # Wait for 1 second
        time.sleep(1)

        # Convert the binary representation in the bit array to an integer and return it
        return self.binary_to_integer(channelstart, totallength, bit)

    def compute_checksum(self, hdr, cmd1, cmd2, cmd3):
        # Sum up all the command bytes
        s = hdr + cmd1 + cmd2 + cmd3
        # Then sum up the result, 3 bits at a time
        s = (s & 7) + ((s >> 3) & 7) + ((s >> 6) & 7)
        # Return the 3 lower bits of the sum
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
    pose1,  # 138
]

isobot = Isobot(5, 0)  # tx is IR OUT pin


def serial_command():
    # Request a command number from the user
    data1 = input("Please enter the command number")
    # Convert the input to an integer
    i = int(data1)

    # If the command number is less than or equal to 11...
    if i <= 11:
        # ...print the corresponding command and send it to the iSobot robot 3 times
        for k in range(5):
            print(Code[i])
            isobot.buttonwrite(Code[i], 3)
    else:
        # ...otherwise, print the command and send it to the robot 3 times
        print(Code[i])
        isobot.buttonwrite(Code[i], 3)

    # Request another command number from the user
    data0 = input("Please enter the command number")
    # Convert the input to an integer
    ir = int(data0)

    # If the command number is less than or equal to 11...
    if ir <= 11:
        # ...print the corresponding command and send it to the iSobot robot 3 times
        for k in range(5):
            print(Code[ir])
            isobot.buttonwrite(Code[ir], 3)
    else:
        # ...otherwise, print the command and send it to the robot 3 times
        print(Code[ir])
        isobot.buttonwrite(Code[ir], 3)


# Continuously call the serial_command function with a 10 millisecond delay between each call
while True:
    serial_command()
    time.sleep_ms(100)

# The original python code for the Sieve of Atkin (SoA)
# and Sieve of Eratosthenes (SoE) was presented here:
# http://krenzel.info/static/atkin.py
# It has been subsequently cosmetically modified.
# I then added versions of P3 & P5 for the Sieve of Zakiya (SoZ).
# George Sakkis subsequently further modified this code here:
# http://codepad.org/C2nQ8syr
# He explained the modifications here:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/acb3349e84a39f26/0d6a3a84b4372ebf?lnk=gst&q=Ultimate+Prime+Sieve#0d6a3a84b4372ebf
# Using this code, I added more efficient/optimized versions
# of P3 & P5, along with handcoded versions of P7 & P11.
# This is the code presented herein.
#
# Running this code on an Intel P4, 2.8Ghz, 1 GB laptop,
# with PCLinuxOS, and Python 2.4.3, I note the following.
# The SoZ versions run much faster than the SoA in pure Python.
# When psyco is used the SoA is significantly faster than the
# pure Python version. The SoZ versions are faster too, but now
# they are slower than the SoA.
# See difference by commenting out: import psyco; psyco.full()
# 
# Jabari Zakiya - 2008/7/19

#import psyco; psyco.full()
from math import sqrt, ceil

def sieveOfAtkin(end):
    end += 1
    lng = (end/2)-1+(end&1)
    sieve = [False]*(lng + 1)
    x_max, x2 = int(sqrt((end-1)/4.0)), 0
    for xd in xrange(4, 8*x_max + 2, 8):
        x2 += xd
        y_max = int(sqrt(end-x2))
        n = x2 + y_max*y_max
        n_diff = (y_max << 1) - 1
        if n&1 == 0: n -= n_diff; n_diff -= 2
        for d in xrange((n_diff - 1) << 1, -1, -8):
            m = n%12
            if (m == 1 or m == 5):
                m = n >> 1; sieve[m] = not sieve[m]
            n -= d

    x_max, x2 = int(sqrt((end-1)/3.0)), 0
    for xd in xrange(3, 6*x_max + 2, 6):
        x2 += xd
        y_max = int(sqrt(end-x2))
        n = x2 + y_max*y_max
        n_diff = (y_max << 1) - 1
        if n&1 == 0: n -= n_diff; n_diff -= 2
        for d in xrange((n_diff - 1) << 1, -1, -8):
            if (n%12 == 7):
                m = n >> 1; sieve[m] = not sieve[m]
            n -= d

    x_max, y_min, x2, xd = int((2 + sqrt(4-8*(1-end)))/4), -1, 0, 3
    for x in xrange(1, x_max + 1):
        x2 += xd
        xd += 6
        if x2 >= end: y_min = (((int(ceil(sqrt(x2-end)))- 1) << 1)- 2) << 1
        n = ((x*x + x) << 1) - 1
        n_diff = (((x-1) << 1) - 2) << 1
        for d in xrange(n_diff, y_min, -8):
            if (n%12 == 11):
                m = n >> 1; sieve[m] = not sieve[m]
            n += d

    primes = [2,3]; append= primes.append
    if end <= 3 : return primes[:max(0,end-2)]
    sqrtN  = int(sqrt(end)) + 1
    for n in xrange(2, sqrtN >> 1):
        if sieve[n]:
            i = (n << 1) +1;  j=i*i;  append(i)
            for k in xrange(j, end, 2*j):
                sieve[k>>1] = False
    if sqrtN&1 == 0: sqrtN += 1
    primes.extend([i for i in xrange(sqrtN, end, 2) if sieve[i >> 1]])
    return primes

def sieveOfErat(end):
    if end < 2: return []
    #The array doesn't need to include even numbers
    lng = (end/2)-1+(end&1)
    # Create array and assume all numbers in array are prime
    sieve = [True]*(lng+1)
    # In the following code, you're going to see some funky
    # bit shifting and stuff, this is just transforming i and j
    # so that they represent the proper elements in the array
    # Only go up to square root of the end
    for i in xrange(int(sqrt(end)) >> 1):
        # Skip numbers that aren't marked as prime
        if not sieve[i]: continue
        # Unmark all multiples of i, starting at i**2
        for j in xrange( (i*(i + 3) << 1) + 3, lng, (i << 1) + 3):
            sieve[j] = False
    # Don't forget 2!
    primes = [2]
    # Gather all the primes into a list, leaving out the composite numbers
    primes.extend([(i << 1) + 3 for i in xrange(lng) if sieve[i]])
    return primes

def primesP3(val):
    # all prime candidates > 3 are of form  6*k+(1,5)
    # initialize sieve array with only these candidate values
    # where sieve contains the odd integers representatives
    # convert integers to array indices/vals by i = (n-3)>>1
    n1, n2 = -1, 1; lndx = (val-1)>>1
    sieve = [False]*(lndx+3)
    while  n2 < lndx:
        n1 += 3;   n2 += 3;  sieve[n1] = n1;   sieve[n2] = n2
    # now load sieve with seed primes  < 6, in this case just 5
    sieve[0]=0; sieve[1]=1
    for i in xrange( 1, ((int(sqrt(val))-3)>>1)+1, 1) :
        if not sieve[i]:  continue
        # j  i  5i  7i  6i    p1=5i,  p2=7i,  k=6i
        # 5->1  11  16  15
        j = (i<<1)+3; p1 = (j<<1)+i; p2 = p1+j; k = p2-i
        while p2 < lndx:
           sieve[p1] = sieve[p2] = False;  p1 += k;  p2 += k
        if p1 < lndx:  sieve[p1] = False
    if val < 3 : return [2]
    primes = [(i<<1)+3 for i in xrange(1, lndx, 1)  if sieve[i]]
    primes[0:0] = [2,3]
    return primes

def primesP5(val):
    # all prime candidates > 5 are of form  30*k+(1,7,11,13,17,19,23,29)
    # initialize sieve array with only these candidate values
    # where sieve contains the odd integers representatives
    # convert integers to array indices/vals by  i = (n-3)>>1
    n1, n2, n3, n4, n5, n6, n7, n8 = -1, 2, 4, 5, 7, 8, 10, 13
    lndx = (val-1)>>1; sieve = [False]*(lndx+15)
    while n8 < lndx:
        n1 += 15;   n2 += 15;   n3 += 15;   n4 += 15
        n5 += 15;   n6 += 15;   n7 += 15;   n8 += 15
        sieve[n1] = n1;  sieve[n2] = n2;  sieve[n3] = n3;  sieve[n4] = n4
        sieve[n5] = n5;  sieve[n6] = n6;  sieve[n7] = n7;  sieve[n8] = n8
    # now load sieve with seed primes  < 30
    sieve[0] = 0; sieve[1] = 1; sieve[2] = 2;   sieve[4] = 4; sieve[5] = 5
    sieve[7] = 7; sieve[8] = 8; sieve[10] = 10; sieve[13] = 13
    for i in xrange(2, ((int(sqrt(val))-3)>>1)+1, 1):
        if not sieve[i]:  continue
        # p1=7*i, p2=11*i, p3=13*i --- p6=23*i, p7=29*i, p8=31*i,  k=30*i
        # j  i  7i  11i  13i  17i  19i  23i  29i  31i  30i
        # 7->2  23   37   44   58   65   79  100  107  105	
        j = (i<<1)+3; j2 = j<<1; p1 = j2+j+i; p2 = p1+j2; p3 = p2+j; p4 = p3+j2
        p5 = p4+j; p6 = p5+j2; p7 = p6+j2+j;  p8 = p7+j;  k = p8-i
        while p8 < lndx:
           sieve[p1] = sieve[p2] = sieve[p3] = sieve[p4] = \
           sieve[p5] = sieve[p6] = sieve[p7] = sieve[p8] = False
           p1 += k; p2 += k; p3 += k; p4 += k; p5 += k; p6 += k; p7 += k; p8 += k
        if p7 < lndx:  sieve[p7] = False
        if p6 < lndx:  sieve[p6] = False
        if p5 < lndx:  sieve[p5] = False
        if p4 < lndx:  sieve[p4] = False
        if p3 < lndx:  sieve[p3] = False
        if p2 < lndx:  sieve[p2] = False
        if p1 < lndx:  sieve[p1] = False
    if val < 3 : return [2]
    if val < 5 : return [2,3]
    primes = [(i<<1)+3 for i in xrange(2, lndx, 1)  if sieve[i]]
    primes[0:0] = [2,3,5]
    return primes

def primesP7(val):
    # all prime candidates > 7 are of form  210*k+(1,11,13,17,19,23,29,31,37
    # 41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,121,127,131
    # 137,139,143,149,151,157,163,167,169,173,179,181,187,191,193,197,199,209)
    # initialize sieve array with only these candidate values
    # where sieve contains the odd integers representatives
    # convert integers to array indices/vals by i = (n-3)>>1
    n1, n2, n3, n4, n5, n6, n7, n8, n9, n10 = -1, 4, 5, 7, 8, 10, 13, 14, 17, 19
    n11, n12, n13, n14, n15, n16, n17, n18 = 20, 22, 25, 28, 29, 32, 34, 35
    n19, n20, n21, n22, n23, n24, n25, n26 = 38, 40, 43, 47, 49, 50, 52, 53
    n27, n28, n29, n30, n31, n32, n33, n34 = 55, 62, 64, 67, 68, 73, 74, 77
    n35, n36, n37, n38, n39, n40, n41, n42, n43 = 80,82, 85, 88, 89, 94, 95,97,98
    n44, n45, n46, n47, n48 = 59, 70, 83, 92, 103
    lndx= (val-1)>>1;  sieve = [False]*(lndx+105)
    while n48 < lndx:
        n1 +=105;    n2 += 105;   n3 += 105;   n4 += 105;   n5 += 105
        n6 +=105;    n7 += 105;   n8 += 105;   n9 += 105;  n10 += 105
        n11 +=105;  n12 += 105;  n13 += 105;  n14 += 105;  n15 += 105
        n16 +=105;  n17 += 105;  n18 += 105;  n19 += 105;  n20 += 105
        n21 +=105;  n22 += 105;  n23 += 105;  n24 += 105;  n25 += 105
        n26 +=105;  n27 += 105;  n28 += 105;  n29 += 105;  n30 += 105
        n31 +=105;  n32 += 105;  n33 += 105;  n34 += 105;  n35 += 105
        n36 +=105;  n37 += 105;  n38 += 105;  n39 += 105;  n40 += 105
        n41 +=105;  n42 += 105;  n43 += 105;  n44 += 105;  n45 += 105
        n46 +=105;  n47 += 105;  n48 += 105
        sieve[n1] = n1;    sieve[n2] = n2;    sieve[n3] = n3;    sieve[n4] = n4
        sieve[n5] = n5;    sieve[n6] = n6;    sieve[n7] = n7;    sieve[n8] = n8
        sieve[n9] = n9;    sieve[n10] = n10;  sieve[n11] = n11;  sieve[n12] = n12
        sieve[n13] = n13;  sieve[n14] = n14;  sieve[n15] = n15;  sieve[n16] = n16
        sieve[n17] = n17;  sieve[n18] = n18;  sieve[n19] = n19;  sieve[n20] = n20
        sieve[n21] = n21;  sieve[n22] = n22;  sieve[n23] = n23;  sieve[n24] = n24
        sieve[n25] = n25;  sieve[n26] = n26;  sieve[n27] = n27;  sieve[n28] = n28
        sieve[n29] = n29;  sieve[n30] = n30;  sieve[n31] = n31;  sieve[n32] = n32
        sieve[n33] = n33;  sieve[n34] = n34;  sieve[n35] = n35;  sieve[n36] = n36
        sieve[n37] = n37;  sieve[n38] = n38;  sieve[n39] = n39;  sieve[n40] = n40
        sieve[n41] = n41;  sieve[n42] = n42;  sieve[n43] = n43;  sieve[n44] = n44 
        sieve[n45] = n45;  sieve[n46] = n46;  sieve[n47] = n47;  sieve[n48] = n48
    # now initialize sieve with the (odd) primes < 210, resize array
    sieve[0]=0;    sieve[1]=1;    sieve[2]=2;    sieve[4]=4;    sieve[5]=5
    sieve[7]=7;    sieve[8]=8;    sieve[10]=10;  sieve[13]=13;  sieve[14]=14
    sieve[17]=17;  sieve[19]=19;  sieve[20]=20;  sieve[22]=22;  sieve[25]=25
    sieve[28]=28;  sieve[29]=29;  sieve[32]=32;  sieve[34]=34;  sieve[35]=35
    sieve[38]=38;  sieve[40]=40;  sieve[43]=43;  sieve[47]=47;  sieve[49]=49
    sieve[50]=50;  sieve[52]=52;  sieve[53]=53;  sieve[55]=55;  sieve[62]=62
    sieve[64]=64;  sieve[67]=67;  sieve[68]=68;  sieve[73]=73;  sieve[74]=74
    sieve[77]=77;  sieve[80]=80;  sieve[82]=82;  sieve[85]=85;  sieve[88]=88
    sieve[89]=89;  sieve[94]=94;  sieve[95]=95;  sieve[97]=97;  sieve[98]=98
    for i in xrange(4, ((int(sqrt(val))-3)>>1)+1, 1):
        if not sieve[i]:  continue
        # residues are (11,13,17,19,23, 29,31,37 41,43, 47,53,59,61,67, 71,73,79,83,89,
        # 97,101,103,107,109, 113,121,127,131,137, 139,143,149,151,157,
        # 163,167,169,173,179, 181,187,191,193,197, 199,209, 211)	
        # p1=11*i, p2=13*i, p3=17*i -- p46=199*i, p47=209*i, p48=211*i,  k=210*i
        #  j  i 11i 13i 17i 19i 23i 29i 31i 37i..193i 197i 199i 209i 211i 210i
        # 11->4  59  70  92 103 125 191 202 128  1060 1082 1093 1148 1159 1155
        j=(i<<1)+3; j2=j<<1; j3=j2+j; j4=j2<<1; j5=j4+j
        p1=j5+i; p2=p1+j; p3=p2+j2; p4=p3+j; p5=p4+j2; p6=p5+j3; p7=p6+j; p8=p7+j3
        p9=p8+j2; p10=p9+j; p11=p10+j2; p12=p11+j3; p13=p12+j3; p14=p13+j;p15=p14+j3
        p16=p15+j2; p17=p16+j;  p18=p17+j3; p19=p18+j2; p20=p19+j3; p21=p20+j4
        p22=p21+j2; p23=p22+j;  p24=p23+j2; p25=p24+j;  p26=p25+j2; p27=p26+j4
        p28=p27+j3; p29=p28+j2; p30=p29+j3; p31=p30+j;  p32=p31+j2; p33=p32+j3
        p34=p33+j;  p35=p34+j3; p36=p35+j3; p37=p36+j2; p38=p37+j;  p39=p38+j2
        p40=p39+j3; p41=p40+j;  p42=p41+j3; p43=p42+j2; p44=p43+j;  p45=p44+j2
        p46=p45+j;  p47=p46+j5; p48=p47+j;  k = p48-i
        while p48 < lndx:
           sieve[p1] = sieve[p2] = sieve[p3] = sieve[p4] = sieve[p5] = sieve[p6]=  \
           sieve[p7] = sieve[p8] = sieve[p9] = sieve[p10]= sieve[p11]= sieve[p12]= \
           sieve[p13]= sieve[p14]= sieve[p15]= sieve[p16]= sieve[p17]= sieve[p18]= \
           sieve[p19]= sieve[p20]= sieve[p21]= sieve[p22]= sieve[p23]= sieve[p24]= \
           sieve[p25]= sieve[p26]= sieve[p27]= sieve[p28]= sieve[p29]= sieve[p30]= \
           sieve[p31]= sieve[p32]= sieve[p33]= sieve[p34]= sieve[p35]= sieve[p36]= \
           sieve[p37]= sieve[p38]= sieve[p39]= sieve[p40]= sieve[p41]= sieve[p42]= \
           sieve[p43]= sieve[p44]= sieve[p45]= sieve[p46]= sieve[p47]= sieve[p48]= False
           p1 += k; p2 += k; p3 += k; p4 += k; p5 += k; p6 += k; p7 += k; p8 += k
           p9 += k; p10 +=k; p11 +=k; p12 +=k; p13 +=k; p14 +=k; p15 +=k; p16 +=k
           p17 +=k; p18 +=k; p19 +=k; p20 +=k; p21 +=k; p22 +=k; p23 +=k; p24 +=k
           p25 +=k; p26 +=k; p27 +=k; p28 +=k; p29 +=k; p30 +=k; p31 +=k; p32 +=k
           p33 +=k; p34 +=k; p35 +=k; p36 +=k; p37 +=k; p38 +=k; p39 +=k; p40 +=k
           p41 +=k; p42 +=k; p43 +=k; p44 +=k; p45 +=k; p46 +=k; p47 +=k; p48 +=k
        if p47 < lndx: sieve[p47] = False 
        if p46 < lndx: sieve[p46] = False
        if p45 < lndx: sieve[p45] = False
        if p44 < lndx: sieve[p44] = False
        if p43 < lndx: sieve[p43] = False
        if p42 < lndx: sieve[p42] = False
        if p41 < lndx: sieve[p41] = False
        if p40 < lndx: sieve[p40] = False
        if p39 < lndx: sieve[p39] = False
        if p38 < lndx: sieve[p38] = False
        if p37 < lndx: sieve[p37] = False
        if p36 < lndx: sieve[p36] = False
        if p35 < lndx: sieve[p35] = False
        if p34 < lndx: sieve[p34] = False
        if p33 < lndx: sieve[p33] = False
        if p32 < lndx: sieve[p32] = False
        if p31 < lndx: sieve[p31] = False
        if p30 < lndx: sieve[p30] = False
        if p29 < lndx: sieve[p29] = False
        if p28 < lndx: sieve[p28] = False
        if p27 < lndx: sieve[p27] = False
        if p26 < lndx: sieve[p26] = False
        if p25 < lndx: sieve[p25] = False
        if p24 < lndx: sieve[p24] = False
        if p23 < lndx: sieve[p23] = False
        if p22 < lndx: sieve[p22] = False
        if p21 < lndx: sieve[p21] = False
        if p20 < lndx: sieve[p20] = False
        if p19 < lndx: sieve[p19] = False
        if p18 < lndx: sieve[p18] = False
        if p17 < lndx: sieve[p17] = False
        if p16 < lndx: sieve[p16] = False
        if p15 < lndx: sieve[p15] = False
        if p14 < lndx: sieve[p14] = False
        if p13 < lndx: sieve[p13] = False
        if p12 < lndx: sieve[p12] = False
        if p11 < lndx: sieve[p11] = False
        if p10 < lndx: sieve[p10] = False
        if p9  < lndx: sieve[p9]  = False
        if p8  < lndx: sieve[p8]  = False
        if p7  < lndx: sieve[p7]  = False
        if p6  < lndx: sieve[p6]  = False
        if p5  < lndx: sieve[p5]  = False
        if p4  < lndx: sieve[p4]  = False
        if p3  < lndx: sieve[p3]  = False
        if p2  < lndx: sieve[p2]  = False
        if p1  < lndx: sieve[p1]  = False
    if val < 3 : return [2]
    if val < 5 : return [2,3]
    if val < 7 : return [2,3,5]
    primes = [(i<<1)+3 for i in xrange(4, lndx, 1)  if sieve[i]]
    primes[0:0] = [2,3,5,7]
    return primes

def primesP11(val):
    # all prime candidates > 11 are of form  2310*k+(1,13,17,19,23,29,31,37,41
    # 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    # 127, 131, 137, 139, 149, 151, 157, 163, 167, 169, 173, 179, 181, 191, 193,
    # 197, 199, 211, 221, 223, 227, 229, 233, 239, 241, 247, 251, 257, 263, 269,
    # 271, 277, 281, 283, 289, 293, 299, 307, 311, 313, 317, 323, 331, 337, 347,
    # 349, 353, 359, 361, 367, 373, 377, 379, 383, 389, 391, 397, 401, 403, 409,
    # 419, 421, 431, 433, 437, 439, 443, 449, 457, 461, 463, 467, 479, 481, 487,
    # 491, 493, 499, 503, 509, 521, 523, 527, 529, 533, 541, 547, 551, 557, 559,
    # 563, 569, 571, 577, 587, 589, 593, 599, 601, 607, 611, 613, 617, 619, 629,
    # 631, 641, 643, 647, 653, 659, 661, 667, 673, 677, 683, 689, 691, 697, 701,
    # 703, 709, 713, 719, 727, 731, 733, 739, 743, 751, 757, 761, 767, 769, 773,
    # 779, 787, 793, 797, 799, 809, 811, 817, 821, 823, 827, 829, 839, 841, 851,
    # 853, 857, 859, 863, 871, 877, 881, 883, 887, 893, 899, 901, 907, 911, 919,
    # 923, 929, 937, 941, 943, 947, 949, 953, 961, 967, 971, 977, 983, 989, 991,
    # 997, 1003, 1007, 1009, 1013, 1019, 1021, 1027, 1031, 1033, 1037, 1039, 1049,
    # 1051,1061, 1063, 1069, 1073, 1079, 1081, 1087, 1091, 1093, 1097, 1103, 1109,
    # 1117,1121, 1123, 1129, 1139, 1147, 1151, 1153, 1157, 1159, 1163, 1171, 1181,
    # 1187,1189, 1193, 1201, 1207, 1213, 1217, 1219, 1223, 1229, 1231, 1237, 1241,
    # 1247,1249, 1259, 1261, 1271, 1273, 1277, 1279, 1283, 1289, 1291, 1297, 1301,
    # 1303,1307, 1313, 1319, 1321, 1327, 1333, 1339, 1343, 1349, 1357, 1361, 1363,
    # 1367,1369, 1373, 1381, 1387, 1391, 1399, 1403, 1409, 1411, 1417, 1423, 1427,
    # 1429,1433, 1439, 1447, 1451, 1453, 1457, 1459, 1469, 1471, 1481, 1483, 1487,
    # 1489,1493, 1499, 1501, 1511, 1513, 1517, 1523, 1531, 1537, 1541, 1543, 1549,
    # 1553,1559, 1567, 1571, 1577, 1579, 1583, 1591, 1597, 1601, 1607, 1609, 1613,
    # 1619,1621, 1627, 1633, 1637, 1643, 1649, 1651, 1657, 1663, 1667, 1669, 1679,
    # 1681,1691, 1693, 1697, 1699, 1703, 1709, 1711, 1717, 1721, 1723, 1733, 1739,
    # 1741,1747, 1751, 1753, 1759, 1763, 1769, 1777, 1781, 1783, 1787, 1789, 1801,
    # 1807,1811, 1817, 1819, 1823, 1829, 1831, 1843, 1847, 1849, 1853, 1861, 1867,
    # 1871,1873, 1877, 1879, 1889, 1891, 1901, 1907, 1909, 1913, 1919, 1921, 1927,
    # 1931,1933, 1937, 1943, 1949, 1951, 1957, 1961, 1963, 1973, 1979, 1987, 1993,
    # 1997,1999, 2003, 2011, 2017, 2021, 2027, 2029, 2033, 2039, 2041, 2047, 2053,
    # 2059,2063, 2069, 2071, 2077, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2117,
    # 2119,2129, 2131, 2137, 2141, 2143, 2147, 2153, 2159, 2161, 2171, 2173, 2179,
    # 2183,2197, 2201, 2203, 2207, 2209, 2213, 2221, 2227, 2231, 2237, 2239, 2243,
    # 2249,2251,2257,2263,2267,2269,2273,2279, 2281, 2287, 2291, 2293, 2297, 2309)
    # initialize sieve array with only these candidate values
    # where sieve contains the odd integers representatives
    # convert integers to array indices/vals by i = (n-3)>>1
    n1, n2, n3, n4, n5, n6, n7, n8, n9, n10 = -1, 5, 7, 8, 10, 13, 14, 17, 19, 20
    n11, n12, n13, n14, n15, n16, n17, n18 = 22, 25, 28, 29, 32, 34, 35, 38
    n19, n20, n21, n22, n23, n24, n25, n26 = 40, 43, 47, 49, 50, 52, 53, 55
    n27, n28, n29, n30, n31, n32, n33, n34 = 62, 64, 67, 68, 73, 74, 77, 80
    n35, n36, n37, n38, n39, n40, n41, n42 = 82, 83, 85, 88, 89, 94, 95, 97
    n43, n44, n45, n46, n47, n48, n49, n50 = 98, 104, 109, 110, 112, 113, 115, 118
    n51, n52, n53, n54, n55, n56, n57, n58 = 119,122, 124, 127, 130, 133, 134, 137
    n59, n60, n61, n62, n63, n64, n65, n66 = 139,140, 143, 145, 148, 152, 154, 155
    n67, n68, n69, n70, n71, n72, n73, n74 = 157,160, 164, 167, 172, 173, 175, 178
    n75, n76, n77, n78, n79, n80, n81, n82 = 179,182, 185, 187, 188, 190, 193, 194
    n83, n84, n85, n86, n87, n88, n89, n90 = 197,199, 200, 203, 208, 209, 214, 215
    n91, n92, n93, n94, n95, n96, n97, n98 = 217,218, 220, 223, 227, 229, 230, 232
    n99,n100,n101,n102,n103,n104,n105,n106 = 238,239, 242, 244, 245, 248, 250, 253
    n107,n108,n109,n110,n111,n112,n113,n114= 259,260, 262, 263, 265, 269, 272, 274
    n115,n116,n117,n118,n119,n120,n121,n122= 277,278, 280, 283, 284, 287, 292, 293
    n123,n124,n125,n126,n127,n128,n129,n130= 295,298, 299, 302, 304, 305, 307, 308
    n131,n132,n133,n134,n135,n136,n137,n138= 313,314, 319, 320, 322, 325, 328, 329
    n139,n140,n141,n142,n143,n144,n145,n146= 332,335, 337, 340, 343, 344, 347, 349
    n147,n148,n149,n150,n151,n152,n153,n154= 350,353, 355, 358, 362, 364, 365, 368
    n155,n156,n157,n158,n159,n160,n161,n162= 370,374, 377, 379, 382, 383, 385, 388
    n163,n164,n165,n166,n167,n168,n169,n170= 392,395, 397, 398, 403, 404, 407, 409
    n171,n172,n173,n174,n175,n176,n177,n178= 410,412, 413, 418, 419, 424, 425, 427
    n179,n180,n181,n182,n183,n184,n185,n186= 428,430, 434, 437, 439, 440, 442, 445
    n187,n188,n189,n190,n191,n192,n193,n194= 448,449, 452, 454, 458, 460, 463, 467
    n195,n196,n197,n198,n199,n200,n201,n202= 469,470, 472, 473, 475, 479, 482, 484
    n203,n204,n205,n206,n207,n208,n209,n210= 487,490, 493, 494, 497, 500, 502, 503
    n211,n212,n213,n214,n215,n216,n217,n218= 505,508, 509, 512, 514, 515, 517, 518
    n219,n220,n221,n222,n223,n224,n225,n226= 523,524, 529, 530, 533, 535, 538, 539
    n227,n228,n229,n230,n231,n232,n233,n234= 542,544, 545, 547, 550, 553, 557, 559
    n235,n236,n237,n238,n239,n240,n241,n242= 560,563, 568, 572, 574, 575, 577, 578
    n243,n244,n245,n246,n247,n248,n249,n250= 580,584, 589, 592, 593, 595, 599, 602
    n251,n252,n253,n254,n255,n256,n257,n258= 605,607, 608, 610, 613, 614, 617, 619
    n259,n260,n261,n262,n263,n264,n265,n266= 622,623, 628, 629, 634, 635, 637, 638
    n267,n268,n269,n270,n271,n272,n273,n274= 640,643, 644, 647, 649, 650, 652, 655
    n275,n276,n277,n278,n279,n280,n281,n282= 658,659, 662, 665, 668, 670, 673, 677
    n283,n284,n285,n286,n287,n288,n289,n290= 679,680, 682, 683, 685, 689, 692, 694
    n291,n292,n293,n294,n295,n296,n297,n298= 698,700, 703, 704, 707, 710, 712, 713
    n299,n300,n301,n302,n303,n304,n305,n306= 715,718, 722, 724, 725, 727, 728, 733
    n307,n308,n309,n310,n311,n312,n313,n314= 734,739, 740, 742, 743, 745, 748, 749
    n315,n316,n317,n318,n319,n320,n321,n322= 754,755, 757, 760, 764, 767, 769, 770
    n323,n324,n325,n326,n327,n328,n329,n330= 773,775, 778, 782, 784, 787, 788, 790
    n331,n332,n333,n334,n335,n336,n337,n338= 794,797, 799, 802, 803, 805, 808, 809
    n339,n340,n341,n342,n343,n344,n345,n346= 812,815, 817, 820, 823, 824, 827, 830
    n347,n348,n349,n350,n351,n352,n353,n354= 832,833, 838, 839, 844, 845, 847, 848
    n355,n356,n357,n358,n359,n360,n361,n362= 850,853, 854, 857, 859, 860, 865, 868
    n363,n364,n365,n366,n367,n368,n369,n370= 869,872, 874, 875, 878, 880, 883, 887
    n371,n372,n373,n374,n375,n376,n377,n378= 889,890, 892, 893, 899, 902, 904, 907
    n379,n380,n381,n382,n383,n384,n385,n386= 908,910, 913, 914, 920, 922, 923, 925
    n387,n388,n389,n390,n391,n392,n393,n394= 929,932, 934, 935, 937, 938, 943, 944
    n395,n396,n397,n398,n399,n400,n401,n402= 949,952, 953, 955, 958, 959, 962, 964
    n403,n404,n405,n406,n407,n408,n409,n410= 965,967, 970, 973, 974, 977, 979, 980
    n411,n412,n413,n414,n415,n416,n417,n418= 985,988, 992, 995, 997, 998,1000,1004
    n419,n420,n421,n422,n423,n424,n425,n426= 1007,1009,1012,1013,1015,1018,1019,1022
    n427,n428,n429,n430,n431,n432,n433,n434= 1025,1028,1030,1033,1034,1037,1039,1040
    n435,n436,n437,n438,n439,n440,n441,n442= 1042,1043,1048,1054,1055,1057,1058,1063
    n443,n444,n445,n446,n447,n448,n449,n450= 1064,1067,1069,1070,1072,1075,1078,1079
    n451,n452,n453,n454,n455,n456,n457,n458= 1084,1085,1088,1090,1097,1099,1100,1102
    n459,n460,n461,n462,n463,n464,n465,n466= 1103,1105,1109,1112,1114,1117,1118,1120
    n467,n468,n469,n470,n471,n472,n473,n474= 1123,1124,1127,1130,1132,1133,1135,1138
    n475,n476,n477,n478,n479,n480 = 1139, 1142, 1144, 1145, 1147, 1153
    lndx= (val-1)>>1;  sieve = [False]*(lndx+1155)
    while n480 < lndx:
        n1 +=1155;   n2 += 1155;   n3 += 1155;   n4 += 1155;   n5 += 1155
        n6 +=1155;   n7 += 1155;   n8 += 1155;   n9 += 1155;   n10 += 1155
        n11 +=1155;  n12 += 1155;  n13 += 1155;  n14 += 1155;  n15 += 1155
        n16 +=1155;  n17 += 1155;  n18 += 1155;  n19 += 1155;  n20 += 1155
        n21 +=1155;  n22 += 1155;  n23 += 1155;  n24 += 1155;  n25 += 1155
        n26 +=1155;  n27 += 1155;  n28 += 1155;  n29 += 1155;  n30 += 1155
        n31 +=1155;  n32 += 1155;  n33 += 1155;  n34 += 1155;  n35 += 1155
        n36 +=1155;  n37 += 1155;  n38 += 1155;  n39 += 1155;  n40 += 1155
        n41 +=1155;  n42 += 1155;  n43 += 1155;  n44 += 1155;  n45 += 1155
        n46 +=1155;  n47 += 1155;  n48 += 1155;  n49 += 1155;  n50 += 1155
        n51 +=1155;  n52 += 1155;  n53 += 1155;  n54 += 1155;  n55 += 1155
        n56 +=1155;  n57 += 1155;  n58 += 1155;  n59 += 1155;  n60 += 1155
        n61 +=1155;  n62 += 1155;  n63 += 1155;  n64 += 1155;  n65 += 1155
        n66 +=1155;  n67 += 1155;  n68 += 1155;  n69 += 1155;  n70 += 1155
        n71 +=1155;  n72 += 1155;  n73 += 1155;  n74 += 1155;  n75 += 1155
        n76 +=1155;  n77 += 1155;  n78 += 1155;  n79 += 1155;  n80 += 1155
        n81 +=1155;  n82 += 1155;  n83 += 1155;  n84 += 1155;  n85 += 1155
        n86 +=1155;  n87 += 1155;  n88 += 1155;  n89 += 1155;  n90 += 1155
        n91 +=1155;  n92 += 1155;  n93 += 1155;  n94 += 1155;  n95 += 1155
        n96 +=1155;  n97 += 1155;  n98 += 1155;  n99 += 1155; n100 += 1155
        n101 +=1155;n102 += 1155; n103 += 1155; n104 += 1155; n105 += 1155
        n106 +=1155;n107 += 1155; n108 += 1155; n109 += 1155; n110 += 1155
        n111 +=1155;n112 += 1155; n113 += 1155; n114 += 1155; n115 += 1155
        n116 +=1155;n117 += 1155; n118 += 1155; n119 += 1155; n120 += 1155
        n121 +=1155;n122 += 1155; n123 += 1155; n124 += 1155; n125 += 1155
        n126 +=1155;n127 += 1155; n128 += 1155; n129 += 1155; n130 += 1155
        n131 +=1155;n132 += 1155; n133 += 1155; n134 += 1155; n135 += 1155
        n136 +=1155;n137 += 1155; n138 += 1155; n139 += 1155; n140 += 1155
        n141 +=1155;n142 += 1155; n143 += 1155; n144 += 1155; n145 += 1155
        n146 +=1155;n147 += 1155; n148 += 1155; n149 += 1155; n150 += 1155
        n151 +=1155;n152 += 1155; n153 += 1155; n154 += 1155; n155 += 1155
        n156 +=1155;n157 += 1155; n158 += 1155; n159 += 1155; n160 += 1155
        n161 +=1155;n162 += 1155; n163 += 1155; n164 += 1155; n165 += 1155
        n166 +=1155;n167 += 1155; n168 += 1155; n169 += 1155; n170 += 1155
        n171 +=1155;n172 += 1155; n173 += 1155; n174 += 1155; n175 += 1155
        n176 +=1155;n177 += 1155; n178 += 1155; n179 += 1155; n180 += 1155
        n181 +=1155;n182 += 1155; n183 += 1155; n184 += 1155; n185 += 1155
        n186 +=1155;n187 += 1155; n188 += 1155; n189 += 1155; n190 += 1155
        n191 +=1155;n192 += 1155; n193 += 1155; n194 += 1155; n195 += 1155
        n196 +=1155;n197 += 1155; n198 += 1155; n199 += 1155; n200 += 1155
        n201 +=1155;n202 += 1155; n203 += 1155; n204 += 1155; n205 += 1155
        n206 +=1155;n207 += 1155; n208 += 1155; n209 += 1155; n210 += 1155
        n211 +=1155;n212 += 1155; n213 += 1155; n214 += 1155; n215 += 1155
        n216 +=1155;n217 += 1155; n218 += 1155; n219 += 1155; n220 += 1155
        n221 +=1155;n222 += 1155; n223 += 1155; n224 += 1155; n225 += 1155
        n226 +=1155;n227 += 1155; n228 += 1155; n229 += 1155; n230 += 1155
        n231 +=1155;n232 += 1155; n233 += 1155; n234 += 1155; n235 += 1155
        n236 +=1155;n237 += 1155; n238 += 1155; n239 += 1155; n240 += 1155
        n241 +=1155;n242 += 1155; n243 += 1155; n244 += 1155; n245 += 1155
        n246 +=1155;n247 += 1155; n248 += 1155; n249 += 1155; n250 += 1155
        n251 +=1155;n252 += 1155; n253 += 1155; n254 += 1155; n255 += 1155
        n256 +=1155;n257 += 1155; n258 += 1155; n259 += 1155; n260 += 1155
        n261 +=1155;n262 += 1155; n263 += 1155; n264 += 1155; n265 += 1155
        n266 +=1155;n267 += 1155; n268 += 1155; n269 += 1155; n270 += 1155
        n271 +=1155;n272 += 1155; n273 += 1155; n274 += 1155; n275 += 1155
        n276 +=1155;n277 += 1155; n278 += 1155; n279 += 1155; n280 += 1155
        n281 +=1155;n282 += 1155; n283 += 1155; n284 += 1155; n285 += 1155
        n286 +=1155;n287 += 1155; n288 += 1155; n289 += 1155; n290 += 1155
        n291 +=1155;n292 += 1155; n293 += 1155; n294 += 1155; n295 += 1155
        n296 +=1155;n297 += 1155; n298 += 1155; n299 += 1155; n300 += 1155
        n301 +=1155;n302 += 1155; n303 += 1155; n304 += 1155; n305 += 1155
        n306 +=1155;n307 += 1155; n308 += 1155; n309 += 1155; n310 += 1155
        n311 +=1155;n312 += 1155; n313 += 1155; n314 += 1155; n315 += 1155
        n316 +=1155;n317 += 1155; n318 += 1155; n319 += 1155; n320 += 1155
        n321 +=1155;n322 += 1155; n323 += 1155; n324 += 1155; n325 += 1155
        n326 +=1155;n327 += 1155; n328 += 1155; n329 += 1155; n330 += 1155
        n331 +=1155;n332 += 1155; n333 += 1155; n334 += 1155; n335 += 1155
        n336 +=1155;n337 += 1155; n338 += 1155; n339 += 1155; n340 += 1155
        n341 +=1155;n342 += 1155; n343 += 1155; n344 += 1155; n345 += 1155
        n346 +=1155;n347 += 1155; n348 += 1155; n349 += 1155; n350 += 1155
        n351 +=1155;n352 += 1155; n353 += 1155; n354 += 1155; n355 += 1155
        n356 +=1155;n357 += 1155; n358 += 1155; n359 += 1155; n360 += 1155
        n361 +=1155;n362 += 1155; n363 += 1155; n364 += 1155; n365 += 1155
        n366 +=1155;n367 += 1155; n368 += 1155; n369 += 1155; n370 += 1155
        n371 +=1155;n372 += 1155; n373 += 1155; n374 += 1155; n375 += 1155
        n376 +=1155;n377 += 1155; n378 += 1155; n379 += 1155; n380 += 1155
        n381 +=1155;n382 += 1155; n383 += 1155; n384 += 1155; n385 += 1155
        n386 +=1155;n387 += 1155; n388 += 1155; n389 += 1155; n390 += 1155
        n391 +=1155;n392 += 1155; n393 += 1155; n394 += 1155; n395 += 1155
        n396 +=1155;n397 += 1155; n398 += 1155; n399 += 1155; n400 += 1155
        n401 +=1155;n402 += 1155; n403 += 1155; n404 += 1155; n405 += 1155
        n406 +=1155;n407 += 1155; n408 += 1155; n409 += 1155; n410 += 1155
        n411 +=1155;n412 += 1155; n413 += 1155; n414 += 1155; n415 += 1155
        n416 +=1155;n417 += 1155; n418 += 1155; n419 += 1155; n420 += 1155
        n421 +=1155;n422 += 1155; n423 += 1155; n424 += 1155; n425 += 1155
        n426 +=1155;n427 += 1155; n428 += 1155; n429 += 1155; n430 += 1155
        n431 +=1155;n432 += 1155; n433 += 1155; n434 += 1155; n435 += 1155
        n436 +=1155;n437 += 1155; n438 += 1155; n439 += 1155; n440 += 1155
        n441 +=1155;n442 += 1155; n443 += 1155; n444 += 1155; n445 += 1155
        n446 +=1155;n447 += 1155; n448 += 1155; n449 += 1155; n450 += 1155
        n451 +=1155;n452 += 1155; n453 += 1155; n454 += 1155; n455 += 1155
        n456 +=1155;n457 += 1155; n458 += 1155; n459 += 1155; n460 += 1155
        n461 +=1155;n462 += 1155; n463 += 1155; n464 += 1155; n465 += 1155
        n466 +=1155;n467 += 1155; n468 += 1155; n469 += 1155; n470 += 1155
        n471 +=1155;n472 += 1155; n473 += 1155; n474 += 1155; n475 += 1155
        n476 +=1155;n477 += 1155; n478 += 1155; n479 += 1155; n480 += 1155
        sieve[n1] = n1;    sieve[n2] = n2;    sieve[n3] = n3;    sieve[n4] = n4
        sieve[n5] = n5;    sieve[n6] = n6;    sieve[n7] = n7;    sieve[n8] = n8
        sieve[n9] = n9;    sieve[n10] = n10;  sieve[n11] = n11;  sieve[n12] = n12
        sieve[n13] = n13;  sieve[n14] = n14;  sieve[n15] = n15;  sieve[n16] = n16
        sieve[n17] = n17;  sieve[n18] = n18;  sieve[n19] = n19;  sieve[n20] = n20
        sieve[n21] = n21;  sieve[n22] = n22;  sieve[n23] = n23;  sieve[n24] = n24
        sieve[n25] = n25;  sieve[n26] = n26;  sieve[n27] = n27;  sieve[n28] = n28
        sieve[n29] = n29;  sieve[n30] = n30;  sieve[n31] = n31;  sieve[n32] = n32
        sieve[n33] = n33;  sieve[n34] = n34;  sieve[n35] = n35;  sieve[n36] = n36
        sieve[n37] = n37;  sieve[n38] = n38;  sieve[n39] = n39;  sieve[n40] = n40
        sieve[n41] = n41;  sieve[n42] = n42;  sieve[n43] = n43;  sieve[n44] = n44 
        sieve[n45] = n45;  sieve[n46] = n46;  sieve[n47] = n47;  sieve[n48] = n48
        sieve[n49] = n49;  sieve[n50] = n50;  sieve[n51] = n51;  sieve[n52] = n52
        sieve[n53] = n53;  sieve[n54] = n54;  sieve[n55] = n55;  sieve[n56] = n56
        sieve[n57] = n57;  sieve[n58] = n58;  sieve[n59] = n59;  sieve[n60] = n60
        sieve[n61] = n61;  sieve[n62] = n62;  sieve[n63] = n63;  sieve[n64] = n64
        sieve[n65] = n65;  sieve[n66] = n66;  sieve[n67] = n67;  sieve[n68] = n68
        sieve[n69] = n69;  sieve[n70] = n70;  sieve[n71] = n71;  sieve[n72] = n72
        sieve[n73] = n73;  sieve[n74] = n74;  sieve[n75] = n75;  sieve[n76] = n76
        sieve[n77] = n77;  sieve[n78] = n78;  sieve[n79] = n79;  sieve[n80] = n80
        sieve[n81] = n81;  sieve[n82] = n82;  sieve[n83] = n83;  sieve[n84] = n84
        sieve[n85] = n85;  sieve[n86] = n86;  sieve[n87] = n87;  sieve[n88] = n88
        sieve[n89] = n89;  sieve[n90] = n90;  sieve[n91] = n91;  sieve[n92] = n92
        sieve[n93] = n93;  sieve[n94] = n94;  sieve[n95] = n95;  sieve[n96] = n96
        sieve[n97] = n97;  sieve[n98] = n98;  sieve[n99] = n99;  sieve[n100] = n100
        sieve[n101]= n101; sieve[n102]= n102; sieve[n103]= n103; sieve[n104] = n104
        sieve[n105]= n105; sieve[n106]= n106; sieve[n107]= n107; sieve[n108] = n108
        sieve[n109]= n109; sieve[n110]= n110; sieve[n111]= n111; sieve[n112] = n112
        sieve[n113]= n113; sieve[n114]= n114; sieve[n115]= n115; sieve[n116] = n116
        sieve[n117]= n117; sieve[n118]= n118; sieve[n119]= n119; sieve[n120] = n120
        sieve[n121]= n121; sieve[n122]= n122; sieve[n123]= n123; sieve[n124] = n124
        sieve[n125]= n125; sieve[n126]= n126; sieve[n127]= n127; sieve[n128] = n128
        sieve[n129]= n129; sieve[n130]= n130; sieve[n131]= n131; sieve[n132] = n132
        sieve[n133]= n133; sieve[n134]= n134; sieve[n135]= n135; sieve[n136] = n136
        sieve[n137]= n137; sieve[n138]= n138; sieve[n139]= n139; sieve[n140] = n140
        sieve[n141]= n141; sieve[n142]= n142; sieve[n143]= n143; sieve[n144] = n144
        sieve[n145]= n145; sieve[n146]= n146; sieve[n147]= n147; sieve[n148] = n148
        sieve[n149]= n149; sieve[n150]= n150; sieve[n151]= n151; sieve[n152] = n152
        sieve[n153]= n153; sieve[n154]= n154; sieve[n155]= n155; sieve[n156] = n156
        sieve[n157]= n157; sieve[n158]= n158; sieve[n159]= n159; sieve[n160] = n160
        sieve[n161]= n161; sieve[n162]= n162; sieve[n163]= n163; sieve[n164] = n164
        sieve[n165]= n165; sieve[n166]= n166; sieve[n167]= n167; sieve[n168] = n168
        sieve[n169]= n169; sieve[n170]= n170; sieve[n171]= n171; sieve[n172] = n172
        sieve[n173]= n173; sieve[n174]= n174; sieve[n175]= n175; sieve[n176] = n176
        sieve[n177]= n177; sieve[n178]= n178; sieve[n179]= n179; sieve[n180] = n180
        sieve[n181]= n181; sieve[n182]= n182; sieve[n183]= n183; sieve[n184] = n184
        sieve[n185]= n185; sieve[n186]= n186; sieve[n187]= n187; sieve[n188] = n188
        sieve[n189]= n189; sieve[n190]= n190; sieve[n191]= n191; sieve[n192] = n192
        sieve[n193]= n193; sieve[n194]= n194; sieve[n195]= n195; sieve[n196] = n196
        sieve[n197]= n197; sieve[n198]= n198; sieve[n199]= n199; sieve[n200] = n200
        sieve[n201]= n201; sieve[n202]= n202; sieve[n203]= n203; sieve[n204] = n204
        sieve[n205]= n205; sieve[n206]= n206; sieve[n207]= n207; sieve[n208] = n208
        sieve[n209]= n209; sieve[n210]= n210; sieve[n211]= n211; sieve[n212] = n212
        sieve[n213]= n213; sieve[n214]= n214; sieve[n215]= n215; sieve[n216] = n216
        sieve[n217]= n217; sieve[n218]= n218; sieve[n219]= n219; sieve[n220] = n220
        sieve[n221]= n221; sieve[n222]= n222; sieve[n223]= n223; sieve[n224] = n224
        sieve[n225]= n225; sieve[n226]= n226; sieve[n227]= n227; sieve[n228] = n228
        sieve[n229]= n229; sieve[n230]= n230; sieve[n231]= n231; sieve[n232] = n232
        sieve[n233]= n233; sieve[n234]= n234; sieve[n235]= n235; sieve[n236] = n236
        sieve[n237]= n237; sieve[n238]= n238; sieve[n239]= n239; sieve[n240] = n240
        sieve[n241]= n241; sieve[n242]= n242; sieve[n243]= n243; sieve[n244] = n244
        sieve[n245]= n245; sieve[n246]= n246; sieve[n247]= n247; sieve[n248] = n248
        sieve[n249]= n249; sieve[n250]= n250; sieve[n251]= n251; sieve[n252] = n252
        sieve[n253]= n253; sieve[n254]= n254; sieve[n255]= n255; sieve[n256] = n256
        sieve[n257]= n257; sieve[n258]= n258; sieve[n259]= n259; sieve[n260] = n260
        sieve[n261]= n261; sieve[n262]= n262; sieve[n263]= n263; sieve[n264] = n264
        sieve[n265]= n265; sieve[n266]= n266; sieve[n267]= n267; sieve[n268] = n268
        sieve[n269]= n269; sieve[n270]= n270; sieve[n271]= n271; sieve[n272] = n272
        sieve[n273]= n273; sieve[n274]= n274; sieve[n275]= n275; sieve[n276] = n276
        sieve[n277]= n277; sieve[n278]= n278; sieve[n279]= n279; sieve[n280] = n280
        sieve[n281]= n281; sieve[n282]= n282; sieve[n283]= n283; sieve[n284] = n284
        sieve[n285]= n285; sieve[n286]= n286; sieve[n287]= n287; sieve[n288] = n288
        sieve[n289]= n289; sieve[n290]= n290; sieve[n291]= n291; sieve[n292] = n292
        sieve[n293]= n293; sieve[n294]= n294; sieve[n295]= n295; sieve[n296] = n296
        sieve[n297]= n297; sieve[n298]= n298; sieve[n299]= n299; sieve[n300] = n300
        sieve[n301]= n301; sieve[n302]= n302; sieve[n303]= n303; sieve[n304] = n304
        sieve[n305]= n305; sieve[n306]= n306; sieve[n307]= n307; sieve[n308] = n308
        sieve[n309]= n309; sieve[n310]= n310; sieve[n311]= n311; sieve[n312] = n312
        sieve[n313]= n313; sieve[n314]= n314; sieve[n315]= n315; sieve[n316] = n316
        sieve[n317]= n317; sieve[n318]= n318; sieve[n319]= n319; sieve[n320] = n320
        sieve[n321]= n321; sieve[n322]= n322; sieve[n323]= n323; sieve[n324] = n324
        sieve[n325]= n325; sieve[n326]= n326; sieve[n327]= n327; sieve[n328] = n328
        sieve[n329]= n329; sieve[n330]= n330; sieve[n331]= n331; sieve[n332] = n332
        sieve[n333]= n333; sieve[n334]= n334; sieve[n335]= n335; sieve[n336] = n336
        sieve[n337]= n337; sieve[n338]= n338; sieve[n339]= n339; sieve[n340] = n340
        sieve[n341]= n341; sieve[n342]= n342; sieve[n343]= n343; sieve[n344] = n344
        sieve[n345]= n345; sieve[n346]= n346; sieve[n347]= n347; sieve[n348] = n348
        sieve[n349]= n349; sieve[n350]= n350; sieve[n351]= n351; sieve[n352] = n352
        sieve[n353]= n353; sieve[n354]= n354; sieve[n355]= n355; sieve[n356] = n356
        sieve[n357]= n357; sieve[n358]= n358; sieve[n359]= n359; sieve[n360] = n360
        sieve[n361]= n361; sieve[n362]= n362; sieve[n363]= n363; sieve[n364] = n364
        sieve[n365]= n365; sieve[n366]= n366; sieve[n367]= n367; sieve[n368] = n368
        sieve[n369]= n369; sieve[n370]= n370; sieve[n371]= n371; sieve[n372] = n372
        sieve[n373]= n373; sieve[n374]= n374; sieve[n375]= n375; sieve[n376] = n376
        sieve[n377]= n377; sieve[n378]= n378; sieve[n379]= n379; sieve[n380] = n380
        sieve[n381]= n381; sieve[n382]= n382; sieve[n383]= n383; sieve[n384] = n384
        sieve[n385]= n385; sieve[n386]= n386; sieve[n387]= n387; sieve[n388] = n388
        sieve[n389]= n389; sieve[n390]= n390; sieve[n391]= n391; sieve[n392] = n392
        sieve[n393]= n393; sieve[n394]= n394; sieve[n395]= n395; sieve[n396] = n396
        sieve[n397]= n397; sieve[n398]= n398; sieve[n399]= n399; sieve[n400] = n400
        sieve[n401]= n401; sieve[n402]= n402; sieve[n403]= n403; sieve[n404] = n404
        sieve[n405]= n405; sieve[n406]= n406; sieve[n407]= n407; sieve[n408] = n408
        sieve[n409]= n409; sieve[n410]= n410; sieve[n411]= n411; sieve[n412] = n412
        sieve[n413]= n413; sieve[n414]= n414; sieve[n415]= n415; sieve[n416] = n416
        sieve[n417]= n417; sieve[n418]= n418; sieve[n419]= n419; sieve[n420] = n420
        sieve[n421]= n421; sieve[n422]= n422; sieve[n423]= n423; sieve[n424] = n424
        sieve[n425]= n425; sieve[n426]= n426; sieve[n427]= n427; sieve[n428] = n428
        sieve[n429]= n429; sieve[n430]= n430; sieve[n431]= n431; sieve[n432] = n432
        sieve[n433]= n433; sieve[n434]= n434; sieve[n435]= n435; sieve[n436] = n436
        sieve[n437]= n437; sieve[n438]= n438; sieve[n439]= n439; sieve[n440] = n440
        sieve[n441]= n441; sieve[n442]= n442; sieve[n443]= n443; sieve[n444] = n444
        sieve[n445]= n445; sieve[n446]= n446; sieve[n447]= n447; sieve[n448] = n448
        sieve[n449]= n449; sieve[n450]= n450; sieve[n451]= n451; sieve[n452] = n452
        sieve[n453]= n453; sieve[n454]= n454; sieve[n455]= n455; sieve[n456] = n456
        sieve[n457]= n457; sieve[n458]= n458; sieve[n459]= n459; sieve[n460] = n460
        sieve[n461]= n461; sieve[n462]= n462; sieve[n463]= n463; sieve[n464] = n464
        sieve[n465]= n465; sieve[n466]= n466; sieve[n467]= n467; sieve[n468] = n468
        sieve[n469]= n469; sieve[n470]= n470; sieve[n471]= n471; sieve[n472] = n472
        sieve[n473]= n473; sieve[n474]= n474; sieve[n475]= n475; sieve[n476] = n476
        sieve[n477]= n477; sieve[n478]= n478; sieve[n479]= n479; sieve[n480] = n480
    # now initialize sieve with the (odd) primes < 2310, resize array
    sieve[0]=0;      sieve[1]=1;      sieve[2]=2;      sieve[4]=4;      sieve[5]=5
    sieve[7]=7;      sieve[8]=8;      sieve[10]=10;    sieve[13]=13;    sieve[14]=14
    sieve[17]=17;    sieve[19]=19;    sieve[20]=20;    sieve[22]=22;    sieve[25]=25
    sieve[28]=28;    sieve[29]=29;    sieve[32]=32;    sieve[34]=34;    sieve[35]=35
    sieve[38]=38;    sieve[40]=40;    sieve[43]=43;    sieve[47]=47;    sieve[49]=49
    sieve[50]=50;    sieve[52]=52;    sieve[53]=53;    sieve[55]=55;    sieve[62]=62
    sieve[64]=64;    sieve[67]=67;    sieve[68]=68;    sieve[73]=73;    sieve[74]=74
    sieve[77]=77;    sieve[80]=80;    sieve[82]=82;    sieve[85]=85;    sieve[88]=88
    sieve[89]=89;    sieve[94]=94;    sieve[95]=95;    sieve[97]=97;    sieve[98]=98
    sieve[104]=104;  sieve[110]=110;  sieve[112]=112;  sieve[113]=113;  sieve[115]=115
    sieve[118]=118;  sieve[119]=119;  sieve[124]=124;  sieve[127]=127;  sieve[130]=130
    sieve[133]=133;  sieve[134]=134;  sieve[137]=137;  sieve[139]=139;  sieve[140]=140
    sieve[145]=145;  sieve[152]=152;  sieve[154]=154;  sieve[155]=155;  sieve[157]=157
    sieve[164]=164;  sieve[167]=167;  sieve[172]=172;  sieve[173]=173;  sieve[175]=175
    sieve[178]=178;  sieve[182]=182;  sieve[185]=185;  sieve[188]=188;  sieve[190]=190
    sieve[193]=193;  sieve[197]=197;  sieve[199]=199;  sieve[203]=203;  sieve[208]=208
    sieve[209]=209;  sieve[214]=214;  sieve[215]=215;  sieve[218]=218;  sieve[220]=220
    sieve[223]=223;  sieve[227]=227;  sieve[229]=229;  sieve[230]=230;  sieve[232]=232
    sieve[238]=238;  sieve[242]=242;  sieve[244]=244;  sieve[248]=248;  sieve[250]=250
    sieve[253]=253;  sieve[259]=259;  sieve[260]=260;  sieve[269]=269;  sieve[272]=272
    sieve[277]=277;  sieve[280]=280;  sieve[283]=283;  sieve[284]=284;  sieve[287]=287
    sieve[292]=292;  sieve[295]=295;  sieve[298]=298;  sieve[299]=299;  sieve[302]=302
    sieve[305]=305;  sieve[307]=307;  sieve[308]=308;  sieve[314]=314;  sieve[319]=319
    sieve[320]=320;  sieve[322]=322;  sieve[325]=325;  sieve[328]=328;  sieve[329]=329
    sieve[335]=335;  sieve[337]=337;  sieve[340]=340;  sieve[344]=344;  sieve[349]=349
    sieve[353]=353;  sieve[358]=358;  sieve[362]=362;  sieve[365]=365;  sieve[368]=368
    sieve[370]=370;  sieve[374]=374;  sieve[377]=377;  sieve[379]=379;  sieve[383]=383
    sieve[385]=385;  sieve[392]=392;  sieve[397]=397;  sieve[403]=403;  sieve[404]=404
    sieve[409]=409;  sieve[410]=410;  sieve[412]=412;  sieve[413]=413;  sieve[418]=418
    sieve[425]=425;  sieve[427]=427;  sieve[428]=428;  sieve[430]=430;  sieve[437]=437
    sieve[439]=439;  sieve[440]=440;  sieve[442]=442;  sieve[452]=452;  sieve[454]=454
    sieve[458]=458;  sieve[463]=463;  sieve[467]=467;  sieve[469]=469;  sieve[472]=472
    sieve[475]=475;  sieve[482]=482;  sieve[484]=484;  sieve[487]=487;  sieve[490]=490
    sieve[494]=494;  sieve[497]=497;  sieve[503]=503;  sieve[505]=505;  sieve[508]=508
    sieve[509]=509;  sieve[514]=514;  sieve[515]=515;  sieve[518]=518;  sieve[523]=523
    sieve[524]=524;  sieve[529]=529;  sieve[530]=530;  sieve[533]=533;  sieve[542]=542
    sieve[544]=544;  sieve[545]=545;  sieve[547]=547;  sieve[550]=550;  sieve[553]=553
    sieve[557]=557;  sieve[560]=560;  sieve[563]=563;  sieve[574]=574;  sieve[575]=575
    sieve[580]=580;  sieve[584]=584;  sieve[589]=589;  sieve[592]=592;  sieve[595]=595
    sieve[599]=599;  sieve[605]=605;  sieve[607]=607;  sieve[610]=610;  sieve[613]=613
    sieve[614]=614;  sieve[617]=617;  sieve[623]=623;  sieve[628]=628;  sieve[637]=637
    sieve[638]=638;  sieve[640]=640;  sieve[643]=643;  sieve[644]=644;  sieve[647]=647
    sieve[649]=649;  sieve[650]=650;  sieve[652]=652;  sieve[658]=658;  sieve[659]=659
    sieve[662]=662;  sieve[679]=679;  sieve[682]=682;  sieve[685]=685;  sieve[689]=689
    sieve[698]=698;  sieve[703]=703;  sieve[710]=710;  sieve[712]=712;  sieve[713]=713
    sieve[715]=715;  sieve[718]=718;  sieve[722]=722;  sieve[724]=724;  sieve[725]=725
    sieve[728]=728;  sieve[734]=734;  sieve[739]=739;  sieve[740]=740;  sieve[742]=742
    sieve[743]=743;  sieve[745]=745;  sieve[748]=748;  sieve[754]=754;  sieve[760]=760
    sieve[764]=764;  sieve[770]=770;  sieve[773]=773;  sieve[775]=775;  sieve[778]=778
    sieve[782]=782;  sieve[784]=784;  sieve[788]=788;  sieve[790]=790;  sieve[797]=797
    sieve[799]=799;  sieve[802]=802;  sieve[803]=803;  sieve[805]=805;  sieve[808]=808
    sieve[809]=809;  sieve[812]=812;  sieve[817]=817;  sieve[827]=827;  sieve[830]=830
    sieve[832]=832;  sieve[833]=833;  sieve[845]=845;  sieve[847]=847;  sieve[848]=848
    sieve[853]=853;  sieve[859]=859;  sieve[860]=860;  sieve[865]=865;  sieve[869]=869
    sieve[872]=872;  sieve[875]=875;  sieve[878]=878;  sieve[887]=887;  sieve[890]=890
    sieve[892]=892;  sieve[893]=893;  sieve[899]=899;  sieve[904]=904;  sieve[910]=910
    sieve[914]=914;  sieve[922]=922;  sieve[929]=929;  sieve[932]=932;  sieve[934]=934
    sieve[935]=935;  sieve[937]=937;  sieve[938]=938;  sieve[943]=943;  sieve[949]=949
    sieve[952]=952;  sieve[955]=955;  sieve[964]=964;  sieve[965]=965;  sieve[973]=973
    sieve[974]=974;  sieve[985]=985;  sieve[988]=988;  sieve[992]=992;  sieve[995]=995
    sieve[997]=997;  sieve[998]=998;  sieve[1000]=1000;sieve[1004]=1004;sieve[1007]=1007
    sieve[1012]=1012;sieve[1013]=1013;sieve[1018]=1018;sieve[1025]=1025;sieve[1030]=1030
    sieve[1033]=1033;sieve[1039]=1039;sieve[1040]=1040;sieve[1042]=1042;sieve[1043]=1043
    sieve[1048]=1048;sieve[1054]=1054;sieve[1055]=1055;sieve[1063]=1063;sieve[1064]=1064
    sieve[1067]=1067;sieve[1069]=1069;sieve[1070]=1070;sieve[1075]=1075;sieve[1079]=1079
    sieve[1088]=1088;sieve[1100]=1100;sieve[1102]=1102;sieve[1105]=1105;sieve[1109]=1109
    sieve[1117]=1117;sieve[1118]=1118;sieve[1120]=1120;sieve[1124]=1124;sieve[1132]=1132
    sieve[1133]=1133;sieve[1135]=1135;sieve[1139]=1139;sieve[1142]=1142;sieve[1145]=1145
    sieve[1147]=1147;sieve[1153]=1153
    for i in xrange(5, ((int(sqrt(val))-3)>>1)+1, 1):
        if not sieve[i]:  continue
        # p1=13*i, p2=17*i, p3=19*i -- p478=2297*i,p479=2309*i,p480=2311*i,k=2310*i
        #  j  i 13i 17i 19i 23i 29i 31i 37i..2291i 2293i 2297i 2309i 2311i 2310i
        # 13->5  83 109 122 148 187 200 239  14890 14903 14929 15007 15020 15015
        j=(i<<1)+3; j2=j<<1; j3=j2+j; j4=j2<<1; j5=j4+j; j6=j4+j2; j7=j4+j3
        p1=j6+i; p2=p1+j2; p3=p2+j; p4=p3+j2; p5=p4+j3; p6=p5+j; p7=p6+j3; p8=p7+j2   # 41
        p9=p8+j; p10=p9+j2; p11=p10+j3; p12=p11+j3; p13=p12+j; p14=p13+j3; p15=p14+j2 # 71
        p16=p15+j;  p17=p16+j3; p18=p17+j2; p19=p18+j3; p20=p19+j4; p21=p20+j2 # 101
        p22=p21+j;  p23=p22+j2; p24=p23+j;  p25=p24+j2; p26=p25+j7; p27=p26+j2 # 131
        p28=p27+j3; p29=p28+j;  p30=p29+j5; p31=p30+j;  p32=p31+j3; p33=p32+j3 # 163
        p34=p33+j2; p35=p34+j;  p36=p35+j2; p37=p36+j3; p38=p37+j;  p39=p38+j5 # 191
        p40=p39+j;  p41=p40+j2; p42=p41+j;  p43=p42+j6; p44=p43+j5; p45=p44+j  # 223
        p46=p45+j2; p47=p46+j;  p48=p47+j2; p49=p48+j3; p50=p49+j;  p51=p50+j3 # 247
        p52=p51+j2; p53=p52+j3; p54=p53+j3; p55=p54+j3; p56=p55+j;  p57=p56+j3 # 277
        p58=p57+j2; p59=p58+j;  p60=p59+j3; p61=p60+j2; p62=p61+j3; p63=p62+j4 # 307
        p64=p63+j2; p65=p64+j;  p66=p65+j2; p67=p66+j3; p68=p67+j4; p69=p68+j3 # 337
        p70=p69+j5; p71=p70+j;  p72=p71+j2; p73=p72+j3; p74=p73+j;  p75=p74+j3 # 367
        p76=p75+j3; p77=p76+j2; p78=p77+j;  p79=p78+j2; p80=p79+j3; p81=p80+j  # 391
        p82=p81+j3; p83=p82+j2; p84=p83+j;  p85=p84+j3; p86=p85+j5; p87=p86+j  # 421        
        p88=p87+j5; p89=p88+j;  p90=p89+j2; p91=p90+j;  p92=p91+j2; p93=p92+j3 # 449
        p94=p93+j4; p95=p94+j2; p96=p95+j;  p97=p96+j2; p98=p97+j6; p99=p98+j  # 481
        p100=p99+j3; p101=p100+j2;p102=p101+j;  p103=p102+j3; p104=p103+j2; p105=p104+j3 # 509
        p106=p105+j6;p107=p106+j; p108=p107+j2; p109=p108+j;  p110=p109+j2; p111=p110+j4 # 541
        p112=p111+j3;p113=p112+j2;p114=p113+j3; p115=p114+j;  p116=p115+j2; p117=p116+j3 # 569
        p118=p117+j; p119=p118+j3;p120=p119+j5; p121=p120+j;  p122=p121+j2; p123=p122+j3 # 599
        p124=p123+j; p125=p124+j3;p126=p125+j2; p127=p126+j;  p128=p127+j2; p129=p128+j  # 619
        p130=p129+j5;p131=p130+j; p132=p131+j5; p133=p132+j;  p134=p133+j2; p135=p134+j3 # 653
        p136=p135+j3;p137=p136+j; p138=p137+j3; p139=p138+j3; p140=p139+j2; p141=p140+j3 # 683
        p142=p141+j3;p143=p142+j; p144=p143+j3; p145=p144+j2; p146=p145+j;  p147=p146+j3 # 709
        p148=p147+j2;p149=p148+j3;p150=p149+j4; p151=p150+j2; p152=p151+j;  p153=p152+j3 # 739
        p154=p153+j2;p155=p154+j4;p156=p155+j3; p157=p156+j2; p158=p157+j3; p159=p158+j  # 769        
        p160=p159+j2;p161=p160+j3;p162=p161+j4; p163=p162+j3; p164=p163+j2; p165=p164+j  # 799
        p166=p165+j5;p167=p166+j; p168=p167+j3; p169=p168+j2; p170=p169+j;  p171=p170+j2 # 827
        p172=p171+j; p173=p172+j5;p174=p173+j;  p175=p174+j5; p176=p175+j;  p177=p176+j2 # 857
        p178=p177+j; p179=p178+j2;p180=p179+j4; p181=p180+j3; p182=p181+j2; p183=p182+j  # 883
        p184=p183+j2;p185=p184+j3;p186=p185+j3; p187=p186+j;  p188=p187+j3; p189=p188+j2 # 911
        p190=p189+j4;p191=p190+j2;p192=p191+j3; p193=p192+j4; p194=p193+j2; p195=p194+j  # 943
        p196=p195+j2;p197=p196+j; p198=p197+j2; p199=p198+j4; p200=p199+j3; p201=p200+j2 # 971
        p202=p201+j3;p203=p202+j3;p204=p203+j3; p205=p204+j;  p206=p205+j3; p207=p206+j3 # 1003
        p208=p207+j2;p209=p208+j; p210=p209+j2; p211=p210+j3; p212=p211+j;  p213=p212+j3 # 1027
        p214=p213+j2;p215=p214+j; p216=p215+j2; p217=p216+j;  p218=p217+j5; p219=p218+j  # 1051
        p220=p219+j5;p221=p220+j; p222=p221+j3; p223=p222+j2; p224=p223+j3; p225=p224+j  # 1081
        p226=p225+j3;p227=p226+j2;p228=p227+j;  p229=p228+j2; p230=p229+j3; p231=p230+j3 # 1109
        p232=p231+j4;p233=p232+j2;p234=p233+j;  p235=p234+j3; p236=p235+j5; p237=p236+j4 # 1147
        p238=p237+j2;p239=p238+j; p240=p239+j2; p241=p240+j;  p242=p241+j2; p243=p242+j4 # 1171
        p244=p243+j5;p245=p244+j3;p246=p245+j;  p247=p246+j2; p248=p247+j4; p249=p248+j3 # 1207
        p250=p249+j3;p251=p250+j2;p252=p251+j;  p253=p252+j2; p254=p253+j3; p255=p254+j  # 1231
        p256=p255+j3;p257=p256+j2;p258=p257+j3; p259=p258+j;  p260=p259+j5; p261=p260+j  # 1261
        p262=p261+j5;p263=p262+j; p264=p263+j2; p265=p264+j;  p266=p265+j2; p267=p266+j3 # 1289
        p268=p267+j; p269=p268+j3;p270=p269+j2; p271=p270+j;  p272=p271+j2; p273=p272+j3 # 1313
        p274=p273+j3;p275=p274+j; p276=p275+j3; p277=p276+j3; p278=p277+j3; p279=p278+j2 # 1343
        p280=p279+j3;p281=p280+j4;p282=p281+j2; p283=p282+j;  p284=p283+j2; p285=p284+j  # 1369
        p286=p285+j2;p287=p286+j4;p288=p287+j3; p289=p288+j2; p290=p289+j4; p291=p290+j2 # 1403
        p292=p291+j3;p293=p292+j; p294=p293+j3; p295=p294+j3; p296=p295+j2; p297=p296+j  # 1429
        p298=p297+j2;p299=p298+j3;p300=p299+j4; p301=p300+j2; p302=p301+j;  p303=p302+j2 # 1457
        p304=p303+j; p305=p304+j5;p306=p305+j;  p307=p306+j5; p308=p307+j;  p309=p308+j2 # 1487
        p310=p309+j; p311=p310+j2;p312=p311+j3; p313=p312+j;  p314=p313+j5; p315=p314+j  # 1513
        p316=p315+j2;p317=p316+j3;p318=p317+j4; p319=p318+j3; p320=p319+j2; p321=p320+j  # 1543
        p322=p321+j3;p323=p322+j2;p324=p323+j3; p325=p324+j4; p326=p325+j2; p327=p326+j3 # 1577
        p328=p327+j; p329=p328+j2;p330=p329+j4; p331=p330+j3; p332=p331+j2; p333=p332+j3 # 1607
        p334=p333+j; p335=p334+j2;p336=p335+j3; p337=p336+j;  p338=p337+j3; p339=p338+j3 # 1633
        p340=p339+j2;p341=p340+j3;p342=p341+j3; p343=p342+j;  p344=p343+j3; p345=p344+j3 # 1663
        p346=p345+j2;p347=p346+j; p348=p347+j5; p349=p348+j;  p350=p349+j5; p351=p350+j  # 1693
        p352=p351+j2;p353=p352+j; p354=p353+j2; p355=p354+j3; p356=p355+j;  p357=p356+j3 # 1717
        p358=p357+j2;p359=p358+j; p360=p359+j5; p361=p360+j3; p362=p361+j;  p363=p362+j3 # 1747
        p364=p363+j2;p365=p364+j; p366=p365+j3; p367=p366+j2; p368=p367+j3; p369=p368+j4 # 1777
        p370=p369+j2;p371=p370+j; p372=p371+j2; p373=p372+j;  p374=p373+j6; p375=p374+j3 # 1807
        p376=p375+j2;p377=p376+j3;p378=p377+j;  p379=p378+j2; p380=p379+j3; p381=p380+j  # 1831
        p382=p381+j6;p383=p382+j2;p384=p383+j;  p385=p384+j2; p386=p385+j4; p387=p386+j3 # 1867
        p388=p387+j2;p389=p388+j; p390=p389+j2; p391=p390+j;  p392=p391+j5; p393=p392+j  # 1891
        p394=p393+j5;p395=p394+j3;p396=p395+j;  p397=p396+j2; p398=p397+j3; p399=p398+j  # 1921
        p400=p399+j3;p401=p400+j2;p402=p401+j;  p403=p402+j2; p404=p403+j3; p405=p404+j3 # 1949
        p406=p405+j; p407=p406+j3;p408=p407+j2; p409=p408+j;  p410=p409+j5; p411=p410+j3 # 1979
        p412=p411+j4;p413=p412+j3;p414=p413+j2; p415=p414+j;  p416=p415+j2; p417=p416+j4 # 2011
        p418=p417+j3;p419=p418+j2;p420=p419+j3; p421=p420+j;  p422=p421+j2; p423=p422+j3 # 2039
        p424=p423+j; p425=p424+j3;p426=p425+j3; p427=p426+j3; p428=p427+j2; p429=p428+j3 # 2069
        p430=p429+j; p431=p430+j3;p432=p431+j2; p433=p432+j;  p434=p433+j2; p435=p434+j  # 2089
        p436=p435+j5;p437=p436+j6;p438=p437+j;  p439=p438+j2; p440=p439+j ; p441=p440+j5 # 2129
        p442=p441+j; p443=p442+j3;p444=p443+j2; p445=p444+j;  p446=p445+j2; p447=p446+j3 # 2153        
        p448=p447+j3;p449=p448+j; p450=p449+j5; p451=p450+j;  p452=p451+j3; p453=p452+j2 # 2183
        p454=p453+j7;p455=p454+j2;p456=p455+j;  p457=p456+j2; p458=p457+j;  p459=p458+j2 # 2213
        p460=p459+j4;p461=p460+j3;p462=p461+j2; p463=p462+j3; p464=p463+j;  p465=p464+j2 # 2243
        p466=p465+j3;p467=p466+j; p468=p467+j3; p469=p468+j3; p470=p469+j2; p471=p470+j  # 2269
        p472=p471+j2;p473=p472+j3;p474=p473+j;  p475=p474+j3; p476=p475+j2; p477=p476+j  # 2293
        p478=p477+j2;p479=p478+j6;p480=p479+j;  k = p480-i
        while p480 < lndx:
           sieve[p1] = sieve[p2] = sieve[p3] = sieve[p4] = sieve[p5] = sieve[p6]=  \
           sieve[p7] = sieve[p8] = sieve[p9] = sieve[p10]= sieve[p11]= sieve[p12]= \
           sieve[p13]= sieve[p14]= sieve[p15]= sieve[p16]= sieve[p17]= sieve[p18]= \
           sieve[p19]= sieve[p20]= sieve[p21]= sieve[p22]= sieve[p23]= sieve[p24]= \
           sieve[p25]= sieve[p26]= sieve[p27]= sieve[p28]= sieve[p29]= sieve[p30]= \
           sieve[p31]= sieve[p32]= sieve[p33]= sieve[p34]= sieve[p35]= sieve[p36]= \
           sieve[p37]= sieve[p38]= sieve[p39]= sieve[p40]= sieve[p41]= sieve[p42]= \
           sieve[p43]= sieve[p44]= sieve[p45]= sieve[p46]= sieve[p47]= sieve[p48]= \
           sieve[p49]= sieve[p50]= sieve[p51]= sieve[p52]= sieve[p53]= sieve[p54]= \
           sieve[p55]= sieve[p56]= sieve[p57]= sieve[p58]= sieve[p59]= sieve[p60]= \
           sieve[p61]= sieve[p62]= sieve[p63]= sieve[p64]= sieve[p65]= sieve[p66]= \
           sieve[p67]= sieve[p68]= sieve[p69]= sieve[p70]= sieve[p71]= sieve[p72]= \
           sieve[p73]= sieve[p74]= sieve[p75]= sieve[p76]= sieve[p77]= sieve[p78]= \
           sieve[p79]= sieve[p80]= sieve[p81]= sieve[p82]= sieve[p83]= sieve[p84]= \
           sieve[p85]= sieve[p86]= sieve[p87]= sieve[p88]= sieve[p89]= sieve[p90]= \
           sieve[p91]= sieve[p92]= sieve[p93]= sieve[p94]= sieve[p95]= sieve[p96]= \
           sieve[p97]= sieve[p98]= sieve[p99]= sieve[p100]=sieve[p101]=sieve[p102]= \
           sieve[p103]=sieve[p104]=sieve[p105]=sieve[p106]=sieve[p107]=sieve[p108]= \
           sieve[p109]=sieve[p110]=sieve[p111]=sieve[p112]=sieve[p113]=sieve[p114]= \
           sieve[p115]=sieve[p116]=sieve[p117]=sieve[p118]=sieve[p119]=sieve[p120]= \
           sieve[p121]=sieve[p122]=sieve[p123]=sieve[p124]=sieve[p125]=sieve[p126]= \
           sieve[p127]=sieve[p128]=sieve[p129]=sieve[p130]=sieve[p131]=sieve[p132]= \
           sieve[p133]=sieve[p134]=sieve[p135]=sieve[p136]=sieve[p137]=sieve[p138]= \
           sieve[p139]=sieve[p140]=sieve[p141]=sieve[p142]=sieve[p143]=sieve[p144]= \
           sieve[p145]=sieve[p146]=sieve[p147]=sieve[p148]=sieve[p149]=sieve[p150]= \
           sieve[p151]=sieve[p152]=sieve[p153]=sieve[p154]=sieve[p155]=sieve[p156]= \
           sieve[p157]=sieve[p158]=sieve[p159]=sieve[p160]=sieve[p161]=sieve[p162]= \
           sieve[p163]=sieve[p164]=sieve[p165]=sieve[p166]=sieve[p167]=sieve[p168]= \
           sieve[p169]=sieve[p170]=sieve[p171]=sieve[p172]=sieve[p173]=sieve[p174]= \
           sieve[p175]=sieve[p176]=sieve[p177]=sieve[p178]=sieve[p179]=sieve[p180]= \
           sieve[p181]=sieve[p182]=sieve[p183]=sieve[p184]=sieve[p185]=sieve[p186]= \
           sieve[p187]=sieve[p188]=sieve[p189]=sieve[p190]=sieve[p191]=sieve[p192]= \
           sieve[p193]=sieve[p194]=sieve[p195]=sieve[p196]=sieve[p197]=sieve[p198]= \
           sieve[p199]=sieve[p200]=sieve[p201]=sieve[p202]=sieve[p203]=sieve[p204]= \
           sieve[p205]=sieve[p206]=sieve[p207]=sieve[p208]=sieve[p209]=sieve[p210]= \
           sieve[p211]=sieve[p212]=sieve[p213]=sieve[p214]=sieve[p215]=sieve[p216]= \
           sieve[p217]=sieve[p218]=sieve[p219]=sieve[p220]=sieve[p221]=sieve[p222]= \
           sieve[p223]=sieve[p224]=sieve[p225]=sieve[p226]=sieve[p227]=sieve[p228]= \
           sieve[p229]=sieve[p230]=sieve[p231]=sieve[p232]=sieve[p233]=sieve[p234]= \
           sieve[p235]=sieve[p236]=sieve[p237]=sieve[p238]=sieve[p239]=sieve[p240]= \
           sieve[p241]=sieve[p242]=sieve[p243]=sieve[p244]=sieve[p245]=sieve[p246]= \
           sieve[p247]=sieve[p248]=sieve[p249]=sieve[p250]=sieve[p251]=sieve[p252]= \
           sieve[p253]=sieve[p254]=sieve[p255]=sieve[p256]=sieve[p257]=sieve[p258]= \
           sieve[p259]=sieve[p260]=sieve[p261]=sieve[p262]=sieve[p263]=sieve[p264]= \
           sieve[p265]=sieve[p266]=sieve[p267]=sieve[p268]=sieve[p269]=sieve[p270]= \
           sieve[p271]=sieve[p272]=sieve[p273]=sieve[p274]=sieve[p275]=sieve[p276]= \
           sieve[p277]=sieve[p278]=sieve[p279]=sieve[p280]=sieve[p281]=sieve[p282]= \
           sieve[p283]=sieve[p284]=sieve[p285]=sieve[p286]=sieve[p287]=sieve[p288]= \
           sieve[p289]=sieve[p290]=sieve[p291]=sieve[p292]=sieve[p293]=sieve[p294]= \
           sieve[p295]=sieve[p296]=sieve[p297]=sieve[p298]=sieve[p299]=sieve[p300]= \
           sieve[p301]=sieve[p302]=sieve[p303]=sieve[p304]=sieve[p305]=sieve[p306]= \
           sieve[p307]=sieve[p308]=sieve[p309]=sieve[p310]=sieve[p311]=sieve[p312]= \
           sieve[p313]=sieve[p314]=sieve[p315]=sieve[p316]=sieve[p317]=sieve[p318]= \
           sieve[p319]=sieve[p320]=sieve[p321]=sieve[p322]=sieve[p323]=sieve[p324]= \
           sieve[p325]=sieve[p326]=sieve[p327]=sieve[p328]=sieve[p329]=sieve[p330]= \
           sieve[p331]=sieve[p332]=sieve[p333]=sieve[p334]=sieve[p335]=sieve[p336]= \
           sieve[p337]=sieve[p338]=sieve[p339]=sieve[p340]=sieve[p341]=sieve[p342]= \
           sieve[p343]=sieve[p344]=sieve[p345]=sieve[p346]=sieve[p347]=sieve[p348]= \
           sieve[p349]=sieve[p350]=sieve[p351]=sieve[p352]=sieve[p353]=sieve[p354]= \
           sieve[p355]=sieve[p356]=sieve[p357]=sieve[p358]=sieve[p359]=sieve[p360]= \
           sieve[p361]=sieve[p362]=sieve[p363]=sieve[p364]=sieve[p365]=sieve[p366]= \
           sieve[p367]=sieve[p368]=sieve[p369]=sieve[p370]=sieve[p371]=sieve[p372]= \
           sieve[p373]=sieve[p374]=sieve[p375]=sieve[p376]=sieve[p377]=sieve[p378]= \
           sieve[p379]=sieve[p380]=sieve[p381]=sieve[p382]=sieve[p383]=sieve[p384]= \
           sieve[p385]=sieve[p386]=sieve[p387]=sieve[p388]=sieve[p389]=sieve[p390]= \
           sieve[p391]=sieve[p392]=sieve[p393]=sieve[p394]=sieve[p395]=sieve[p396]= \
           sieve[p397]=sieve[p398]=sieve[p399]=sieve[p400]=sieve[p401]=sieve[p402]= \
           sieve[p403]=sieve[p404]=sieve[p405]=sieve[p406]=sieve[p407]=sieve[p408]= \
           sieve[p409]=sieve[p410]=sieve[p411]=sieve[p412]=sieve[p413]=sieve[p414]= \
           sieve[p415]=sieve[p416]=sieve[p417]=sieve[p418]=sieve[p419]=sieve[p420]= \
           sieve[p421]=sieve[p422]=sieve[p423]=sieve[p424]=sieve[p425]=sieve[p426]= \
           sieve[p427]=sieve[p428]=sieve[p429]=sieve[p430]=sieve[p431]=sieve[p432]= \
           sieve[p433]=sieve[p434]=sieve[p435]=sieve[p436]=sieve[p437]=sieve[p438]= \
           sieve[p439]=sieve[p440]=sieve[p441]=sieve[p442]=sieve[p443]=sieve[p444]= \
           sieve[p445]=sieve[p446]=sieve[p447]=sieve[p448]=sieve[p449]=sieve[p450]= \
           sieve[p451]=sieve[p452]=sieve[p453]=sieve[p454]=sieve[p455]=sieve[p456]= \
           sieve[p457]=sieve[p458]=sieve[p459]=sieve[p460]=sieve[p461]=sieve[p462]= \
           sieve[p463]=sieve[p464]=sieve[p465]=sieve[p466]=sieve[p467]=sieve[p468]= \
           sieve[p469]=sieve[p470]=sieve[p471]=sieve[p472]=sieve[p473]=sieve[p474]= \
           sieve[p475]=sieve[p476]=sieve[p477]=sieve[p478]=sieve[p479]=sieve[p480]= False
           p1 += k;  p2 += k;  p3 += k;  p4 += k;  p5 += k;  p6 += k;  p7 += k;  p8 += k
           p9 += k;  p10 +=k;  p11 +=k;  p12 +=k;  p13 +=k;  p14 +=k;  p15 +=k;  p16 +=k
           p17 +=k;  p18 +=k;  p19 +=k;  p20 +=k;  p21 +=k;  p22 +=k;  p23 +=k;  p24 +=k
           p25 +=k;  p26 +=k;  p27 +=k;  p28 +=k;  p29 +=k;  p30 +=k;  p31 +=k;  p32 +=k
           p33 +=k;  p34 +=k;  p35 +=k;  p36 +=k;  p37 +=k;  p38 +=k;  p39 +=k;  p40 +=k
           p41 +=k;  p42 +=k;  p43 +=k;  p44 +=k;  p45 +=k;  p46 +=k;  p47 +=k;  p48 +=k
           p49 +=k;  p50 +=k;  p51 +=k;  p52 +=k;  p53 +=k;  p54 +=k;  p55 +=k;  p56 +=k
           p57 +=k;  p58 +=k;  p59 +=k;  p60 +=k;  p61 +=k;  p62 +=k;  p63 +=k;  p64 +=k
           p65 +=k;  p66 +=k;  p67 +=k;  p68 +=k;  p69 +=k;  p70 +=k;  p71 +=k;  p72 +=k
           p73 +=k;  p74 +=k;  p75 +=k;  p76 +=k;  p77 +=k;  p78 +=k;  p79 +=k;  p80 +=k
           p81 +=k;  p82 +=k;  p83 +=k;  p84 +=k;  p85 +=k;  p86 +=k;  p87 +=k;  p88 +=k
           p89 +=k;  p90 +=k;  p91 +=k;  p92 +=k;  p93 +=k;  p94 +=k;  p95 +=k;  p96 +=k
           p97 +=k;  p98 +=k;  p99 +=k; p100 +=k; p101 +=k; p102 +=k; p103 +=k; p104 +=k
           p105 +=k;p106 +=k; p107 +=k; p108 +=k; p109 +=k; p110 +=k; p111 +=k; p112 +=k
           p113 +=k;p114 +=k; p115 +=k; p116 +=k; p117 +=k; p118 +=k; p119 +=k; p120 +=k
           p121 +=k;p122 +=k; p123 +=k; p124 +=k; p125 +=k; p126 +=k; p127 +=k; p128 +=k
           p129 +=k;p130 +=k; p131 +=k; p132 +=k; p133 +=k; p134 +=k; p135 +=k; p136 +=k
           p137 +=k;p138 +=k; p139 +=k; p140 +=k; p141 +=k; p142 +=k; p143 +=k; p144 +=k
           p145 +=k;p146 +=k; p147 +=k; p148 +=k; p149 +=k; p150 +=k; p151 +=k; p152 +=k
           p153 +=k;p154 +=k; p155 +=k; p156 +=k; p157 +=k; p158 +=k; p159 +=k; p160 +=k
           p161 +=k;p162 +=k; p163 +=k; p164 +=k; p165 +=k; p166 +=k; p167 +=k; p168 +=k
           p169 +=k;p170 +=k; p171 +=k; p172 +=k; p173 +=k; p174 +=k; p175 +=k; p176 +=k
           p177 +=k;p178 +=k; p179 +=k; p180 +=k; p181 +=k; p182 +=k; p183 +=k; p184 +=k
           p185 +=k;p186 +=k; p187 +=k; p188 +=k; p189 +=k; p190 +=k; p191 +=k; p192 +=k
           p193 +=k;p194 +=k; p195 +=k; p196 +=k; p197 +=k; p198 +=k; p199 +=k; p200 +=k
           p201 +=k;p202 +=k; p203 +=k; p204 +=k; p205 +=k; p206 +=k; p207 +=k; p208 +=k
           p209 +=k;p210 +=k; p211 +=k; p212 +=k; p213 +=k; p214 +=k; p215 +=k; p216 +=k
           p217 +=k;p218 +=k; p219 +=k; p220 +=k; p221 +=k; p222 +=k; p223 +=k; p224 +=k
           p225 +=k;p226 +=k; p227 +=k; p228 +=k; p229 +=k; p230 +=k; p231 +=k; p232 +=k
           p233 +=k;p234 +=k; p235 +=k; p236 +=k; p237 +=k; p238 +=k; p239 +=k; p240 +=k
           p241 +=k;p242 +=k; p243 +=k; p244 +=k; p245 +=k; p246 +=k; p247 +=k; p248 +=k
           p249 +=k;p250 +=k; p251 +=k; p252 +=k; p253 +=k; p254 +=k; p255 +=k; p256 +=k
           p257 +=k;p258 +=k; p259 +=k; p260 +=k; p261 +=k; p262 +=k; p263 +=k; p264 +=k
           p265 +=k;p266 +=k; p267 +=k; p268 +=k; p269 +=k; p270 +=k; p271 +=k; p272 +=k
           p273 +=k;p274 +=k; p275 +=k; p276 +=k; p277 +=k; p278 +=k; p279 +=k; p280 +=k
           p281 +=k;p282 +=k; p283 +=k; p284 +=k; p285 +=k; p286 +=k; p287 +=k; p288 +=k
           p289 +=k;p290 +=k; p291 +=k; p292 +=k; p293 +=k; p294 +=k; p295 +=k; p296 +=k
           p297 +=k;p298 +=k; p299 +=k; p300 +=k; p301 +=k; p302 +=k; p303 +=k; p304 +=k
           p305 +=k;p306 +=k; p307 +=k; p308 +=k; p309 +=k; p310 +=k; p311 +=k; p312 +=k
           p313 +=k;p314 +=k; p315 +=k; p316 +=k; p317 +=k; p318 +=k; p319 +=k; p320 +=k
           p321 +=k;p322 +=k; p323 +=k; p324 +=k; p325 +=k; p326 +=k; p327 +=k; p328 +=k
           p329 +=k;p330 +=k; p331 +=k; p332 +=k; p333 +=k; p334 +=k; p335 +=k; p336 +=k
           p337 +=k;p338 +=k; p339 +=k; p340 +=k; p341 +=k; p342 +=k; p343 +=k; p344 +=k
           p345 +=k;p346 +=k; p347 +=k; p348 +=k; p349 +=k; p350 +=k; p351 +=k; p352 +=k
           p353 +=k;p354 +=k; p355 +=k; p356 +=k; p357 +=k; p358 +=k; p359 +=k; p360 +=k
           p361 +=k;p362 +=k; p363 +=k; p364 +=k; p365 +=k; p366 +=k; p367 +=k; p368 +=k
           p369 +=k;p370 +=k; p371 +=k; p372 +=k; p373 +=k; p374 +=k; p375 +=k; p376 +=k
           p377 +=k;p378 +=k; p379 +=k; p380 +=k; p381 +=k; p382 +=k; p383 +=k; p384 +=k
           p385 +=k;p386 +=k; p387 +=k; p388 +=k; p389 +=k; p390 +=k; p391 +=k; p392 +=k
           p393 +=k;p394 +=k; p395 +=k; p396 +=k; p397 +=k; p398 +=k; p399 +=k; p400 +=k
           p401 +=k;p402 +=k; p403 +=k; p404 +=k; p405 +=k; p406 +=k; p407 +=k; p408 +=k
           p409 +=k;p410 +=k; p411 +=k; p412 +=k; p413 +=k; p414 +=k; p415 +=k; p416 +=k
           p417 +=k;p418 +=k; p419 +=k; p420 +=k; p421 +=k; p422 +=k; p423 +=k; p424 +=k
           p425 +=k;p426 +=k; p427 +=k; p428 +=k; p429 +=k; p430 +=k; p431 +=k; p432 +=k
           p433 +=k;p434 +=k; p435 +=k; p436 +=k; p437 +=k; p438 +=k; p439 +=k; p440 +=k
           p441 +=k;p442 +=k; p443 +=k; p444 +=k; p445 +=k; p446 +=k; p447 +=k; p448 +=k
           p449 +=k;p450 +=k; p451 +=k; p452 +=k; p453 +=k; p454 +=k; p455 +=k; p456 +=k
           p457 +=k;p458 +=k; p459 +=k; p460 +=k; p461 +=k; p462 +=k; p463 +=k; p464 +=k
           p465 +=k;p466 +=k; p467 +=k; p468 +=k; p469 +=k; p470 +=k; p471 +=k; p472 +=k
           p473 +=k;p474 +=k; p475 +=k; p476 +=k; p477 +=k; p478 +=k; p479 +=k; p480 +=k
        if p479 < lndx: sieve[p479] = False
        if p478 < lndx: sieve[p478] = False
        if p477 < lndx: sieve[p477] = False
        if p476 < lndx: sieve[p476] = False
        if p475 < lndx: sieve[p475] = False
        if p474 < lndx: sieve[p474] = False
        if p473 < lndx: sieve[p473] = False
        if p472 < lndx: sieve[p472] = False
        if p471 < lndx: sieve[p471] = False
        if p470 < lndx: sieve[p470] = False
        if p469 < lndx: sieve[p469] = False
        if p468 < lndx: sieve[p468] = False
        if p467 < lndx: sieve[p467] = False
        if p466 < lndx: sieve[p466] = False
        if p465 < lndx: sieve[p465] = False
        if p464 < lndx: sieve[p464] = False
        if p463 < lndx: sieve[p463] = False
        if p462 < lndx: sieve[p462] = False
        if p461 < lndx: sieve[p461] = False
        if p460 < lndx: sieve[p460] = False
        if p459 < lndx: sieve[p459] = False
        if p458 < lndx: sieve[p458] = False
        if p457 < lndx: sieve[p457] = False
        if p456 < lndx: sieve[p456] = False
        if p455 < lndx: sieve[p455] = False
        if p454 < lndx: sieve[p454] = False
        if p453 < lndx: sieve[p453] = False
        if p452 < lndx: sieve[p452] = False
        if p451 < lndx: sieve[p451] = False
        if p450 < lndx: sieve[p450] = False
        if p449 < lndx: sieve[p449] = False
        if p448 < lndx: sieve[p448] = False
        if p447 < lndx: sieve[p447] = False
        if p446 < lndx: sieve[p446] = False
        if p445 < lndx: sieve[p445] = False
        if p444 < lndx: sieve[p444] = False
        if p443 < lndx: sieve[p443] = False
        if p442 < lndx: sieve[p442] = False
        if p441 < lndx: sieve[p441] = False
        if p440 < lndx: sieve[p440] = False
        if p439 < lndx: sieve[p439] = False
        if p438 < lndx: sieve[p438] = False
        if p437 < lndx: sieve[p437] = False
        if p436 < lndx: sieve[p436] = False
        if p435 < lndx: sieve[p435] = False
        if p434 < lndx: sieve[p434] = False
        if p433 < lndx: sieve[p433] = False
        if p432 < lndx: sieve[p432] = False
        if p431 < lndx: sieve[p431] = False
        if p430 < lndx: sieve[p430] = False
        if p429 < lndx: sieve[p429] = False
        if p428 < lndx: sieve[p428] = False
        if p427 < lndx: sieve[p427] = False
        if p426 < lndx: sieve[p426] = False
        if p425 < lndx: sieve[p425] = False
        if p424 < lndx: sieve[p424] = False
        if p423 < lndx: sieve[p423] = False
        if p422 < lndx: sieve[p422] = False
        if p421 < lndx: sieve[p421] = False
        if p420 < lndx: sieve[p420] = False
        if p419 < lndx: sieve[p419] = False
        if p418 < lndx: sieve[p418] = False
        if p417 < lndx: sieve[p417] = False
        if p416 < lndx: sieve[p416] = False
        if p415 < lndx: sieve[p415] = False
        if p414 < lndx: sieve[p414] = False
        if p413 < lndx: sieve[p413] = False
        if p412 < lndx: sieve[p412] = False
        if p411 < lndx: sieve[p411] = False
        if p410 < lndx: sieve[p410] = False
        if p409 < lndx: sieve[p409] = False
        if p408 < lndx: sieve[p408] = False
        if p407 < lndx: sieve[p407] = False
        if p406 < lndx: sieve[p406] = False
        if p405 < lndx: sieve[p405] = False
        if p404 < lndx: sieve[p404] = False
        if p403 < lndx: sieve[p403] = False
        if p402 < lndx: sieve[p402] = False
        if p401 < lndx: sieve[p401] = False
        if p400 < lndx: sieve[p400] = False
        if p399 < lndx: sieve[p399] = False
        if p398 < lndx: sieve[p398] = False
        if p397 < lndx: sieve[p397] = False
        if p396 < lndx: sieve[p396] = False
        if p395 < lndx: sieve[p395] = False
        if p394 < lndx: sieve[p394] = False
        if p393 < lndx: sieve[p393] = False
        if p392 < lndx: sieve[p392] = False
        if p391 < lndx: sieve[p391] = False
        if p390 < lndx: sieve[p390] = False
        if p389 < lndx: sieve[p389] = False
        if p388 < lndx: sieve[p388] = False
        if p387 < lndx: sieve[p387] = False
        if p386 < lndx: sieve[p386] = False
        if p385 < lndx: sieve[p385] = False
        if p384 < lndx: sieve[p384] = False
        if p383 < lndx: sieve[p383] = False
        if p382 < lndx: sieve[p382] = False
        if p381 < lndx: sieve[p381] = False
        if p380 < lndx: sieve[p380] = False
        if p379 < lndx: sieve[p379] = False
        if p378 < lndx: sieve[p378] = False
        if p377 < lndx: sieve[p377] = False
        if p376 < lndx: sieve[p376] = False
        if p375 < lndx: sieve[p375] = False
        if p374 < lndx: sieve[p374] = False
        if p373 < lndx: sieve[p373] = False
        if p372 < lndx: sieve[p372] = False
        if p371 < lndx: sieve[p371] = False
        if p370 < lndx: sieve[p370] = False
        if p369 < lndx: sieve[p369] = False
        if p368 < lndx: sieve[p368] = False
        if p367 < lndx: sieve[p367] = False
        if p366 < lndx: sieve[p366] = False
        if p365 < lndx: sieve[p365] = False
        if p364 < lndx: sieve[p364] = False
        if p363 < lndx: sieve[p363] = False
        if p362 < lndx: sieve[p362] = False
        if p361 < lndx: sieve[p361] = False
        if p360 < lndx: sieve[p360] = False
        if p359 < lndx: sieve[p359] = False
        if p358 < lndx: sieve[p358] = False
        if p357 < lndx: sieve[p357] = False
        if p356 < lndx: sieve[p356] = False
        if p355 < lndx: sieve[p355] = False
        if p354 < lndx: sieve[p354] = False
        if p353 < lndx: sieve[p353] = False
        if p352 < lndx: sieve[p352] = False
        if p351 < lndx: sieve[p351] = False
        if p350 < lndx: sieve[p350] = False
        if p349 < lndx: sieve[p349] = False
        if p348 < lndx: sieve[p348] = False
        if p347 < lndx: sieve[p347] = False
        if p346 < lndx: sieve[p346] = False
        if p345 < lndx: sieve[p345] = False
        if p344 < lndx: sieve[p344] = False
        if p343 < lndx: sieve[p343] = False
        if p342 < lndx: sieve[p342] = False
        if p341 < lndx: sieve[p341] = False
        if p340 < lndx: sieve[p340] = False
        if p339 < lndx: sieve[p339] = False
        if p338 < lndx: sieve[p338] = False
        if p337 < lndx: sieve[p337] = False
        if p336 < lndx: sieve[p336] = False
        if p335 < lndx: sieve[p335] = False
        if p334 < lndx: sieve[p334] = False
        if p333 < lndx: sieve[p333] = False
        if p332 < lndx: sieve[p332] = False
        if p331 < lndx: sieve[p331] = False
        if p330 < lndx: sieve[p330] = False
        if p329 < lndx: sieve[p329] = False
        if p328 < lndx: sieve[p328] = False
        if p327 < lndx: sieve[p327] = False
        if p326 < lndx: sieve[p326] = False
        if p325 < lndx: sieve[p325] = False
        if p324 < lndx: sieve[p324] = False
        if p323 < lndx: sieve[p323] = False
        if p322 < lndx: sieve[p322] = False
        if p321 < lndx: sieve[p321] = False
        if p320 < lndx: sieve[p320] = False
        if p319 < lndx: sieve[p319] = False
        if p318 < lndx: sieve[p318] = False
        if p317 < lndx: sieve[p317] = False
        if p316 < lndx: sieve[p316] = False
        if p315 < lndx: sieve[p315] = False
        if p314 < lndx: sieve[p314] = False
        if p313 < lndx: sieve[p313] = False
        if p312 < lndx: sieve[p312] = False
        if p311 < lndx: sieve[p311] = False
        if p310 < lndx: sieve[p310] = False
        if p309 < lndx: sieve[p309] = False
        if p308 < lndx: sieve[p308] = False
        if p307 < lndx: sieve[p307] = False
        if p306 < lndx: sieve[p306] = False
        if p305 < lndx: sieve[p305] = False
        if p304 < lndx: sieve[p304] = False
        if p303 < lndx: sieve[p303] = False
        if p302 < lndx: sieve[p302] = False
        if p301 < lndx: sieve[p301] = False
        if p300 < lndx: sieve[p300] = False
        if p299 < lndx: sieve[p299] = False
        if p298 < lndx: sieve[p298] = False
        if p297 < lndx: sieve[p297] = False
        if p296 < lndx: sieve[p296] = False
        if p295 < lndx: sieve[p295] = False
        if p294 < lndx: sieve[p294] = False
        if p293 < lndx: sieve[p293] = False
        if p292 < lndx: sieve[p292] = False
        if p291 < lndx: sieve[p291] = False
        if p290 < lndx: sieve[p290] = False
        if p289 < lndx: sieve[p289] = False
        if p288 < lndx: sieve[p288] = False
        if p287 < lndx: sieve[p287] = False
        if p286 < lndx: sieve[p286] = False
        if p285 < lndx: sieve[p285] = False
        if p284 < lndx: sieve[p284] = False
        if p283 < lndx: sieve[p283] = False
        if p282 < lndx: sieve[p282] = False
        if p281 < lndx: sieve[p281] = False
        if p280 < lndx: sieve[p280] = False
        if p279 < lndx: sieve[p279] = False
        if p278 < lndx: sieve[p278] = False
        if p277 < lndx: sieve[p277] = False
        if p276 < lndx: sieve[p276] = False
        if p275 < lndx: sieve[p275] = False
        if p274 < lndx: sieve[p274] = False
        if p273 < lndx: sieve[p273] = False
        if p272 < lndx: sieve[p272] = False
        if p271 < lndx: sieve[p271] = False
        if p270 < lndx: sieve[p270] = False
        if p269 < lndx: sieve[p269] = False
        if p268 < lndx: sieve[p268] = False
        if p267 < lndx: sieve[p267] = False
        if p266 < lndx: sieve[p266] = False
        if p265 < lndx: sieve[p265] = False
        if p264 < lndx: sieve[p264] = False
        if p263 < lndx: sieve[p263] = False
        if p262 < lndx: sieve[p262] = False
        if p261 < lndx: sieve[p261] = False
        if p260 < lndx: sieve[p260] = False
        if p259 < lndx: sieve[p259] = False
        if p258 < lndx: sieve[p258] = False
        if p257 < lndx: sieve[p257] = False
        if p256 < lndx: sieve[p256] = False
        if p255 < lndx: sieve[p255] = False
        if p254 < lndx: sieve[p254] = False
        if p253 < lndx: sieve[p253] = False
        if p252 < lndx: sieve[p252] = False
        if p251 < lndx: sieve[p251] = False
        if p250 < lndx: sieve[p250] = False
        if p249 < lndx: sieve[p249] = False
        if p248 < lndx: sieve[p248] = False
        if p247 < lndx: sieve[p247] = False
        if p246 < lndx: sieve[p246] = False
        if p245 < lndx: sieve[p245] = False
        if p244 < lndx: sieve[p244] = False
        if p243 < lndx: sieve[p243] = False
        if p242 < lndx: sieve[p242] = False
        if p241 < lndx: sieve[p241] = False
        if p240 < lndx: sieve[p240] = False
        if p239 < lndx: sieve[p239] = False
        if p238 < lndx: sieve[p238] = False
        if p237 < lndx: sieve[p237] = False
        if p236 < lndx: sieve[p236] = False
        if p235 < lndx: sieve[p235] = False
        if p234 < lndx: sieve[p234] = False
        if p233 < lndx: sieve[p233] = False
        if p232 < lndx: sieve[p232] = False
        if p231 < lndx: sieve[p231] = False
        if p230 < lndx: sieve[p230] = False
        if p229 < lndx: sieve[p229] = False
        if p228 < lndx: sieve[p228] = False
        if p227 < lndx: sieve[p227] = False
        if p226 < lndx: sieve[p226] = False
        if p225 < lndx: sieve[p225] = False
        if p224 < lndx: sieve[p224] = False
        if p223 < lndx: sieve[p223] = False
        if p222 < lndx: sieve[p222] = False
        if p221 < lndx: sieve[p221] = False
        if p220 < lndx: sieve[p220] = False
        if p219 < lndx: sieve[p219] = False
        if p218 < lndx: sieve[p218] = False
        if p217 < lndx: sieve[p217] = False
        if p216 < lndx: sieve[p216] = False
        if p215 < lndx: sieve[p215] = False
        if p214 < lndx: sieve[p214] = False
        if p213 < lndx: sieve[p213] = False
        if p212 < lndx: sieve[p212] = False
        if p211 < lndx: sieve[p211] = False
        if p210 < lndx: sieve[p210] = False
        if p209 < lndx: sieve[p209] = False
        if p208 < lndx: sieve[p208] = False
        if p207 < lndx: sieve[p207] = False
        if p206 < lndx: sieve[p206] = False
        if p205 < lndx: sieve[p205] = False
        if p204 < lndx: sieve[p204] = False
        if p203 < lndx: sieve[p203] = False
        if p202 < lndx: sieve[p202] = False
        if p201 < lndx: sieve[p201] = False
        if p200 < lndx: sieve[p200] = False
        if p199 < lndx: sieve[p199] = False
        if p198 < lndx: sieve[p198] = False
        if p197 < lndx: sieve[p197] = False
        if p196 < lndx: sieve[p196] = False
        if p195 < lndx: sieve[p195] = False
        if p194 < lndx: sieve[p194] = False
        if p193 < lndx: sieve[p193] = False
        if p192 < lndx: sieve[p192] = False
        if p191 < lndx: sieve[p191] = False
        if p190 < lndx: sieve[p190] = False
        if p189 < lndx: sieve[p189] = False
        if p188 < lndx: sieve[p188] = False
        if p187 < lndx: sieve[p187] = False
        if p186 < lndx: sieve[p186] = False
        if p185 < lndx: sieve[p185] = False
        if p184 < lndx: sieve[p184] = False
        if p183 < lndx: sieve[p183] = False
        if p182 < lndx: sieve[p182] = False
        if p181 < lndx: sieve[p181] = False
        if p180 < lndx: sieve[p180] = False
        if p179 < lndx: sieve[p179] = False
        if p178 < lndx: sieve[p178] = False
        if p177 < lndx: sieve[p177] = False
        if p176 < lndx: sieve[p176] = False
        if p175 < lndx: sieve[p175] = False
        if p174 < lndx: sieve[p174] = False
        if p173 < lndx: sieve[p173] = False
        if p172 < lndx: sieve[p172] = False
        if p171 < lndx: sieve[p171] = False
        if p170 < lndx: sieve[p170] = False
        if p169 < lndx: sieve[p169] = False
        if p168 < lndx: sieve[p168] = False
        if p167 < lndx: sieve[p167] = False
        if p166 < lndx: sieve[p166] = False
        if p165 < lndx: sieve[p165] = False
        if p164 < lndx: sieve[p164] = False
        if p163 < lndx: sieve[p163] = False
        if p162 < lndx: sieve[p162] = False
        if p161 < lndx: sieve[p161] = False
        if p160 < lndx: sieve[p160] = False
        if p159 < lndx: sieve[p159] = False
        if p158 < lndx: sieve[p158] = False
        if p157 < lndx: sieve[p157] = False
        if p156 < lndx: sieve[p156] = False
        if p155 < lndx: sieve[p155] = False
        if p154 < lndx: sieve[p154] = False
        if p153 < lndx: sieve[p153] = False
        if p152 < lndx: sieve[p152] = False
        if p151 < lndx: sieve[p151] = False
        if p150 < lndx: sieve[p150] = False
        if p149 < lndx: sieve[p149] = False
        if p148 < lndx: sieve[p148] = False
        if p147 < lndx: sieve[p147] = False
        if p146 < lndx: sieve[p146] = False
        if p145 < lndx: sieve[p145] = False
        if p144 < lndx: sieve[p144] = False
        if p143 < lndx: sieve[p143] = False
        if p142 < lndx: sieve[p142] = False
        if p141 < lndx: sieve[p141] = False
        if p140 < lndx: sieve[p140] = False
        if p139 < lndx: sieve[p139] = False
        if p138 < lndx: sieve[p138] = False
        if p137 < lndx: sieve[p137] = False
        if p136 < lndx: sieve[p136] = False
        if p135 < lndx: sieve[p135] = False
        if p134 < lndx: sieve[p134] = False
        if p133 < lndx: sieve[p133] = False
        if p132 < lndx: sieve[p132] = False
        if p131 < lndx: sieve[p131] = False
        if p130 < lndx: sieve[p130] = False
        if p129 < lndx: sieve[p129] = False
        if p128 < lndx: sieve[p128] = False
        if p127 < lndx: sieve[p127] = False
        if p126 < lndx: sieve[p126] = False
        if p125 < lndx: sieve[p125] = False
        if p124 < lndx: sieve[p124] = False
        if p123 < lndx: sieve[p123] = False
        if p122 < lndx: sieve[p122] = False
        if p121 < lndx: sieve[p121] = False
        if p120 < lndx: sieve[p120] = False
        if p119 < lndx: sieve[p119] = False
        if p118 < lndx: sieve[p118] = False
        if p117 < lndx: sieve[p117] = False
        if p116 < lndx: sieve[p116] = False
        if p115 < lndx: sieve[p115] = False
        if p114 < lndx: sieve[p114] = False
        if p113 < lndx: sieve[p113] = False
        if p112 < lndx: sieve[p112] = False
        if p111 < lndx: sieve[p111] = False
        if p110 < lndx: sieve[p110] = False
        if p109 < lndx: sieve[p109] = False
        if p108 < lndx: sieve[p108] = False
        if p107 < lndx: sieve[p107] = False
        if p106 < lndx: sieve[p106] = False
        if p105 < lndx: sieve[p105] = False
        if p104 < lndx: sieve[p104] = False
        if p103 < lndx: sieve[p103] = False
        if p102 < lndx: sieve[p102] = False
        if p101 < lndx: sieve[p101] = False
        if p100 < lndx: sieve[p100] = False
        if p99 < lndx: sieve[p99] = False
        if p98 < lndx: sieve[p98] = False
        if p97 < lndx: sieve[p97] = False
        if p96 < lndx: sieve[p96] = False
        if p95 < lndx: sieve[p95] = False
        if p94 < lndx: sieve[p94] = False
        if p93 < lndx: sieve[p93] = False
        if p92 < lndx: sieve[p92] = False
        if p91 < lndx: sieve[p91] = False
        if p90 < lndx: sieve[p90] = False
        if p89 < lndx: sieve[p89] = False
        if p88 < lndx: sieve[p88] = False
        if p87 < lndx: sieve[p87] = False
        if p86 < lndx: sieve[p86] = False
        if p85 < lndx: sieve[p85] = False
        if p84 < lndx: sieve[p84] = False
        if p83 < lndx: sieve[p83] = False
        if p82 < lndx: sieve[p82] = False
        if p81 < lndx: sieve[p81] = False
        if p80 < lndx: sieve[p80] = False
        if p79 < lndx: sieve[p79] = False
        if p78 < lndx: sieve[p78] = False
        if p77 < lndx: sieve[p77] = False
        if p76 < lndx: sieve[p76] = False
        if p75 < lndx: sieve[p75] = False
        if p74 < lndx: sieve[p74] = False
        if p73 < lndx: sieve[p73] = False
        if p72 < lndx: sieve[p72] = False
        if p71 < lndx: sieve[p71] = False
        if p70 < lndx: sieve[p70] = False
        if p69 < lndx: sieve[p69] = False
        if p68 < lndx: sieve[p68] = False
        if p67 < lndx: sieve[p67] = False
        if p66 < lndx: sieve[p66] = False
        if p65 < lndx: sieve[p65] = False
        if p64 < lndx: sieve[p64] = False
        if p63 < lndx: sieve[p63] = False
        if p62 < lndx: sieve[p62] = False
        if p61 < lndx: sieve[p61] = False
        if p60 < lndx: sieve[p60] = False
        if p59 < lndx: sieve[p59] = False
        if p58 < lndx: sieve[p58] = False
        if p57 < lndx: sieve[p57] = False
        if p56 < lndx: sieve[p56] = False
        if p55 < lndx: sieve[p55] = False
        if p54 < lndx: sieve[p54] = False
        if p53 < lndx: sieve[p53] = False
        if p52 < lndx: sieve[p52] = False
        if p51 < lndx: sieve[p51] = False
        if p50 < lndx: sieve[p50] = False
        if p49 < lndx: sieve[p49] = False
        if p48 < lndx: sieve[p48] = False
        if p47 < lndx: sieve[p47] = False
        if p46 < lndx: sieve[p46] = False
        if p45 < lndx: sieve[p45] = False
        if p44 < lndx: sieve[p44] = False
        if p43 < lndx: sieve[p43] = False
        if p42 < lndx: sieve[p42] = False
        if p41 < lndx: sieve[p41] = False
        if p40 < lndx: sieve[p40] = False
        if p39 < lndx: sieve[p39] = False
        if p38 < lndx: sieve[p38] = False
        if p37 < lndx: sieve[p37] = False
        if p36 < lndx: sieve[p36] = False
        if p35 < lndx: sieve[p35] = False
        if p34 < lndx: sieve[p34] = False
        if p33 < lndx: sieve[p33] = False
        if p32 < lndx: sieve[p32] = False
        if p31 < lndx: sieve[p31] = False
        if p30 < lndx: sieve[p30] = False
        if p29 < lndx: sieve[p29] = False
        if p28 < lndx: sieve[p28] = False
        if p27 < lndx: sieve[p27] = False
        if p26 < lndx: sieve[p26] = False
        if p25 < lndx: sieve[p25] = False
        if p24 < lndx: sieve[p24] = False
        if p23 < lndx: sieve[p23] = False
        if p22 < lndx: sieve[p22] = False
        if p21 < lndx: sieve[p21] = False
        if p20 < lndx: sieve[p20] = False
        if p19 < lndx: sieve[p19] = False
        if p18 < lndx: sieve[p18] = False
        if p17 < lndx: sieve[p17] = False
        if p16 < lndx: sieve[p16] = False
        if p15 < lndx: sieve[p15] = False
        if p14 < lndx: sieve[p14] = False
        if p13 < lndx: sieve[p13] = False
        if p12 < lndx: sieve[p12] = False
        if p11 < lndx: sieve[p11] = False
        if p10 < lndx: sieve[p10] = False
        if p9  < lndx: sieve[p9]  = False
        if p8  < lndx: sieve[p8]  = False
        if p7  < lndx: sieve[p7]  = False
        if p6  < lndx: sieve[p6]  = False
        if p5  < lndx: sieve[p5]  = False
        if p4  < lndx: sieve[p4]  = False
        if p3  < lndx: sieve[p3]  = False
        if p2  < lndx: sieve[p2]  = False
        if p1  < lndx: sieve[p1]  = False
    if val < 3 : return [2]
    if val < 5 : return [2,3]
    if val < 7 : return [2,3,5]
    primes = [(i<<1)+3 for i in xrange(4, lndx, 1)  if sieve[i]]
    primes[0:0] = [2,3,5,7]
    return primes

if __name__ == '__main__':
    import time

    for j in range(5, 20000007, 1000000):
        print j,

        #a = time.time()
        #soe = sieveOfErat(j)
        #print time.time() -a,

        a = time.time()
        soa = sieveOfAtkin(j)
        print time.time() -a,

        a = time.time()
        soz1 = primesP5(j)
        print time.time() -a,

        a = time.time()
        soz2 = primesP7(j)
        print time.time() -a

        a = time.time()
        soz3 = primesP11(j)
        print time.time() -a

        assert soa == soz1 == soz2 == soz3 ##== soe

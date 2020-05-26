DEBUG = 1
import Pkg_voiceRecog as myPkg

# Test model on single file 'temp.wav'

# usr_phrase = myPkg.recogPhrase('temp.wav', 'Instruction', 0)

# Test model on all raw files

count = 0
n_AG_Samples = 0
n_FSB_Samples = 0
n_FA_Samples = 0
n_BZ_Samples = 0
n_OS_Samples = 0
n_ONE_Samples = 3
n_TWO_Samples = 3
n_THREE_Samples = 3

for i in range(1, n_AG_Samples + 1):
    filename = "Raw_Audio/R_AG_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Instruction', DEBUG)
    if usr_phrase == 'AG':
        print("R_AG_", i, " PASS")
    else:
        print("FAIL")
        print("Failed Case no: (AG)", i)
        count = count + 1
for i in range(1, n_FSB_Samples + 1):
    filename = "Raw_Audio/R_FSB_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Instruction', DEBUG)
    if usr_phrase == 'AG':
        print("R_FSB_", i, "FAIL")
        print("Failed Case no: (FSB)", i)
        count = count + 1
    else:
        print("R_FSB_", i, "PASS")
for i in range(1, n_FA_Samples + 1):
    filename = "Raw_Audio/R_FA_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Title', DEBUG)
    if usr_phrase != 'FA':
        print("R_FA_", i, "FAIL")
        print("Failed Case no: (FA)", i)
        count = count + 1
    else:
        print("R_FA_", i, "PASS")
for i in range(1, n_BZ_Samples + 1):
    filename = "Raw_Audio/R_BZ_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Title', DEBUG)
    if usr_phrase != 'BZ':
        print("R_FA_", i, "FAIL")
        print("Failed Case no: (BZ)", i)
        count = count + 1
    else:
        print("R_BZ_", i, "PASS")
for i in range(1, n_OS_Samples + 1):
    filename = "Raw_Audio/R_OS_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Title', DEBUG)
    if usr_phrase != 'OS':
        print("R_OS_", i, "FAIL")
        print("Failed Case no: (OS)", i)
        count = count + 1
    else:
        print("R_OS_", i, "PASS")
for i in range(1, n_ONE_Samples + 1):
    filename = "Raw_Audio/R_ONE_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Title_AL', DEBUG)
    if usr_phrase != 'FA':
        print("R_ONE_", i, "FAIL")
        print("Failed Case no: (ONE)", i)
        count = count + 1
    else:
        print("R_ONE_", i, "PASS")
for i in range(1, n_TWO_Samples + 1):
    filename = "Raw_Audio/R_TWO_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Title_AL', DEBUG)
    if usr_phrase != 'BZ':
        print("R_TWO_", i, "FAIL")
        print("Failed Case no: (TWO)", i)
        count = count + 1
    else:
        print("R_TWO_", i, "PASS")
for i in range(1, n_THREE_Samples + 1):
    filename = "Raw_Audio/R_THREE_" + str(i) + ".wav"
    usr_phrase = myPkg.recogPhrase(filename, 'Title_AL', DEBUG)
    if usr_phrase != 'OS':
        print("R_THREE_", i, "FAIL")
        print("Failed Case no: (THREE)", i)
        count = count + 1
    else:
        print("R_THREE_", i, "PASS")
print("Score = ", n_FSB_Samples+n_ONE_Samples+n_TWO_Samples+n_THREE_Samples + n_BZ_Samples+n_OS_Samples+ n_AG_Samples + n_FA_Samples - count, "/", n_FSB_Samples +n_BZ_Samples+n_OS_Samples+n_ONE_Samples+n_TWO_Samples+n_THREE_Samples+n_FA_Samples+ n_AG_Samples)

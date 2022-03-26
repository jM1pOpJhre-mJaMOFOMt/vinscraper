#https://dot.report/manufacturer/15984/displayfile/256d30c5-4d6f-4c1f-8f86-f1fb81aba7f2

VIN_DIGIT_POSITION_MULTIPLIER = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
VIN_DIGIT_VALUES = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1,
                  'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5,
                  'W': 6, 'X': 7, 'Y': 8, 'Z': 9, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                  '7': 7, '8': 8, '9': 9, '0': 0}

def get_check_sum_char(vin):
    sum = 0
    for i in range(len(vin)):
        sum += int(VIN_DIGIT_VALUES[vin[i]]) * VIN_DIGIT_POSITION_MULTIPLIER[i]
    remain = sum % 11
    char = repr(remain)
    if remain == 10:
        char = 'X'
    return char

def get_vin_from_serial(serial):
    return "KMHLW4AK" + get_check_sum_char("KMHLW4AK0NU" + str(serial).zfill(6)) + "NU" + str(serial).zfill(6)

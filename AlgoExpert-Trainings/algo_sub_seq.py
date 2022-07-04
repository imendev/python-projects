# solution1: while loop 
def is_valid_sub_sequence(array, sequence):
    seqIdx = 0
    arrIdx = 0
    # there is still elements in both array
    while len(array) > arrIdx and len(sequence) > seqIdx:
        if array[arrIdx] == sequence[seqIdx]:
            seqIdx += 1
        arrIdx += 1
    
    return seqIdx == len(sequence)
        
# solution2: for loop 
def is_valid_two_sub_sequence(array, sequence):
    seqIdx = 0
    # for each element inside the 1st array
    for value in array:
        if len(sequence) == seqIdx:
            break
        if value == sequence[seqIdx]:
            seqIdx += 1
    
    return seqIdx == len(sequence)


dic = {
    "array": [1, 3, -7, 9, -22, 5, 12, 0],
    "sequence": [ 3, -22, 5, 12]
    }
dic1 = {
    "array": [1, 3, -7, 9, -22, 5, 12, 0],
    "sequence": [ 3,5, -22,12]
    }
is_valid = is_valid_sub_sequence(dic1["array"], dic1["sequence"])
is_valid_two = is_valid_two_sub_sequence(dic["array"], dic["sequence"])

print(dic["array"])
print(dic["sequence"])
print(is_valid)
print(is_valid_two)



start, _, *f = open("input.txt", "rb").readlines()

splitCount = 0
hashSet = set()
hashMap = dict()


indexOfS = start.decode().strip().index("S")
hashSet.add(indexOfS)
hashMap[indexOfS] = 1


for i in range(len(f)):
    parsedRow = f[i].strip().decode()
    for j in range(len(parsedRow)):
        if(parsedRow[j] == "^" and j in hashSet):
            splitCount += 1
            hashSet.remove(j) 
            hashSet.add(j - 1) 
            hashSet.add(j + 1) 


            count = hashMap[j]
            del hashMap[j]
            hashMap[j - 1] = hashMap.get(j - 1, 0) + count
            hashMap[j + 1] = hashMap.get(j + 1, 0) + count


print("Part 1:", splitCount)
print("Part 2:", sum(hashMap.values()))
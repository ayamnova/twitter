mat = ""
fout = open('degrees', 'w')
with open("userMatrix2", 'r') as f:
    count = 0
    for line in f:
        if count % 1000 == 0:
            print("1,000 Done")
        nums = [int(n) for n in line.split("\t") if n is not "\n"]
        total = sum(nums)
        mat += str(total) + ","
        count += 1
f.close()
mat = mat.rstrip(",")
fout.write(mat)



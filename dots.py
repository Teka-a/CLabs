def find_quadratic_residues(p):
    residues = []
    nums = {}
    for i in range(p):
        y2 = (i ** 2)
        residue = y2 % p
        if residue in nums:
            mas = nums.get(residue)
            mas.append(i)
            nums[residue] = mas
        else:
            nums[residue] = [i]
        residues.append(residue)
    sorted_residues = dict(sorted(nums.items(), key=lambda x: x[0]))
    return sorted_residues

def find_dots(a, b, p):
    # массив точек содержит точки в виде массива [x,y] : dots = [[x,y],[x,y]]
    dots = []

    quadratic_residues = find_quadratic_residues(p)

    for x in range(p):
        ys = []
        y2 = (x ** 3 + a*x + b) % p
        if y2 in quadratic_residues:
            mas = quadratic_residues.get(y2)
            for o in mas:
                ys.append(str(o))
                dot = [x, o]
                dots.append(dot)
    return dots


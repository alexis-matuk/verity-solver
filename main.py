# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from enum import Enum
from itertools import permutations
from copy import deepcopy


class TwoDShape(Enum):
    Circle = 1
    Square = 2
    Triangle = 3


class ThreeDShape(Enum):
    Pyramid = 1
    Sphere = 2
    Cube = 3
    Cone = 4
    Cylinder = 5
    Prism = 6


twoDArr = [TwoDShape.Circle, TwoDShape.Square, TwoDShape.Triangle]

twoD_sum_dict = {
    TwoDShape.Circle: {TwoDShape.Circle: ThreeDShape.Sphere,
                       TwoDShape.Square: ThreeDShape.Cylinder,
                       TwoDShape.Triangle: ThreeDShape.Cone},

    TwoDShape.Square: {TwoDShape.Circle: ThreeDShape.Cylinder,
                       TwoDShape.Square: ThreeDShape.Cube,
                       TwoDShape.Triangle: ThreeDShape.Prism},

    TwoDShape.Triangle: {TwoDShape.Circle: ThreeDShape.Cone,
                         TwoDShape.Square: ThreeDShape.Prism,
                         TwoDShape.Triangle: ThreeDShape.Pyramid}
}

threeD_to_twoD = {
    ThreeDShape.Pyramid: [TwoDShape.Triangle, TwoDShape.Triangle],
    ThreeDShape.Sphere: [TwoDShape.Circle, TwoDShape.Circle],
    ThreeDShape.Cube: [TwoDShape.Square, TwoDShape.Square],
    ThreeDShape.Cone: [TwoDShape.Triangle, TwoDShape.Circle],
    ThreeDShape.Cylinder: [TwoDShape.Circle, TwoDShape.Square],
    ThreeDShape.Prism: [TwoDShape.Square, TwoDShape.Triangle]
}

solution_to_twoD = {
    TwoDShape.Circle: ThreeDShape.Prism,
    TwoDShape.Square: ThreeDShape.Cone,
    TwoDShape.Triangle: ThreeDShape.Cylinder
}


def add2DShapes(shape1, shape2):
    return twoD_sum_dict[shape1][shape2]


def isCombinationSolvable(s1, s2, s3):
    combination_sum = threeD_to_twoD[s1] + threeD_to_twoD[s2] + threeD_to_twoD[s3]
    result_dict = {}
    for item in combination_sum:
        if item in result_dict:
            result_dict[item] += 1
        else:
            result_dict[item] = 1
    for item in result_dict:
        if TwoDShape.Circle not in result_dict or TwoDShape.Square not in result_dict or TwoDShape.Triangle not in result_dict:
            return False
        if result_dict[item] < 2:
            return False
    return True


def enumToDetailedName(shape):
    match shape:
        case ThreeDShape.Pyramid:
            return 'Pyramid (TT)'
        case ThreeDShape.Sphere:
            return 'Sphere (CC)'
        case ThreeDShape.Cube:
            return 'Cube (SS)'
        case ThreeDShape.Cone:
            return 'Cone (TC)'
        case ThreeDShape.Cylinder:
            return 'Cylinder (ST)'
        case ThreeDShape.Prism:
            return 'Prism (ST)'


def generateCombinations():
    counter = 0
    p = permutations(twoDArr)
    result = []

    for perm in p:
        for s1 in ThreeDShape:
            for s2 in ThreeDShape:
                for s3 in ThreeDShape:
                    if isCombinationSolvable(s1, s2, s3):
                        # print(perm[0].name, perm[1].name, perm[2].name, enumToDetailedName(s1), enumToDetailedName(s2), enumToDetailedName(s3))
                        counter += 1
                        result.append([[perm[0], perm[1], perm[2]], [s1, s2, s3]])
    print(counter)
    return result


def printCombinationMatrix(combinationMatrix):
    for entry in combinationMatrix:
        print(entry[0][0].name, entry[0][1].name, entry[0][2].name, entry[1][0].name, entry[1][1].name,
              entry[1][2].name)


def getSame2dComponentsOf3dShapes(shape1, shape2):
    shape1Comps = threeD_to_twoD[shape1]
    shape2Comps = threeD_to_twoD[shape2]
    for x in shape1Comps:
        for y in shape2Comps:
            if x == y:
                return x
    return None

def getOfferableComponent(wantedShape, shape1):
    wantedShapeComps = threeD_to_twoD[wantedShape]
    shape1Comps = threeD_to_twoD[shape1]
    lockedOneShape = False
    for x in shape1Comps:
        if x in wantedShapeComps and not lockedOneShape:
            lockedOneShape = True
            continue
        return x


def swap2dComponents(shape1, shape2, twoDComponent1, twoDComponent2):
    localDict = deepcopy(threeD_to_twoD)
    shape1Comps = localDict[shape1]
    shape2Comps = localDict[shape2]
    index1 = shape1Comps.index(twoDComponent1)
    index2 = shape2Comps.index(twoDComponent2)
    shape1Comps[index1] = twoDComponent2
    shape2Comps[index2] = twoDComponent1
    return twoD_sum_dict[shape1Comps[0]][shape1Comps[1]], twoD_sum_dict[shape2Comps[0]][shape2Comps[1]]

def shapeIsSolved(twoDshape, threeDshape):
    return solution_to_twoD[twoDshape] == threeDshape

def isEntrySolved(insideTuple, outsideTuple):
    return shapeIsSolved(insideTuple[0], outsideTuple[0]) \
           and shapeIsSolved(insideTuple[1], outsideTuple[1]) \
           and shapeIsSolved(insideTuple[2], outsideTuple[2])

def indexToNamedPosition(i):
    match i:
        case 0:
            return "left"
        case 1:
            return "mid"
        case 2:
            return "right"

def getCombinationSolution(combinationEntry):
    insideTuple = combinationEntry[0]
    outsideTuple = combinationEntry[1]
    solvedInside = [False, False, False]

    currentlySolvingFor2D = 0

    # choose starting shape with existing solution 2d shape for efficiency in movements
    for idx, threeDshape in enumerate(outsideTuple):
        sameComponents = getSame2dComponentsOf3dShapes(solution_to_twoD[insideTuple[idx]], threeDshape)
        if sameComponents is not None:
            currentlySolvingFor2D = idx
            break

    print("=========")
    print("starting shape:", indexToNamedPosition(currentlySolvingFor2D))
    while not isEntrySolved(insideTuple, outsideTuple):
        for idx, x in enumerate(outsideTuple):
            if idx == currentlySolvingFor2D or (solvedInside[idx] is True):
                continue
            wantedSolutionShape = solution_to_twoD[insideTuple[currentlySolvingFor2D]]
            wantedComponent = getSame2dComponentsOf3dShapes(wantedSolutionShape, x)
            if wantedComponent is None:
                continue
            #found a shape to swap with
            offeredComponent = getOfferableComponent(solution_to_twoD[insideTuple[currentlySolvingFor2D]], outsideTuple[currentlySolvingFor2D])
            newCurrentlySolvingShape, newSwappedShape = swap2dComponents(outsideTuple[currentlySolvingFor2D], x, offeredComponent ,wantedComponent)
            print("swapping", offeredComponent.name, "in", indexToNamedPosition(currentlySolvingFor2D), "with", wantedComponent.name, "in", indexToNamedPosition(idx))
            outsideTuple[currentlySolvingFor2D] = newCurrentlySolvingShape
            outsideTuple[idx] = newSwappedShape
            if shapeIsSolved(insideTuple[currentlySolvingFor2D], outsideTuple[currentlySolvingFor2D]):
                solvedInside[currentlySolvingFor2D] = True
                currentlySolvingFor2D = (currentlySolvingFor2D + 1) % 2
                break

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    combinationList = generateCombinations()
    # printCombinationMatrix(combinationList)
    testEntry9 = [[TwoDShape.Circle, TwoDShape.Square, TwoDShape.Triangle],[ThreeDShape.Pyramid, ThreeDShape.Sphere, ThreeDShape.Cube]]
    testEntry10 = [[TwoDShape.Circle, TwoDShape.Square, TwoDShape.Triangle],[ThreeDShape.Pyramid, ThreeDShape.Cube, ThreeDShape.Sphere]]
    testEntry11 = [[TwoDShape.Circle, TwoDShape.Square, TwoDShape.Triangle],[ThreeDShape.Pyramid, ThreeDShape.Cylinder, ThreeDShape.Cylinder]]
    testEntry12 = [[TwoDShape.Circle, TwoDShape.Square, TwoDShape.Triangle],[ThreeDShape.Sphere, ThreeDShape.Pyramid, ThreeDShape.Cube]]
    testEntry13 = [[TwoDShape.Circle, TwoDShape.Square, TwoDShape.Triangle],[ThreeDShape.Sphere, ThreeDShape.Cube, ThreeDShape.Pyramid]]

    for idx, x in enumerate(combinationList):
        print(idx+1)
        getCombinationSolution(x)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

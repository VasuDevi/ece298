from os import path
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import random as r, numpy as np


templateCase = SolutionDirectory("/home/vasu/Downloads/parameterStudy/template_square", archive=None, paraviewLink=False)


# Define parameters
start_pre = -25
end_post = 65
height = 10
thickness = 0.5
allowance = 0.0001


for p in range(2):
    # Define case
    case_name = "sq_case_" + str(p)
    print(case_name)
    case = templateCase.cloneCase(case_name)

    # Checks
    file = ParsedParameterFile(path.join(case.name,"system", "blockMeshDict"))

    # Define parameters
    start_obstacle = r.uniform(-25, 45)
    start_post = start_obstacle + 2 * height
    ob_center = start_obstacle + height
    radius = r.uniform(allowance, 5-allowance)
    cyl_start = ob_center - radius
    cyl_end = ob_center + radius

    # Setting vertices
    new_vertices = [

        # "// pre-block",
        "({}   -{}   {}) // 0".format(start_pre, height, thickness),
        "({}   -{}   {}) // 1".format(start_obstacle, height, thickness),
        "({}   -{}  -{}) // 2".format(start_obstacle, height, thickness),
        "({}   -{}  -{}) // 3".format(start_pre, height, thickness),

        "({}   {}   {}) // 4".format(start_pre, height, thickness),
        "({}   {}   {}) // 5".format(start_obstacle, height, thickness),
        "({}   {}  -{}) // 6".format(start_obstacle, height, thickness),
        "({}   {}  -{}) // 7".format(start_pre, height, thickness),

        # "// obstacle blocks",
        "({}   -{}   {}) // 8".format(start_post, height, thickness),
        "({}   -{}  -{}) // 9".format(start_post, height, thickness),           


        "({} -{}  {}) // 10".format(cyl_start, radius, thickness),
        "({} -{}  {}) // 11".format(cyl_end, radius, thickness),
        "({} -{} -{}) // 12".format(cyl_end, radius, thickness),
        "({} -{} -{}) // 13".format(cyl_start, radius, thickness),

        "({}  {}  {}) // 14".format(cyl_start, radius, thickness),
        "({}  {} -{}) // 15".format(cyl_start, radius, thickness),

        "({}  {}  {}) // 16".format(cyl_end, radius, thickness),
        "({}  {} -{}) // 17".format(cyl_end, radius, thickness),

        "({}   {}   {}) // 18".format(start_post, height, thickness),
        "({}   {}  -{}) // 19".format(start_post, height, thickness),

        # "// post-block",
        "({}   -{}  {}) // 20".format(end_post, height, thickness),
        "({}   -{} -{}) // 21".format(end_post, height, thickness),
        "({}    {}  {}) // 22".format(end_post, height, thickness),
        "({}    {} -{}) // 23".format(end_post, height, thickness)
    ]

    # Define blocks
    new_blocks = [
        # "// pre-block",
        "hex ( 0  1  2  3  4  5  6  7) ( 60 1 30) simpleGrading (1 1 1)",

        # "// obstacle blocks",
        "hex ( 1  8  9  2 10 11 12 13) (30 1 30) simpleGrading (1 1 1) // bottom",
        "hex ( 1 10 13  2  5 14 15  6) (30 1 30) simpleGrading (1 1 1) // left",
        "hex (14 16 17 15  5 18 19  6) (30 1 30) simpleGrading (1 1 1) // top",
        "hex (11  8  9 12 16 18 19 17) (30 1 30) simpleGrading (1 1 1) // right",

        # "// post-block",
        "hex ( 8 20 21  9 18 22 23 19) (180 1 30) simpleGrading (1 1 1)"
    ]

    # Define random values
    mid = (np.random.rand(1, 8) * height).squeeze()
    mid_start = ((ob_center - start_obstacle) * np.random.rand(1, 4) + start_obstacle).squeeze()
    mid_end = ((start_post - ob_center) * np.random.rand(1, 4) + ob_center).squeeze()
    

    # Define edge types
    edge_types = np.random.randint(2, size=8)


    line_types = [
        "line 10 11",
        "line 12 13",
        "line 14 10",
        "line 15 13",
        "line 14 16",
        "line 15 17",
        "line 16 11",
        "line 17 12",
    ]

    arc_types = [
        "arc 10 11 ({} -{}  {})".format(mid_start[0].item(), mid[0].item(), thickness),
        "arc 12 13 ({} -{} -{})".format(mid_start[1].item(), mid[1].item(), thickness),
        "line 14 10",
        "line 15 13",
        "arc 14 16 ({}  {}  {})".format(mid_end[0].item(), mid[4].item(), thickness),
        "arc 15 17 ({}  {} -{})".format(mid_end[1].item(), mid[5].item(), thickness),
        "line 16 11",
        "line 17 12",
    ]

    # polyLine_types = [
    #     "polyLine 10 11 ( ({} -{}  {}) )".format(mid_start[0].item(), mid[0].item(), thickness),
    #     "polyLine 12 13 ( ({} -{} -{}) )".format(mid_start[1].item(), mid[1].item(), thickness),
    #     "line 14 10",
    #     "line 15 13",
    #     "polyLine 14 16 ( ({}  {}  {}) )".format(mid_end[0].item(), mid[4].item(), thickness),
    #     "polyLine 15 17 ( ({}  {} -{}) )".format(mid_end[1].item(), mid[5].item(), thickness),
    #     "line 16 11",
    #     "line 17 12",
    # ]

    # Define edges
    new_edges = []

    for e in range(len(edge_types)):
        if edge_types[e] == 0:
            new_edges.append(line_types[e])
        elif edge_types[e] == 1:
            new_edges.append(arc_types[e])
        # elif edge_types[e] == 2:
        #     new_edges.append(polyLine_types[e])

    # Write to file
    file["vertices"] = new_vertices
    file["blocks"] = new_blocks
    file["edges"] = new_edges
    file.writeFile()
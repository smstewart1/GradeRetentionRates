import csv
from sys import argv

# sets up global variables
# in the future the curriculum code will need to expanded and the courselist will need to contain nested lists of the form [[#...#],[#....#]...] to account for each program's unique course numbers
Semester = []
Course = []
# placeholder for when more than one program is being analyzed; for now the CSV data is only being given with the course numbers
Curriculum = ["CHM"]
CourseList = ["90", "130", "131", "131A", "132", "151", "152", "251", "252"]
Capacity = []
Students = []
Location = []
LocationMaster = ["ONL ", "401S", "401N", "HS", "WEST", "RTP "]
Delivery = []
MasterDelivery = ["ON", "TR", "BL"]


def main():
    # create semester lists
    RegList = []
    for l in range(2011, 2023):
        RegList.append(f"{l}SP")
        RegList.append(f"{l}FA")
    SummerList = []
    for l in range(2011, 2023):
        SummerList.append(f"{l}SU")

    # Counts for capacity (C) and students (S) and total number of points (N)
    C = 0
    S = 0
    N = 0
    # import files
    try:
        input = open(argv[1], "r")
    except:
        print("List the file to be read in")

    # reads in data
    with input as file:
        lines = csv.reader(file)
        next(lines)
        for row in lines:
            # loads student information
            Semester.append(str(row[0]))
            Course.append(str(row[1]))
            Capacity.append(int(row[2]))
            Students.append(int(row[3]))
            Location.append(str(row[4]))
            Delivery.append(str(row[5]))

            # Updates Counters
            N += 1
    cleaner(N, Location, Delivery)
    Type = ["Regular", "Summer"]
    OtherType = ["Capacity", "Enrollment"]
    for i in Curriculum:
        reporter(N, i, Course, Semester, Location, RegList, Capacity, Type[0], OtherType[0])
        reporter(N, i, Course, Semester, Location, RegList, Students, Type[0], OtherType[1])
        reporter(N, i, Course, Semester, Location, SummerList, Capacity, Type[1], OtherType[0])
        reporter(N, i, Course, Semester, Location, SummerList, Students, Type[1], OtherType[1])
        phaseplot(N, i, Course, Semester, Location, RegList, Students, Capacity, Delivery, Type[0])


def phaseplot(N, Curriculum, Course, Semester, Location, Semesters, Students, Capacity, Delivery, Type):
    # reports by course number
    for i in CourseList:
        # overall by course
        string = f"{i}_{Type}_{Curriculum}_PhasePlots.csv"
        filename = string
        with open(filename, "w") as output:
            # start by sorting by location
            for j in LocationMaster:
                # sort by method of delivery
                for m in MasterDelivery:
                    Counter = []
                    output.write(f"{j} {m}\nN N+1\n")
                    for l in Semesters:
                        S = 0
                        C = 0
                        for k in range(0, N-1):
                            # future code will add Curriculum[k] == Curriculum
                            if (Course[k] == i and Semester[k] == l and Location[k] == j and Delivery[k] == m):
                                S = S + Students[k]
                                C = C + Capacity[k]
                        Counter.append([S, C])
                    for l in range(1, len(Counter)-1):
                        if Counter[l][1] != 0 and Counter[l-1][1] != 0:
                            output.write(f"{Counter[l-1][0]},{Counter[l][0]}\n")
                    output.write("\n\n")
            output.close()


def reporter(N, Curriculum, Course, Semester, Location, Semesters, Students, Type, OtherType):
    # reports by course number
    for i in CourseList:
        # overall by course
        string = f"{i}_{Type}_{OtherType}_{Curriculum}_Students.csv"
        filename = string
        with open(filename, "w") as output:
            # start by sorting by location
            for j in LocationMaster:
                # prints the online courses
                if j == "ONL ":
                    output.write(f"{j}\nSemester, Online\n")
                    for l in Semesters:
                        S = 0
                        for k in range(0, N-1):
                            # future code will add Curriculum[k] == Curriculum
                            if (Course[k] == i and Semester[k] == l and Location[k] == j):
                                S = S + Students[k]
                        string = f"{l}, {S} \n"
                        output.write(string)
                # prints all others
                else:
                    output.write(f"{j}\nSemester, In Person, Hybrid\n")
                    for l in Semesters:
                        Sinperson = 0
                        Shybrid = 0
                        for k in range(0, N-1):
                            # future code will add Curriculum[k] == Curriculum
                            if (Course[k] == i and Semester[k] == l and Location[k] == j and Delivery[k] == "TR"):
                                Sinperson = Sinperson + Students[k]
                        for k in range(0, N-1):
                            # future code will add Curriculum[k] == Curriculum
                            if (Course[k] == i and Semester[k] == l and Location[k] == j and Delivery[k] == "HY"):
                                Shybrid = Shybrid + Students[k]
                        string = f"{l}, {Sinperson}, {Shybrid}\n"
                        output.write(string)
                output.write("\n\n")
        output.close()


def cleaner(N, campus, deployment):
    for i in range(0, N-1):
        if campus[i] == "ONL":
            deployment[i] = "ON"
        else:
            if deployment[i] == "BL":
                deployment[i] = "HY"
            if deployment[i] == "WB":
                deployment[i] = "TR"
    return 0


main()
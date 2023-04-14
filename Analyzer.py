import csv
from sys import argv

# sets up global variables
Ethnicity = {}
EthList = []
CourseX = []
CourseY = []
CourseNX = []
CourseNY = []
GradeX = []
GradeY = []
TermX = []
TermY = []
YearX = []
YearY = []
DeliveryX = []
DeliveryY = []
StudentID = []
OutputLaziness = ["A", "B", "C", "D", "F", "W/WE/WF/WP"]

# cutoff for the minimum number of data point for report by number of students
Cutoff = 100


def main():
    # Counts for the different courses
    N = 0

    # import files
    try:
        input = open(argv[1], "r")
    except:
        print("List the file to be read in")

    # lists the matrices to be used
    Grades = {"A": 1, "B": 2, "C": 3, "D": 4, "F": 5, "W": 6}

    # reads in data
    with input as file:
        lines = csv.reader(file)
        next(lines)
        for row in lines:
            # loads student information
            StudentID.append(int(row[0]))
            EthList.append(row[1])
            Ethnicity.update({row[1]: int(row[0])})

            # loads the Y data for an entry
            Course = row[2]
            CourseNY.append(int(Course[4:7]))
            CourseY.append(Course[0:3])
            Grade = row[3]
            GradeY.append(int(Grades[Grade[0]]))
            Term = row[4]
            TermY.append(Term[4:5])
            YearY.append(Term[0:3])
            DeliveryY.append(swapper(row[5]))

            # loads the X data for an entry
            Course = row[6]
            CourseNX.append(int(Course[4:7]))
            CourseX.append(Course[0:3])
            Grade = row[7]
            GradeX.append(int(Grades[Grade[0]]))
            Term = row[8]
            TermX.append(Term[4:5])
            YearX.append(Term[0:3])
            DeliveryX.append(swapper(row[9]))

            # Updates Counters
            N += 1

    # Creates lists of unique student IDs, Ethnicities, Courses, Course Numbers
    SSID = set(StudentID)
    CourseNumbers = sorted(list(set(CourseNX + CourseNY)))
    CourseList = sorted(list(set(CourseX)))
    Ethnics = list(set(EthList))
    DelMods = sorted(list(set(DeliveryX)))

    # starts generating reports for overall performance
    distr(N)

    # overall report by ethnicity
    for j in range(0, len(Ethnics)):
        distrEO(N, Ethnics[j])

    # overall by ethnicity and deployment method
    for j in range(0, len(Ethnics)):
        for k in range(0, len(DelMods)):
            for l in range(0, len(DelMods)):
                distrOEIO(N, Ethnics[j], DelMods[k], DelMods[l])

    # overall by just incoming course
    for k in range(0, len(DelMods)):
        distrI(N, DelMods[k])
    for k in range(0, len(DelMods)):
        for l in range(0, len(Ethnics)):
            distrEI(N, Ethnics[l], DelMods[k])

    # overall by delivery method
    for k in range(0, len(DelMods)):
        for l in range(0, len(DelMods)):
            distrIO(N, DelMods[k], DelMods[l])

    # reports by course number
    for i in range(0, len(CourseNumbers) - 1):
        # overall by course
        distrA(N, CourseNumbers[i], CourseNumbers[i + 1])
        # generates reports based on ethnicity
        for j in range(0, len(Ethnics)):
            distrE(N, CourseNumbers[i], CourseNumbers[i + 1], Ethnics[j])
            # sort over delivery methods 
            for k in range(0, len(DelMods) - 1):
                  distrEID(N, CourseNumbers[i], CourseNumbers[i + 1], Ethnics[j], DelMods[k])
                  distrEFD(N, CourseNumbers[i], CourseNumbers[i + 1], Ethnics[j], DelMods[k])
            for k in range(0, len(DelMods) - 1):
                 for l in range(0, len(DelMods) - 1):
                     distrEDD(N, CourseNumbers[i], CourseNumbers[i + 1], Ethnics[j], DelMods[k], DelMods[l])
        # sort just over delivery methods
        for k in range(0, len(DelMods)):
             distrID(N, CourseNumbers[i], CourseNumbers[i + 1], DelMods[k])
             distrFD(N, CourseNumbers[i], CourseNumbers[i + 1], DelMods[k])
        for k in range(0, len(DelMods)):
            for l in range(0, len(DelMods)):
                distrDD(N, CourseNumbers[i], CourseNumbers[i + 1], DelMods[k], DelMods[l])
    print(f"Reports were omitted if the number of students was less than {Cutoff} students")


# converts old names for course delivery to the current definitions
def swapper(item):
    if (item == "IN"):
        string = "Online"
    elif (item == "HY" or item == "BL"):
        string = "Hybrid"
    else:
        string = "Inperson"
    return string


# script for printing output to files
def Script(array):
    string = f"Grade in First Course Followed by Grade in Next Course \nN = {array[3][0] + array[3][1] + array[3][2]}\nn = "
    string = string + f"{array[3][0]} {array[3][1]} {array[3][2]}\nGrade A B C \n"
    for i in range(0, 6):
        string = string + f"{OutputLaziness[i]} "
        for j in range(0, 3):
            if array[3][j] == 0:
                string = string + "-- "
            else:
                string = string + f"{array[j][i]/array[3][j] * 100:.2f}% "
        string = string + "\n"
    return string


# the following generates the reports and are functions for specific filters
def distr(N):
    # gives the overall distribution for all courses given
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = "Allcourses.txt"
        with open(filename, "w") as output:
            output.write("No Restrictions - all course, ethnicities, and deployment methods\n")
            output.write(Script(Distribution))
    return 0


def distrEO(N, ethnicity):
    # gives the overall distribution for all courses given by ethnicity
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (GradeX[i] < 4 and GradeY[i] < 7 and EthList[i] == ethnicity):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"AllcoursesE_{ethnicity}.txt"
        with open(filename, "w") as output:
            output.write(f"No Restrictions with ethnicity being {ethnicity}\n")
            output.write(Script(Distribution))
    return 0


def distrIO(N, DelOne, DelTwo):
    # gives the overall distribution for all courses given by deployment methods
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (GradeX[i] < 4 and GradeY[i] < 7 and DeliveryX[i] == DelOne and DeliveryY[i] == DelTwo):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"AllcoursesDX_{DelOne}_DY_{DelTwo}.txt"
        with open(filename, "w") as output:
            output.write(f"No Restrictions with DX being {DelOne} and DY being {DelTwo}\n")
            output.write(Script(Distribution))
    return 0


def distrOEIO(N, ethnicity, DelOne, DelTwo):
    # gives the overall distribution for all courses given by deployment methods and ethnicity
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (GradeX[i] < 4 and GradeY[i] < 7 and DeliveryX[i] == DelOne and DeliveryY[i] == DelTwo and EthList[i] == ethnicity):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"AllcoursesE_{ethnicity}_DX_{DelOne}_DY_{DelTwo}.txt"
        with open(filename, "w") as output:
            output.write(f"No Restrictions ethnicity is {ethnicity} DX is {DelOne} and DY is {DelTwo}\n")
            output.write(Script(Distribution))
    return 0


def distrI(N, DelOne):
    # gives the overall distribution for all courses given by deployment methods and ethnicity
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (GradeX[i] < 4 and GradeY[i] < 7 and DeliveryX[i] == DelOne):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"AllcoursesE_DX_{DelOne}.txt"
        with open(filename, "w") as output:
            output.write(f"No Restrictions DX is {DelOne}\n")
            output.write(Script(Distribution))
    return 0


def distrEI(N, ethnicity, DelOne):
    # gives the overall distribution for all courses given by deployment methods and ethnicity
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (GradeX[i] < 4 and GradeY[i] < 7 and DeliveryX[i] == DelOne and EthList[i] == ethnicity):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"AllcoursesE_{ethnicity}_DX_{DelOne}.txt"
        with open(filename, "w") as output:
            output.write(f"No Restrictions ethnicity is {ethnicity} DX is {DelOne}\n")
            output.write(Script(Distribution))
    return 0


def distrA(N, name, nametwo):
    # gives the overall distribution by course with no filters
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + " No Restrictions \n")
            output.write(Script(Distribution))
    return 0


def distrE(N, name, nametwo, ethnicity):
    # gives the distribution based on ethnicity
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and EthList[i] == ethnicity and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + f"E_{ethnicity}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + " FOR all student where Ethnicity = " + f"{ethnicity} \n")
            output.write(Script(Distribution))
    return 0


def distrEID(N, name, nametwo, ethnicity, DelOne):
    # gives the distribution based on ethnicity and initial delivery method
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and EthList[i] == ethnicity and DeliveryX[i] == DelOne and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + f"E_{ethnicity}_DX_{DelOne}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + " FOR all student where Ethnicity = " + f"{ethnicity} and the Initial Delivery is {DelOne}\n")
            output.write(Script(Distribution))
    return 0


def distrEDD(N, name, nametwo, ethnicity, DelOne, DelTwo):
    # gives the distribution based on ethnicity and intial + final delivery method
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and EthList[i] == ethnicity and DeliveryX[i] == DelOne and DeliveryY[i] == DelTwo and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + f"E_{ethnicity}_DX_{DelOne}_DY_{DelTwo}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + " FOR all student where Ethnicity = " + f"{ethnicity} and the Initial Delivery is {DelOne} and the Final Delivery is {DelTwo}\n")
            output.write(Script(Distribution))
    return 0


def distrEFD(N, name, nametwo, ethnicity, DelTwo):
    # gives the distribution based on ethnicity and final delivery method
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and EthList[i] == ethnicity and DeliveryY[i] == DelTwo and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + f"E_{ethnicity}_DY_{DelTwo}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + " FOR all student where Ethnicity = " + f"{ethnicity} and the Final Delivery is {DelTwo}\n")
            output.write(Script(Distribution))
    return 0


def distrID(N, name, nametwo, DelOne):
    # gives the distribution based on initial delivery method
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and DeliveryX[i] == DelOne and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + f"_DX_{DelOne}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + f" FOR all student where the initial delivery is {DelOne}\n")
            output.write(Script(Distribution))
    return 0


def distrDD(N, name, nametwo, DelOne, DelTwo):
    # gives the distribution based on intial + final delivery method
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and DeliveryX[i] == DelOne and DeliveryY[i] == DelTwo and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + f"_DX_{DelOne}_DY_{DelTwo}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + f" FOR all student where the Initial Delivery is {DelOne} and the Final Delivery is {DelTwo}\n")
            output.write(Script(Distribution))
    return 0


def distrFD(N, name, nametwo, DelTwo):
    # gives the distribution based on final delivery method
    # sets up initial matrix
    Distribution = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0]]

    # searches for given criteria
    for i in range(0, N-1):
        if (CourseNY[i] == int(nametwo) and CourseNX[i] == int(name) and DeliveryY[i] == DelTwo and GradeX[i] < 4 and GradeY[i] < 7):
            # adds the student's grade to the distribution based on their grade in the subsequent course
            Distribution[GradeX[i] - 1][GradeY[i] - 1] += 1

            # counts the number of students who came in with an A, B, or C
            Distribution[3][GradeX[i] - 1] += 1

    # prints results to file ignoring if the number of data points is less than the cutoff
    if ((Distribution[3][0] + Distribution[3][1] + Distribution[3][2] > Cutoff)):
        filename = f"{name}" + f"{nametwo}" + f"_DY_{DelTwo}" + ".txt"
        with open(filename, "w") as output:
            output.write(f"{nametwo}" + " vs. " + f"{name}" + f" FOR all student where Final Delivery is {DelTwo}\n")
            output.write(Script(Distribution))
    return 0


main()

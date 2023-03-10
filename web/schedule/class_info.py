import requests
# from schedule_structure import Schedule, Professor, Course, Course_Time
import time
import json

# Data to be stored
# Course name, section code
# Prof
# Location
# Time

def getClassInfo(year: int, quarter: str, department: str) -> dict[int: list[dict]]:
    response = requests.get(f"https://api.peterportal.org/rest/v0/schedule/soc?term={year}%20{quarter}&department={department}").content.decode("utf-8")
    if response == '{"schools":[]}' : return {}
    response = json.loads(response)
    response = getInfo(response)
    return response

def getInfo(response: dict) -> dict[str: list[dict]]:
    info = {}
    for course in response["schools"][0]["departments"][0]["courses"]:
        sections = []
        print(f"\tProcessing {course['deptCode']} {course['courseNumber']}")
        for section in course["sections"]:
            print(f"\t\tProcessing {section['sectionCode']}")
            # print(section)
            sectionType = section["sectionType"]
            sectionNum = section["sectionNum"]
            units = section["units"]
            finalExam = section["finalExam"]
            course_id = section["sectionCode"]
            professors = section["instructors"]
            location = section["meetings"][0]["bldg"]
            course_time = {"days": section["meetings"][0]["days"], "time": section["meetings"][0]["time"]}
            sections.append({"ID": course_id, "sectionType": sectionType, "sectionNum": sectionNum, "units": units, "finalExam": finalExam, "professors": professors, "location": location, "time": course_time})
            # time = Course_Time(False, False, False, False, False, 0, 0)
            # if "M" in section["meetings"][0]["days"]:
            #     time.mon = True
            # if "Tu" in section["meetings"][0]["days"]:
            #     time.tue = True
            # if "W" in section["meetings"][0]["days"]:
            #     time.wed = True
            # if "Th" in section["meetings"][0]["days"]:
            #     time.thu = True
            # if "F" in section["meetings"][0]["days"]:
            #     time.fri = True
            # times = convert_time(section["meetings"][0]["time"])
            # time.start = times[0]
            # time.end = times[1]
            # info.append(Course(course_name, course_id, professors, time, location))
        info.update({f"{course['deptCode']} {course['courseNumber']}": sections})
    return info

def convert_time(time: str) -> list[int, int]:
    if time == "" or time == "TBA": return [0,0]
    pm_offset = 0 if "p" not in time else 1200
    times = time.split("-")
    for i in [0, 1]:
        t = ''.join(c for c in times[i] if c.isdigit())
        times[i] = int(t) + pm_offset
    return times


def getAllCourses() -> None:
    """
    Retrieves all UCI courses and store in file
    """
    response = requests.get("https://api.peterportal.org/rest/v0/courses/all")
    if response.status_code == 200:
        with open("all_courses.json", "wb") as f:
            f.write(response.content)


def getAllCourseNames() -> None:
    """
    Retrieves all UCI course names from json file.
    """
    all_course_dict = {}
    with open("all_courses.json", "rb") as f:
        all_course_dict = json.load(f)
    
    with open("all_course_names.txt", "w") as f:
        for course in all_course_dict:
            f.write(f"{course.get('department', None)} {course.get('number', None)}\n")


def getDepartments():
    departments = set()
    with open("all_course_names.txt", "r") as f:
        for line in f:
            departments.add(line.rsplit(" ", 1)[0])
    return departments

if __name__ == "__main__":
    all_class = {}
    for department in getDepartments():
        time.sleep(0.5)
        department = department.replace("&", "%26")
        department = department.replace("/", "%2F")
        print(f"Processing {department}...")
        
        all_class.update(getClassInfo(2023, "Winter", department))

    with open("all_course_info.json", "w") as fout:
        json.dump(all_class, fout)

    # with open("all_course_names.txt", "r") as fin:
    #     # counter = 0
    #     all_class = {}

    #     for line in fin:
    #         course = line.strip().rsplit(sep=" ", maxsplit=1)
    #         time.sleep(0.1)
    #         print(f"Retrieving {course[0]} {course[1]} information...")
    #         course[0] = course[0].replace("&", "%26")
    #         course[0] = course[0].replace("/", "%2F")
    #         all_class.update(getClassInfo(2023, "Winter", course[0], course[1]))
    #         print()

    #         # counter += 1
    #         # if counter == 6:
    #         #     break

    #     with open("all_course_info.json", "w") as fout:
    #         json.dump(all_class, fout)
    
    # course = ["CRM/LAW", "C7"]
    # course[0] = course[0].replace("&", "%26")
    # course[0] = course[0].replace("/", "%2F")
    # print(course[0])
    # print(getClassInfo(2023, "Winter", course[0], course[1]))
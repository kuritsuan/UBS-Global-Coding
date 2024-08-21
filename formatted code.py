import pandas as pd
import math
import json

#read and import json input data
with open("input.json", "r") as f:
    data = json.load(f)


#create empty list to input
schoolName = []
schoolLocation = []
schoolMax = []

schoolInfo = [schoolName, schoolLocation, schoolMax]

studentID = []
studentLocation = []
studentAlumni = []
studentVolunteer = []

studentInfo = [studentID, studentLocation, studentAlumni, studentVolunteer]

# import the data from json to the list created
#school data entry
for school in data['school']:
    schoolName.append(school['name'])
    schoolLocation.append(school['location'])
    schoolMax.append(school['maxAllocation'])
    
#student data entry
for students in data['students']:
    studentID.append(students['id'])
    studentLocation.append(students['homeLocation'])
    studentAlumni.append(students['alumni'])
    if 'volunteer' in students:
        studentVolunteer.append(students['volunteer'] )
    else:
        studentVolunteer.append([])
        
#define all the functions
## calculate euclidian distance
def calcLocation(schoolname,studentid):
    distance = math.sqrt(((schoolLocation[schoolname][0]-studentLocation[studentid][0])**2)+((schoolLocation[schoolname][1]-studentLocation[studentid][1])**2))
    return distance

## returns the max distane of 1 school
# **GPT**
def get_max_distances(df, school_names):
    max_distances = {}
    for school in school_names:
        if school in df.columns:
            max_distances[school] = df[school].max()
        else:
            max_distances[school] = 0
    return max_distances

## calculate distance poin allocation for a certain school
def calculate_dist_points(df, school_names):
    max_distances = get_max_distances(df, school_names)
    for school in school_names:
        column_name = f"{school}_pt"
        if school in df.columns:
            df[column_name] = ((max_distances[school] - df[school]) / max_distances[school]) * 0.5
        else:
            df[column_name] = 0

    return df

## adds the volunteer and alumni poins to the distance poin
# **GPT**
def calculate_total_points(df, school_names):
    for school in school_names:
        dist_pt_col = f"{school}_pt"
        total_col = f"{school}_tot"
        df[total_col] = df.apply(lambda row: row[dist_pt_col] +
                                (0.3 if row['alum'] == school else 0) +
                                (0.2 if row['volun'] == school else 0), axis=1)

    return df
        
## accessory function for creating columns in df
def get_dist_names(school_names):
    return [f"{school}_pt" for school in school_names]

def get_total_names(school_names):
    return [f"{school}_tot" for school in school_names]

distName = get_dist_names(schoolName)
totName = get_total_names(schoolName)

# create df
df = pd.DataFrame(columns=['student_id'] + schoolName + distName + ['volun'] + ['alum'] + totName)

# fill the necessary data
for i in range(len(studentID)):
    df.at[i, 'student_id'] = studentID[i]
    df.at[i, 'alum'] = studentAlumni[i]
    df.at[i, 'volun'] = studentVolunteer[i]

# calculate location for each school
for y in range(len(df)):
    for x in range(len(schoolName)):
        a = schoolName[x]
        df.at[y, a] = calcLocation(x,y)

# use the functions defined earlier to calculate the poins of each students
df = calculate_dist_points(df, schoolName)
df = calculate_total_points(df, schoolName)

# -- until here tested and proven correct --

# create the output
school_lists = {}
for school in schoolName:
    school_lists[school] = []
    
print(school_lists)

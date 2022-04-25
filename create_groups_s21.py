import csv
import sys
import gitlab

#Original code courtesy of Caleb Huck. Modified by Anthony Palmer.
#token: acquire via GitLab (placeholder comment where you can put token so you don't lose it)

#input validation
if (len(sys.argv) != 4):
    print("Error: invalid number of arguments. Please use the following format:\n<script_name> <access_token> <parent_group_id> <file_name>")
    exit()

#access token, id of parent group, and .csv file containing students and group ids are
#supplied by the user
csv_file = sys.argv[1]
parent_id = sys.argv[2]
token = sys.argv[3]
url = 'https://gitlab.csc.tntech.edu'

delete_groups = False

#authenticate token and create gitlab object
gl = gitlab.Gitlab(url, private_token=token)

if delete_groups:
    group = gl.groups.get(parent_id)
    sub_groups = group.subgroups.list()
    for sub_group in sub_groups:
        new_group = gl.groups.get(sub_group.id)
        new_group.delete()
    exit()

students = []
num_groups = 0
#open the csv file and create a list of dictionaries containing the username and group
with open(csv_file, mode='r', encoding='utf-8-sig') as students_file:
    csv_reader = csv.reader(students_file, delimiter=',')
    for row in csv_reader:

        #determine how many groups to make
        if (int(row[1]) > num_groups):
            num_groups = int(row[1])

        #append a '0' to single digit numbers to ensure consistent format (i.e. Group-XX)
        if int(row[1]) < 10:
            student_group_id = '0' + row[1]
        else:
            student_group_id = row[1]

        #remove the '@tntech.edu' to get gitlab username
        email = row[0]
        length = len(email)
        username_length = length - 11
        username = email[:username_length]

        #add the dictionary entry containing one student to the list
        students.append({'username': username, 'group_id': student_group_id})

#create each group (if the group already exists, a message will be printed instead)
id_list = []
count = 1
while count <= num_groups:

    #ensures consistent format (i.e. Group-XX)
    if count < 10:
        id_str = '0' + str(count)
    else:
        id_str = str(count)

    group = {'name': 'Group-' + id_str, 'path': 'group-' + id_str, 'parent_id': parent_id}
    try:
        gl.groups.create(group)
    except:
        print(group['name'] + ' already exists\n')
    count+=1

#iterate through each student and determine the correct group, then attempt
#to add the user (if an error occurs, or the user is already a member, a messgae will be printed instead)
group = gl.groups.get(parent_id)
sub_groups = group.subgroups.list()
for student in students:
    for sub_group in sub_groups:
        #check the end of the sub-group name for the group number, if they match, add the user
        if sub_group.name[-2:] == student['group_id']:
            try:
                #get the actual user matching the username from gitlab API
                user = gl.users.list(username=student['username'])[0]
                current_group = gl.groups.get(sub_group.id)
                current_group.members.create({'user_id': user.id, 'access_level': gitlab.OWNER_ACCESS})
            except:
                print(student['username'] + ' was not added to ' + sub_group.name + ' (may already be a member)')

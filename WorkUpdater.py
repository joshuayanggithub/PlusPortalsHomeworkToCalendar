from todoist_api_python.api import TodoistAPI
import LoginInfo, CourseWorkRequest
import json, time,os
from datetime import datetime, timedelta

api = TodoistAPI(LoginInfo.api_key)

ospath = os.path.dirname(os.path.realpath(__file__))
filepath = ospath + '/addedtasks.json'
file = open(filepath,'r')
addedTasks = json.loads(file.read())

def dateExpired(date_str): #over a day old tasks are auto cleared from the .json file
  if (date_str == ""): #do nothing if there is no due string date given
    return False
  today =  datetime.today()
  duedate = datetime.strptime(date_str,"%Y-%m-%d")
  return  duedate.date() < today.date()
def removeExpired():
  global addedTasks
  i = len(addedTasks)-1
  while (i >= 0):
    if (dateExpired(addedTasks[i]["due"])):
      addedTasks.pop(i)
      dumpJSON()
    i -= 1
    
def checkDuplicatedTask(unique_id):
  global addedTasks
  for item in addedTasks:
    if (unique_id==item["unique_id"]):
      return True

def updateTask(json_obj):
  global addedTasks
  for i,item in enumerate(addedTasks):
    if (json_obj["unique_id"] == item["unique_id"]):
      if (json_obj["title"] != item["title"]):
        api.update_task(task_id=item["api_id"], content=taskFormat(json_obj["title"],json_obj["course"]))
        addedTasks[i]["title"] = json_obj["title"]
        print("Succesfully updated title of task: " +  addedTasks[i]["title"])
      if (json_obj["description"] != item["description"]):
        api.update_task(task_id=item["api_id"], description=json_obj["description"])
        addedTasks[i]["description"] = json_obj["description"]
        print("Succesfully updated description of task: " +  addedTasks[i]["title"])
      if (dueFormat(json_obj["due"]) != (item["due"])):
        api.update_task(task_id=item["api_id"], due_date=dueFormat(json_obj["due"]))
        addedTasks[i]["due"] = dueFormat(json_obj["due"])
        print("Succesfully updated due date of task: " +  addedTasks[i]["title"])

def createJSON(course, title, description, due, unique_id,api_id):
  json_obj = {
    'course': course,
    'title': title,
    'description': description,
    'due': due,
    'unique_id': unique_id,
    'api_id': api_id
  }
  return json_obj
def courseFormat(course):
  if (course.index("(") == -1):
    return course
  else:
    return course[0:(course.index("(")-1)]
def taskFormat(title, course):
  return (title + " - " + courseFormat(course))
def dueFormat(date): #Converting date between DD-MM-YYYY and YYYY-MM-DD
  if (date == ""):
    return ""
  if (date.lower() == "tomorrow"):
    tomorrow = datetime.today() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")
  elif (date.lower() == "today"):
    return datetime.today().strftime("%Y-%m-%d")
  else:
    l = date.split("-")
    newdate = l[2] + "-" + l[0] + "-" + l[1]
    return newdate
def idFormat(section_id, assignment_id):
  return str(section_id) + "/" + str(assignment_id)
def addTask(json_response):
  global addedTasks
  course = json_response["Class"]
  title = json_response["Title"]
  description = json_response["Description"]
  unique_id = idFormat(json_response["SectionID"], json_response["AssignmentID"])
  due = json_response["DueDate"]
  json_obj = createJSON(course, title, description, due, unique_id, None)
  if (checkDuplicatedTask(unique_id) == True):
    updateTask(json_obj)
    return
  try:
    course_formatted = courseFormat(course)
    taskstr = taskFormat(title,course)
    due_date = dueFormat(due)
    task = api.add_task(content=taskstr, description=description, due_date=due_date)
    api_id = task.id
    json_obj = createJSON(course, title, description, dueFormat(due), unique_id, api_id)
    addedTasks.append(json_obj)
    print("Successfully added new task: " + taskstr)
  except Exception as error:
    print(error)
def dumpJSON():
  with open(filepath,"w") as file:
    json.dump(addedTasks,file)

removeExpired()
try:
  counter = 0
  while True: 
    if (counter == 60): #10 hours!
      dumpJSON()
      counter = 0
    response = CourseWorkRequest.workRequest()
    for item in response.json()["dataResult"]["Data"]:
      addTask(item)
    time.sleep(600)
    counter += 1
except:
  dumpJSON()
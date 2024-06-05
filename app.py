from flask import *
from flask_session import Session
import os
import subprocess
import time

#This part is for creating the flask app and creating flask session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#This is the data structure to store information about which email id points to which dashboard
ds={}
ds['tanishkakalra0910@gmail.com']="student_dashboard.html"
ds['tanishqrawat8@gmail.com']="teacher_dashboard.html"

grades={
    'Assignment-1':'A+',
    'Assignment-2':'-1',
    'Assignment-10':'-1',
    'Assignment-4':'B'
}
ass1=False
ass4=False

assignments={}

@app.route("/reset",methods=['GET'])
def reset():
    global ass1
    global ass4
    ass1=False
    ass4=False
    print("Ass1: ",ass1)
    print("Ass4: ",ass4)
    return "Done"
@app.route("/find",methods=['POST'])
def find():
    if request.method=="POST":
        global ass1
        global ass4
        print("Ass1: ",ass1)
        print("Ass4: ",ass4)
        return {"ass1":ass1,"ass4":ass4}

#This function will fetch information about assignments and will store in assignments dictionary
def loadAssignments():
    print("Loading assignments")
    with open('ass.json','r') as file:
        aa=file.read()
        if len(aa)!=0:
            c=json.loads(aa)
        else:
            c={}
    if len(c)==0: return
    for i in c['ass']:
        assignments[i]=c['ass'][i]

loadAssignments()



students=[]
data={"tanishqrawat8@gmail.com":"Tanu@091710","tanishkakalra0910@gmail.com":"Tanu@091710"}
def loadStudentsData():
    for file in os.listdir("students"):
        with open(f"students/{file}",'r') as stFile:
            a=json.load(stFile)
        students.append({file[0:-5]:a['id']})
    print(students)
loadStudentsData()


@app.route("/")
def index():
    if not session.get("name"): return redirect("/login")
    return render_template(ds[session.get("name")],name=session.get("name"))

@app.route("/studentDashboard")
def studentDashboard():
    nm=session.get("name")
    for i in students:
        if i[nm]!=None:
            id=i[nm]
    return render_template('student_dashboard.html',name=nm)

@app.route("/teacherDashboard")
def teacherDashboard():
    return render_template('teacher_dashboard.html',name=session.get("name"))

@app.route("/login")
def login():
    return render_template("pages-login.html")

@app.route("/logout")
def logout():
	session["name"] = None
	return redirect("/")


@app.route("/auth",methods=["POST"])
def auth():
    if request.method=="POST":
        user=request.form['user']
        pwd=request.form['pass']
        forwhom=request.form['whom']
        print(forwhom)
        if data[user]!=pwd:
            return "-1"
        session["name"] = user
        return "/"+forwhom.lower()+"Dashboard"


@app.route("/assignments")
def showAllAssignments():
    return render_template("assignmentList.html")

@app.route("/getAssignments",methods=['POST'])
def getAssignments():
    ans={}
    '''
        ans={
            "data":[
            
            ]
        }
    '''
    ans['data']=[]
    for i in assignments:
        ans['data'].append({
            'name':i,
            'len':len(assignments[i])
        })
    return ans


@app.route("/st_assignments")
def redirect_st_assignments():
    return render_template("st_assignment.html")


@app.route("/saveAssignment",methods=['POST'])
def saveAss():
    if request.method=="POST":
        sz=int(request.form['size'])
        questions=[]
        assName=request.form['assName']
        if assignments.get(assName)!=None:
            return "-1"
        for i in range(sz):
            questions.append({
                'name':request.form[f'ques{i}'],
                'prompt':request.form[f'quesP{i}'],
                'input':request.files[f'inp{i}'].filename,
                'output':request.files[f'out{i}'].filename,
            })
            inputFile=request.files[f'inp{i}']
            inputFile.save(f'inputs/{inputFile.filename}')
            outputFile=request.files[f'out{i}']
            outputFile.save(f'outputs/{outputFile.filename}')
        assignments[assName]=questions
        print(assignments)
        updateAssJson(assName,questions)
    return "Assignment Successfully Submitted"

@app.route("/getData",methods=['POST'])
def getData():
    user=session.get('name')
    return user


@app.route("/getStudentAssignments",methods=['POST'])
def getStudentAssignments():
    if request.method=="POST":
        user=request.form['user']
        with(open(f'students/{user}.json','r')) as f:
            d=json.load(f)
        print({"pending":d['assignmentsPending'],"done":d['assignmentsDone']})
        return {"pending":d['assignmentsPending'],"done":d['assignmentsDone']}


@app.route("/showAssignment")
def showAssignment():
    return render_template("showAssignment.html",assName=request.args.get('assignment'))

def updateAssJson(assName,questions):
    with open('ass.json','r') as file:
        aa=file.read()
        if len(aa)!=0:
            data=json.loads(aa)
        else:
            data={}
    print(type(assignments))
    data['ass']=assignments
    with open("ass.json", "w") as f:
        json.dump(data, f)
    updateStudents(assName,questions)

def updateStudents(assName,questions):
    for i in students:
        for key in i:
            with open(f'students/{key}.json','r') as f:
                d=json.load(f)
                print(d)
            d['assignmentsPending'].append({'name':assName,'questions':questions})
            print("After")
            print(d)
            with open(f'students/{key}.json', "w") as f:
                json.dump(d, f)
    return

@app.route("/getAssData",methods=['POST'])
def getAssData():
    if request.method=="POST":
        assName=request.form['assName']
        return {"questions":assignments[assName]}


@app.route("/giveQuestionData",methods=['POST'])
def giveQuestionData():
    if request.method=="POST":
        assName=request.form['assName']
        qnm=request.form['qnm']
        data=None
        for i in assignments[assName]:
            if i['name']==qnm:
                data=i
                break
        return {'questionPrompt':data['prompt']}


@app.route("/submitAssignment",methods=['POST'])
def submitAssignment():
    if request.method=="POST":
        print(request.form)
        print(request.files['file'])
        fName=request.files['file'].filename
        request.files['file'].save(f'zips/{fName}')
        assName=fName.split('_')[0]
        sid=fName.split('_')[1]
        status=processAssignment(assName,sid,fName)
        if fName=="Assignment-1_101.zip":
            addToDone(sid,assName)
            global ass1
            ass1=True
            print("Ass1: ",ass1)
            return "Assignment submitted successfully, Your grades A+ (2/2)"
        if fName=="Assignment-2_101.zip":
            return "Failed to submit assignment, Remarks-: Incomplete (0/1)"
        if fName=="Assignment-4_101.zip":
            global ass4
            ass4=True
            print("Ass4: ",ass4)
            addToDone(sid,assName)
            return "Assignment submitted successfully, Your grades B+ (0.75/1)"
        else:
            return "Failed to submit assignment, Remarks-: Incomplete (0/1)"
    

def addToDone(sid,assName):
    with open('students/tanishkakalra0910@gmail.com.json','r') as rf:
        data=json.load(rf)
    for i in range(len(data['assignmentsPending'])):
        if data['assignmentsPending'][i]['name']==assName:
            index=i 
            print(index)
    if index!=None:
        data['assignmentsDone'].append(data['assignmentsPending'][index])
        data['assignmentsPending'].remove(data['assignmentsPending'][index])
        with open('students/tanishkakalra0910@gmail.com.json','w') as wf:
                json.dump(data,wf)

def processAssignment(assName,sid,fName):
    details=assignments.get(assName)
    if details==None:
        return -1
    subprocess.run(["unzip",f"zips/{fName}"])
    time.sleep(1)
    for file in os.listdir(f"{fName[0:-4]}"):
        pass

@app.route("/showResult")
def showResult():
    return render_template("viewResult.html")

if __name__ == '__main__':
    app.run(debug = True)

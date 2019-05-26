import uuid
from flask import Flask,request,render_template,redirect,url_for,flash,abort,jsonify
import hashlib

from celery import Celery
from lib.core.baidu import BaiduApi
from lib.core.webapi import UBW_Scan
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, PasswordField,TextAreaField
from wtforms.validators import DataRequired
import pymongo
from flask_mongoengine import MongoEngine
import os
from datetime import datetime
from lib.utils.cmsdata import cms_dict
NowPath=os.path.abspath(os.path.dirname(__file__))
ScriptPath=NowPath+'/script/'
app=Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': '127.0.0.1',
    'port': 27017
}

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
db=MongoEngine(app)
bootstrap=Bootstrap(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
conn = pymongo.MongoClient('127.0.0.1', 27017, socketTimeoutMS=3000)





class ScanTask(db.Document):
    meta={
        'collection':'scan_result',
        'ordering': ['-create_at'],
        'strict': False,
    }
    url=db.StringField()
    pocname=db.StringField()
    result=db.StringField()
    create_time = db.DateTimeField(default=datetime.now)
    is_completed = db.BooleanField(default=False)

class CmsData(db.Document):
    meta={
        'collection':'cms',
        'ordering': ['-create_at'],
        'strict': False,
    }
    cmsname=db.StringField()
    finger=db.StringField()
    hash=db.StringField()
    create_time = db.DateTimeField(default=datetime.now)
    
class ScanForm(Form):
    target = StringField('target', validators=[DataRequired()])
    pocname = StringField('pocname', validators=[DataRequired()])
    submit = SubmitField()

class CmsForm(Form):
    cmsname = StringField('cmsname', validators=[DataRequired()])
    finger = StringField('finger', validators=[DataRequired()])
    submit = SubmitField()
class PocForm(Form):
    product=StringField('product', validators=[DataRequired()])
    vultype=StringField('vultype', validators=[DataRequired()])
    code=TextAreaField('code',validators=[DataRequired()],default='''
import pymongo
def poc(target):
    ip=target
    port=27017
    try:
        conn = pymongo.MongoClient(ip, port, socketTimeoutMS=3000)
        dbs = conn.database_names()
        return 'dbsname' + ' -> ' + '|'.join(dbs) if dbs else False
    except Exception as e:
        return False
''')
    submit = SubmitField()

class TaskDeliver(object):
    def __init__(self,url,pocname,result,createtime=None,is_completed=False):
        self.url=url
        self.pocname=pocname
        self.result=result
        self.createtime=createtime
        self.is_completed=is_completed
class PocDeliver(object):
    def __init__(self,filename,product,vultype):
        self.filename=filename
        self.product=product
        self.vultype=vultype

class CmsDeliver(object):
    def __init__(self,cmsname,finger,hash):
        self.cmsname=cmsname
        self.finger=finger
        self.hash=hash

# @celery.task
# def Baidu_Api(query,num):
#     baidu=BaiduApi(query,num)
#     list1=baidu.run()
def Init_CMS():
    if CmsData.objects().all().count()>0:
        return
    else:
        for cmsname in cms_dict:
            for finger in cms_dict[cmsname]:
                for i in finger:
                    cms = CmsData(cmsname, i, str(getMD5(i))).save()
def getMD5(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()

@celery.task
def New_UBW_Task(target,pocname):
    ubw=UBW_Scan(target,pocname)
    ubw.scan()

@app.route('/index')
def hello():
    success_task_num=0
    tasks=ScanTask.objects.all()
    for i in tasks:
        if i.result:
            success_task_num=success_task_num+1
    cmss=CmsData.objects.all()
    pocs=[i.split('.')[0] for i in os.listdir(ScriptPath)]
    return render_template('index.html',task_num=len(tasks),cms_num=len(cmss),poc_num=len(pocs),success_task_num=success_task_num)
@app.route('/newscan',methods=['POST','GET'])
def createtask():
    form=ScanForm(csrf_enabled=False)
    if form.validate_on_submit():
        target=request.form['target']
        pocname=request.form['pocname']
        New_UBW_Task.delay(target,pocname)
        return redirect(url_for('showtask'))
    return render_template('scan.html',form=form)

@app.route('/newpoc',methods=['POST','GET'])
def createpoc():
    form=PocForm(csrf_enabled=False)
    if form.validate_on_submit():
        product=request.form['product']
        vultype=request.form['vultype']
        code=request.form['code']
        pocname=product+'_'+vultype
        fp = open(ScriptPath+pocname+'.py','w')
        fp.writelines(code)
        fp.close()   
        return redirect(url_for('showtask'))
    return render_template('poc.html',form=form)

@app.route('/pocshow')
def showpoc():
    poc_list=[]
    filenames=[i.split('.')[0] for i in os.listdir(ScriptPath)]
    for i in filenames:
        try:
            poc=PocDeliver(i,i.split('_')[0],i.split('_')[1])
            poc_list.append(poc)
        except:
            poc=PocDeliver(i,'','')
            poc_list.append(poc)
    return render_template('poccenter.html',pocs=poc_list)

@app.route('/cmsshow')
def showcms():
    page = request.args.get('page', 1, type=int)
    pagination = CmsData.objects.paginate(page=page, per_page=50)
    return render_template('cmscenter.html',pagination=pagination)

@app.route('/newcms',methods=['POST','GET'])
def createcms():
    form=CmsForm(csrf_enabled=False)
    if form.validate_on_submit():
        cmsname=request.form['cmsname']
        finger=request.form['finger']
        fingerhash=getMD5(finger)
        cms = CmsData(cmsname, finger, str(fingerhash)).save()
        return redirect(url_for('showcms'))
    return render_template('cms.html',form=form)
@app.route('/scanshow')
def showtask():
    page = request.args.get('page', 1, type=int)
    pagination = ScanTask.objects.paginate(page=page, per_page=10)
    return render_template('taskcenter.html',pagination=pagination)

Init_CMS()


if __name__=='__name__':
    app.run(debug=True)

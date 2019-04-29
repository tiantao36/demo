from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from app01.utils import *
# Create your views here.
import json
from django.utils.safestring import mark_safe

from app01.utils.pagination import Page

from threading import  Thread
def editdate(host,input_date_time,data):
    if host.host_type == 1:
        editdate_status =linuxeditdate.handler(host.ipaddr, host.port, host.username, host.password, input_date_time)
    else:
        editdate_status = wineditdate.handler(host.ipaddr, host.username, host.password, input_date_time)
    if editdate_status:
         pass
    else:
        data.append({host.ipaddr:editdate_status})

# def getdate(host,data):
#     if host.host_type == 1:
#         getdate_result = linuxgetdate.handler(host.ipaddr, host.port, host.username, host.password)
#     else:
#         getdate_result = 'windows获取失败'
#     if getdate_result:
#         data.append({host.id: [host.ipaddr, getdate_result.strip()]})
#     else:
#         data.append({host.id: [host.ipaddr, 'linux获取失败']})

def getdate(host,data):
    if host.host_type == 1:
        getdate_result = linuxgetdate.handler(host.ipaddr, host.port, host.username, host.password)
    else:
        getdate_result = wingetdate.handler(host.ipaddr, host.username, host.password)
    if getdate_result:
        data.append({host.id: [host.ipaddr, getdate_result]})
    elif host.host_type == 1 and not getdate_result:
        data.append({host.id: [host.ipaddr, 'linux获取失败']})
    else:
        data.append({host.id: [host.ipaddr, 'window获取失败']})
def tcdm(requests):
    group_obj=models.Hgroup.objects.values('title')
    data_list=[]
    for group in group_obj:
        title=group.get('title')
        dict_tmp={title:models.Host.objects.filter(system_env__title=title).all()}
        data_list.append(dict_tmp)
    return  render(requests,'test/cmd.html',context={'data_list':data_list})


# import copy
# def tcdm(requests):
#     group_obj=models.Hgroup.objects.values('title')
#     data_list=[]
#     for group in group_obj:
#         title=group.get('title')
#         data = []
#         concurrent_task = []
#         tmp=models.Host.objects.filter(system_env__title=title).all()
#         for host in tmp:
#             t = Thread(target=getdate, args=(host,data))
#             concurrent_task.append(t)
#             t.start()
#         for t in concurrent_task:
#             t.join()
#         result_data=copy.deepcopy(data)
#         # dict_tmp={title:models.Host.objects.filter(system_env__title=title).all().values('id','ipaddr')}  #环境和主机的一个组关系
#         dict_tmp={title:result_data}  #环境和主机的一个组关系
#
#         data_list.append(dict_tmp)
#     print(data_list)
#     return  render(requests,'test/cmd2.html',context={'data_list':data_list})

def hadd(requests):
    #改成ajax提交
    ipaddr=requests.POST.get('ipaddr')
    username=requests.POST.get('username')
    password=requests.POST.get('password')
    port=requests.POST.get('port')
    system_env=requests.POST.get('system_env')
    host_type=requests.POST.get('host_type')

    if ipaddr and username and password and port and system_env and host_type:
        models.Host.objects.create(ipaddr=ipaddr,username=username,password=password,port=port,system_env_id=system_env,host_type=host_type)
        return redirect('/host.html')
    else:
        return HttpResponse('提交失败')

def hdelete(requests,id):
    models.Host.objects.filter(id=id).delete()
    return redirect('/host.html')


def gdelete(requests,id):
    models.Hgroup.objects.filter(id=id).delete()
    return redirect('/envset.html')


def task(requests):
    input_date_time=requests.POST.get('input_date_time')
    task_id_list=requests.POST.get('task_id_list')
    system_env_name=requests.POST.get('system_env_name')

    print(input_date_time)


    task_id_list=task_id_list.strip('-').split('-')
    data=[]
    concurrent_task=[]
    for host in models.Host.objects.filter(id__in=task_id_list):
        t=Thread(target=editdate,args=(host,input_date_time,data))
        concurrent_task.append(t)
        t.start()
    for t in concurrent_task:
        t.join()
    html='''
		<tr>
			<td>{0}</td>
			<td>{1}</td>
		</tr>
    '''
    tmp=''
    if data:
        for item in data:
            for ip in item.keys():
                tmp=ip+'<br/>'+tmp
    else:
        tmp='成功'
    html = '''
        <tr>
            <td>{0}</td>
            <td>{1}</td>
        </tr>
    '''.format(system_env_name,tmp)
    return HttpResponse(json.dumps(mark_safe(html)))


def check(requests):
    task_id_list=requests.POST.get('task_id_list')
    task_id_list=task_id_list.strip('-').split('-')

    data = []
    concurrent_task = []
    for host in models.Host.objects.filter(id__in=task_id_list):
        t = Thread(target=getdate, args=(host,data))
        concurrent_task.append(t)
        t.start()
    for t in concurrent_task:
        t.join()
    result_data=json.dumps(data, ensure_ascii=False)
    print(result_data)
    return HttpResponse(result_data)


def gadd(requstst):
    title=requstst.POST.get('title')
    if title:
        models.Hgroup.objects.create(title=title)
        return redirect('/envset.html')
    else:
        return HttpResponse('提交失败')


def tenvset(requests):
    current_page = int(requests.GET.get('current_page',1))
    all_count = models.Hgroup.objects.all().count()
    # page_obj = Page(current_page,all_count,'/hosts.html')
    page_obj = Page(current_page,all_count,requests.path_info)

    hgroup_obj = models.Hgroup.objects.all()[page_obj.start:page_obj.end]
    page_str = page_obj.page_html()

    return render(requests,'test/envset.html',context={'hgroup_obj':hgroup_obj,'page_str':page_str})


def thost(requests):
    exclude=['ID','password']  #排除某个filed
    #添加删除按钮
    title_obj=[f.verbose_name for f in models.Host._meta.fields if f.verbose_name not in exclude]
    title_obj.append('操作')
    hgroup_obj=models.Hgroup.objects.all()

    current_page = int(requests.GET.get('current_page',1))
    all_count = models.Host.objects.all().count()
    # page_obj = Page(current_page,all_count,'/hosts.html')
    page_obj = Page(current_page,all_count,requests.path_info)

    data_obj = models.Host.objects.all()[page_obj.start:page_obj.end]
    page_str = page_obj.page_html()

    return render(requests,'test/host.html',context={'hgroup_obj':hgroup_obj,'title_obj':title_obj,'data_obj':data_obj,'page_str':page_str})

def tsearch(requests):
    search_group_name=requests.POST.get('search_group_name')
    if search_group_name:
        group_obj=models.Hgroup.objects.filter(title__icontains=search_group_name).values('title')
    else:
        group_obj =group_obj=models.Hgroup.objects.values('title')
    data_list=[]
    for group in group_obj:
        title=group.get('title')
        dict_tmp={title:models.Host.objects.filter(system_env__title=title).all()}
        data_list.append(dict_tmp)
    return  render(requests,'test/cmd.html',context={'data_list':data_list})

def help(requests):
    return render(requests, 'test/help.html')

def login(requests):
    if requests.method=="GET":
        return render(requests,'login.html')
    else:
        username=requests.POST.get('username')
        password=requests.POST.get('password')
        if username and password:
            print('@@@@@@@@@@@@@@@@@')
            print(pasmd5.encrypt(password),password)
            obj=models.UserInfo.objects.filter(username=username,password=pasmd5.encrypt(password)).first()
            print('@@@@@@@@@@@@@@@@',obj)
            if obj:
                requests.session['username']=username
                requests.session['role']=obj.role
                return redirect('/')
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')


def logout(request):
    del request.session['username']
    return redirect('/login/')

def changpas(request):
    password_1=request.POST.get('password_1')
    password_2=request.POST.get('password_2')
    username=request.session.get('username')
    if password_1 and password_2 and password_1==password_2:
        models.UserInfo.objects.filter(username=username).update(password=pasmd5.encrypt(password_1))
    return redirect('/')


def formatdata(requests):
    obj_dict=models.Host.objects.values('ipaddr')
    for ip in obj_dict:
        ipaddr=ip['ipaddr'].replace('14','168')
        models.Host.objects.filter(**ip).update(ipaddr=ipaddr)

    return HttpResponse('ok')
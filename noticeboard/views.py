from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from digitalnoticeboard.utils.utils import base64ofsha
from .models import User, Posts, Department


def login(request):
    username = request.session.get("username")
    department = request.session.get("department")
    if username is not None and department is not None:
        return redirect('panel')

    if request.method == "GET":
        return render(request, 'noticeboard/login.html')
    elif request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST["password"]
            hashed = base64ofsha(password)

            rec = User.objects.filter(email=username, password=hashed)
            if len(rec) == 1:
                if rec[0].is_approved == False:
                    return render(request, 'noticeboard/login.html', {
                        "error": "Your account is not approved. Please contact concerned authority for approval"})
                rec = rec[0]
                request.session["department"] = rec.department.department_name
                request.session["username"] = username
                return redirect('panel')
            else:
                return render(request, 'noticeboard/login.html', {"error": "Email / password does not match"})
        except IndexError:
            return HttpResponse("Invalid Request")


def panel(request):
    username = request.session.get("username")
    department = request.session.get("department")
    if request.method == "GET" and username is not None and department is not None:
        user = User.objects.filter(email=username)[0]
        posts = Posts.objects.filter(department=user.department)
        if len(posts) == 0:
            return render(request, 'noticeboard/feed.html', {"posts": posts, "noposts": True})
        return render(request, 'noticeboard/feed.html', {"posts": posts})
    elif request.method == "POST" and username is not None and department is not None:
        s = getSessionDetails(request)
        if s[0]:
            try:
                user = User.objects.filter(email=username)[0]
                department = Department.objects.filter(department_id=user.department)[0]
                title = request.POST["post-title"]
                notice_text = request.POST["notice"]
                user = User.objects.filter(email=s[1])[0]
                p = Posts(title=title, notice_text=notice_text, user=user, department=department)
                p.save()
                return redirect('panel')
            except IndexError:
                return JsonResponse({"status": "failed", "message": "There was some error while posting the notice"})
    else:
        return redirect('login')


def privacy(request):
    return render(request, 'noticeboard/privacy.html')


def settings(request):
    username = request.session.get("username")
    department = request.session.get("department")

    if request.method == "GET" and username is not None and department is not None:
        u = User.objects.filter(email=username)[0]

        return render(request, 'noticeboard/profile.html',
                      context={"name": u.name, "email": u.email, "designation": u.designation,
                               "department": u.department.department_name, "is_admin": u.is_admin})
    else:
        return redirect('login')


def getSessionDetails(request):
    username = request.session.get("username")
    department = request.session.get("department")
    if username is not None and department is not None:
        return (True, username, department)
    else:
        return (False,)


def registerUser(request):
    departments = Department.objects.all()
    if request.method == "GET":

        return render(request, 'noticeboard/register.html', {"departments": departments})
    elif request.method == "POST":
        try:
            name = request.POST["name"]
            designation = request.POST['designation']
            department = Department.objects.filter(department_id=request.POST['department'])[0]
            email = request.POST['email']
            password = request.POST["password"]

            user = User(name=name, designation=designation,
                        department=department,
                        email=email,
                        password=base64ofsha(password))
            user.save(force_insert=True)
            return render(request, 'noticeboard/register.html',
                          {"type": "success", "message": "Registration Successful", "departments": departments})
        except MultiValueDictKeyError:
            return render(request, 'noticeboard/register.html',
                          {"type": "error", "message": "Please provide all the paramters for registration",
                           "departments": departments})


def approve(request):
    username = request.session.get('username')
    department = request.session.get('department')
    if request.method == "GET" and username is not None and department is not None:
        users = User.objects.filter(is_approved=False)
        admin = User.objects.filter(email=username)[0]
        if not admin.is_admin:
            return render(request, 'noticeboard/approval.html',
                          {"users": [], "message": "Sorry you cannot approve users. Please contact the admin"})
        if len(users) == 0:
            return render(request, 'noticeboard/approval.html',
                          {"users": users, "message": "No users pending for approval"})

        return render(request, 'noticeboard/approval.html', {"users": users})
    elif request.method == "POST" and username is not None and department is not None:
        user = User.objects.filter(email=request.POST["username"])[0]
        user.is_approved = True
        user.save(force_update=True)
        return redirect('approve')
    else:
        return redirect('login')


def logout(request):
    try:
        del request.session['username']
        del request.session["department"]
    except:
        return redirect('login')
    return redirect('login')


def post(request):
    username = request.session.get('username')
    department = request.session.get('department')
    if request.method == "POST" and username is not None and department is not None:
        post_id = request.POST["post_id"]
        req_type = request.POST["req_type"]
        if req_type == 'delete':
            post = Posts.objects.filter(id=post_id)[0]
            post.delete()
            return redirect('panel')
        elif req_type == 'edit':
            post = Posts.objects.filter(id=post_id)[0]
            content_new = request.POST["content"]
            post.notice_text = content_new
            post.save(force_update=True)
            return redirect('panel')
        else:
            return redirect('panel')
    else:
        return redirect('panel')


def posts(request):
    s = getSessionDetails(request)
    if request.method == "GET":
        pass
    elif request.method == 'POST':
        email = request.POST["email"]
        user = User.objects.filter(email=email)[0]
        department = Department.objects.filter(department_id=s[1])[0]
        posts = Posts.objects.filter(department=department)
        return render()
    else:
        return JsonResponse({"status": "failed", "message": "Operation not permitted"})


def change_password(request):
    username = request.session.get("username")
    department = request.session.get("department")
    if request.method == "GET" and username is not None and department is not None:
        return redirect('profile')
    elif request.method == "POST" and username is not None and department is not None:
        user = User.objects.filter(email=username)[0]
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        if user.password == base64ofsha(current_password):
            user.password = base64ofsha(new_password)
            user.save(force_update=True)
            return redirect('profile')
        else:
            return render(request, 'noticeboard/profile.html',
                          {"name": user.name, "email": user.email, "designation": user.designation,
                           "department": user.department.department_name, "is_admin": user.is_admin,
                           "message": "Previous password does not match"})
    else:
        return redirect('logout')

def board(request):
    if request.method == "GET":
        posts = Posts.objects.order_by('-id')[:10]
        print(posts)
        context= {"posts":posts,"temperature":"32 C","humidity":"60%","smoke":"0ppm"}
        if request.GET["type"]=="json":
            posts_list = []
            for p in posts :
                posts_list.append({"title":p.title,"post_text":p.notice_text})
            context["posts"]=posts_list
            return JsonResponse(context)
        return render(request,'noticeboard/board.html',context=context)
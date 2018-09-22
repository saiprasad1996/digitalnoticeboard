from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from digitalnoticeboard.utils.utils import base64ofsha
from .models import User, Posts, Department


def login(request):
    username = request.session.get("username")
    name = request.session.get("name")
    if username is not None and name is not None:
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
                request.session["name"] = rec.name
                request.session["username"] = username
                return redirect('panel')
            else:
                return render(request, 'noticeboard/login.html', {"error": "Email / password does not match"})
        except IndexError:
            return HttpResponse("Invalid Request")


def panel(request):
    username = request.session.get("username")
    name = request.session.get("name")
    if request.method == "GET" and username is not None and name is not None:
        return render(request, 'noticeboard/feed.html')
    else:
        return redirect('login')


def privacy(request):
    return render(request, 'noticeboard/privacy.html')


def settings(request):
    username = request.session.get("username")
    name = request.session.get("name")

    if request.method == "GET" and username is not None and name is not None:
        u = User.objects.filter(email=username)[0]

        return render(request, 'noticeboard/profile.html',
                      context={"name": u.name, "email": u.email, "designation": u.designation,
                               "department": u.department.department_name, "is_admin": u.is_admin})
    else:
        return redirect('login')


def getSessionDetails(request):
    username = request.session.get("username")
    name = request.session.get("name")
    if username is not None and name is not None:
        return (True, username, name)
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
                        password=password)
            user.save(force_insert=True)
            return render(request, 'noticeboard/register.html',
                          {"type": "success", "message": "Registration Successful", "departments": departments})
        except MultiValueDictKeyError:
            return render(request, 'noticeboard/register.html',
                          {"type": "error", "message": "Please provide all the paramters for registration",
                           "departments": departments})


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('login')


@csrf_exempt
def post(request):
    if request.method == "GET":
        return JsonResponse({"status": "failed", "message": "Operation not permitted"})
    elif request.method == "POST":
        s = getSessionDetails(request)
        if s[0]:
            try:
                department = Department.objects.filter(request.POST["department"])[0]
                title = request.POST["title"]
                notice_text = request.POST["notice"]
                user = User.objects.filter(email=s[1])[0]
                p = Posts(title=title, notice_text=notice_text, user=user, department=department)
                p.save()
                return JsonResponse({"status": "success", "message": "Notice posted successfully"})
            except IndexError:
                return JsonResponse({"status": "failed", "message": "There was some error while posting the notice"})
    else:
        return JsonResponse({"status": "failed", "message": "Operation not permitted"})


def posts(request):
    s = getSessionDetails(request)
    if request.method == "GET":
        pass
    elif request.method == 'POST':
        email = request.POST["email"]
        user = User.objects.filter(email=email)[0]
        Posts.objects.filter()
    else:
        return JsonResponse({"status": "failed", "message": "Operation not permitted"})

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_user, logout
from django.contrib import messages
from django.db.models import Sum

from .decorators import unauthenticated_user,allowed_users
from .forms import SignupForm,SubjectForm,StudentForm,ProfessorForm,ProfessorStudentForm,CreateUserForm
from .models import Predmet,Korisnik,Upis
from .auth import EmailBackend

@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
        else:
            messages.error(request, "Korisnik vec postoji ili se šifre ne podudaraju")
            
    else:
        form = SignupForm()

    return render(request, 'base/signup.html',{
        'form': form
    })

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Korisnik.objects.get(email=email)
        except:
            messages.error(request, "User doesn't exist")
    
        user = EmailBackend().authenticate(request, email=email, password=password)

        if user is not None:
            auth_user(request, user)
            
            if user.role == 'adm':
                return redirect('admin_page')
            elif user.role == 'prof':
                return redirect('professor')
            else:
                return redirect('home')
                
        else:
            messages.error(request, "Username or password doesn't exist")

    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

# ADMIN PAGE

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def admin(request):
    users = Korisnik.objects.all()

    return render(request, 'base/admin_page.html',{
        'users':users
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def addUser(request):

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/admin_page/')
        else:
            return HttpResponse("Nesto je poslo po krivu",status=400)
    else:
        form = CreateUserForm()

    return render(request, 'base/admin/user/user_form.html',{
        'form':form
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def editUser(request,pk):
    user = Korisnik.objects.get(id=pk)
    form = CreateUserForm(instance=user)

    if request.method == 'POST':
        form = CreateUserForm(request.POST,instance=user)

        if form.is_valid():
            form.save()
            return redirect('/admin_page/')
        else:
            return HttpResponse("Ne možemo urediti korisnika")

    return render(request, 'base/admin/user/user_form_update.html', {
        'form': form
    })



@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def subject(request):
    subjects = Predmet.objects.all()

    return render(request, 'base/admin/subject/subject.html', {
        'subjects': subjects,
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def subject_detail(request,pk):
    subject = Predmet.objects.get(id=pk)

    upis = Upis.objects.filter(predmet_id=pk).values_list('korisnik_id')

    studenti = Korisnik.objects.filter(role='stu',id__in=upis)

    return render(request,'base/admin/subject/subject_detail.html',{
        'subject':subject,
        'studenti': studenti
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def createSubject(request):
    if request.method == 'POST':

        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin_page/subject/')
        else:
            return HttpResponse("Ne možemo kreirati predmet")
    else:
        form = SubjectForm()

    return render(request, 'base/admin/subject/subject_form.html', {
        'form': form
    }) 

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateSubject(request,pk):
    subject = Predmet.objects.get(id=pk)
    form = SubjectForm(instance=subject)

    if request.method == 'POST':
        form = SubjectForm(request.POST,instance=subject)

        if form.is_valid():
            form.save()
            return redirect('/admin_page/subject/')
        else:
            return HttpResponse("Ne možemo urediti predmet")

    return render(request, 'base/admin/subject/subject_form.html', {
        'form': form
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteSubject(request,pk):

    subject = Predmet.objects.get(id=pk)

    if request.method == 'POST':
        subject.delete()
        return redirect('/admin_page/subject/')

    return render(request, 'base/delete.html', {
        'obj': subject
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def student(request):
    students = Korisnik.objects.filter(role='stu')

    return render(request, 'base/admin/student/student.html', {
        'students': students
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateStudent(request,pk):
    student = Korisnik.objects.get(id=pk)

    form = StudentForm(instance=student)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('/admin_page/student/') 
        else:
            return HttpResponse("Ne možemo urediti studenta")

    return render(request, 'base/admin/student/student_form.html', {
        'form': form
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteStudent(request,pk):
    student = Korisnik.objects.get(id=pk)

    if request.method == 'POST':
        student.delete()
        return redirect('/admin_page/student/')

    return render(request, 'base/delete.html', {
        'obj': student
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def professor(request):
    professors = Korisnik.objects.filter(role='prof')

    return render(request, 'base/admin/professor/professor.html',{
        'professors':professors
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def updateProfessor(request,pk):
    professor = Korisnik.objects.get(id=pk)

    form = ProfessorForm(instance=professor)

    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)

        if form.is_valid():
            form.save()
            return redirect('/admin_page/professor')
        else:
            return HttpResponse("Ne možemo urediti profesora")

    return render(request, 'base/admin/professor/professor_form.html',{
        'form':form
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteProfessor(request,pk):
    professor = Korisnik.objects.get(id=pk)

    if request.method == 'POST':
        professor.delete()
        return redirect('/admin_page/professor/')

    return render(request, 'base/delete.html',{
        'obj':professor
    })

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def upisi(request):
    predmeti = Predmet.objects.all()
    upisi = Upis.objects.all()

    upisi_po_predmetu = {}

    for predmet in predmeti:
        upisi_po_predmetu[predmet.ime] = []

    for upis in upisi:
        for predmet in predmeti:
            if upis.predmet_id.ime == predmet.ime:
                upisi_po_predmetu[upis.predmet_id.ime].append(upis)

    return render(request, 'base/admin/upis/upisi.html',{
        'upisi':upisi_po_predmetu
    })


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def deleteUpis(request,pk):
    upis = Upis.objects.get(id=pk)

    if request.method == 'POST':
        upis.delete()
        return redirect('/admin_page/upisi/')

    return render(request, 'base/delete.html',{
        'obj':upis
    })

# PROFFESOR PAGE

@login_required(login_url='/login/')
@allowed_users(allowed_roles=['professor'])
def professor_page(request):
    user = request.user

    subjects = Predmet.objects.filter(korisnik_id=user.id)

    predmeti = []

    for predmet in subjects:

        upisi_po_predmetu = []

        upisi = Upis.objects.filter(predmet_id=predmet.id)
        polozeno = Upis.objects.filter(predmet_id=predmet.id,status='pol')
        nepolozeno = Upis.objects.filter(predmet_id=predmet.id,status='potne')
        izgubljeno = Upis.objects.filter(predmet_id=predmet.id,status='izg')

        for upis in upisi:
            upisi_po_predmetu.append(upis)

        predmet_object = {predmet.ime: {'upisani': len(upisi_po_predmetu), 'polozeno': len(polozeno), 'nepolozeno': len(nepolozeno), 'izgubljeno': len(izgubljeno)}}

        predmeti.append(predmet_object)

    return render(request, 'base/professor.html',{
        'user': user,
        'predmeti': predmeti
    })

@login_required
@allowed_users(allowed_roles=['professor'])
def professor_subject(request):
    user = request.user

    subjects = Predmet.objects.filter(korisnik_id=user.id)

    return render(request, 'base/professor/professor_subject.html',{
        'subjects': subjects
    })

@login_required
@allowed_users(allowed_roles=['professor'])
def professor_students(request):

    user = request.user
    predmeti = Predmet.objects.filter(korisnik_id=user.id)
    studenti = []

    for predmet in predmeti:
        upisi = Upis.objects.filter(predmet_id=predmet.id)
        
        for upis in upisi:
            studenti.append(upis)

    return render(request, 'base/professor/professor_students.html',{
        'students':studenti
    })

@login_required
@allowed_users(allowed_roles=['professor'])
def professor_student_update(request,pk):
    upis = Upis.objects.get(id=pk)

    form = ProfessorStudentForm(instance=upis)

    if request.method == 'POST':
        form = ProfessorStudentForm(request.POST, instance=upis)

        if form.is_valid():
            form.save()
            return redirect('/professor/students')
        else:
            return HttpResponse("Ne možemo urediti studentov status")


    return render(request, 'base/professor/professor_studen_form.html',{
        'form': form
    })


# STUDENT PAGE

def home(request):
    user = request.user
    predmeti = Predmet.objects.all()
    upis = Upis.objects.filter(korisnik_id=request.user.id).values_list('predmet_id')

    polozeno = Upis.objects.filter(korisnik_id=user.id, status='pol')
    nepolozeno = Upis.objects.filter(korisnik_id=user.id, status='potne')
    izgubljeno = Upis.objects.filter(korisnik_id=user.id, status='izg')

    ukupno_bodova = Upis.objects.filter(korisnik_id=user.id).aggregate(total_points=Sum('predmet_id__bodovi'))
    ostvareno_bodova = Upis.objects.filter(korisnik_id=user.id, status='pol').aggregate(total_points=Sum('predmet_id__bodovi'))

    bodovi_uk = ukupno_bodova['total_points'] if ukupno_bodova['total_points'] is not None else 0
    bodovi_ost = ostvareno_bodova['total_points'] if ostvareno_bodova['total_points'] is not None else 0

    data = {
        'polozeno': len(polozeno),
        'nepolozeno': len(nepolozeno),
        'izgubljeno': len(izgubljeno),
        'ukupno_bodova': int(bodovi_uk),
        'ostvareno_bodova': int(bodovi_ost),
    }
    
    neupisani_predmeti = predmeti.exclude(id__in=upis)

    return render(request, 'base/home.html',{
        'predmeti': neupisani_predmeti,
        'data': data
    })

@login_required
@allowed_users(allowed_roles=['student'])
def student_subject(request):
    user = request.user

    godine = [1,2,3,4,5,6,7,8]
    predmeti_po_statusu = {godina: [] for godina in godine}

    upisani_predmeti = Upis.objects.filter(korisnik_id=user.id)

    for upis in upisani_predmeti:
        if user.status == 'izv':
            for godina in godine:
                if godina == upis.predmet_id.sem_izvanredni:
                    predmeti_po_statusu[godina].append(upis)
        else:
            for godina in godine:
                if godina == upis.predmet_id.sem_redovni:
                    predmeti_po_statusu[godina].append(upis)

    return render(request, 'base/student/subject.html',{
        'subjects': predmeti_po_statusu
    })

@login_required
@allowed_users(allowed_roles=['student'])
def subject_upis(request,pk):

    predmet = Predmet.objects.get(id=pk)
    user = request.user

    if request.method == 'POST':
        upis = Upis.objects.create(
            korisnik_id=user,
            predmet_id=predmet
        )

        return redirect('home')



    return render(request, 'base/student/subject_upis.html',{
        'obj': predmet
    })
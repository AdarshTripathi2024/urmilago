from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from myadmin.models import MyAdmin, Blog
from urmilafoundation.models import Join, Contact
from django.contrib import messages
from .forms import AdminRegisterForm
from django.http import JsonResponse
from django.core.paginator import Paginator
import os
from django.views.decorators.cache import never_cache

# Create your views here.
def admin_login(request):
    if request.method=="POST":
       username = request.POST.get('username')
       password = request.POST.get('password')
       user=authenticate(request, username=username,password=password)
       if user is not None:
         login(request,user)
         return redirect("admin-dashboard")
       else:
         return render(request,"myadmin/login.html")
    return render(request,'myadmin/login.html')

@never_cache
@login_required(login_url='login')
def contact_list(request):
   contact = Contact.objects.all().order_by('id')
   paginator = Paginator(contact,5)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   return render(request,"myadmin/contact-list.html",{'page_obj': page_obj})

@never_cache
@login_required(login_url='login')
def volunteer_list(request):
   v=Join.objects.all().order_by('id')
   paginator = Paginator(v,5)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   return render(request,"myadmin/join-list.html",{'page_obj': page_obj})

@never_cache
@login_required(login_url='login')
def dashboard(request):
   return render(request,"myadmin/dashboard.html")

@never_cache
@login_required(login_url='login')
def admin_logout(request):
   logout(request)
   login_url = reverse('login')
   return redirect(f'{login_url}?message=logged_out')


def admin_register(request):
   if MyAdmin.objects.exists():
      return render(request,'myadmin/login.html')
   if request.method=='POST':
      form= AdminRegisterForm(request.POST)
      if form.is_valid():
         name=form.cleaned_data['username']
         plain_password= form.cleaned_data['password']
         admin = MyAdmin(username=name,role='admin',plain_password=plain_password)
         admin.set_password(plain_password)
         admin.save()
         return redirect('login')
   else:
      form = AdminRegisterForm()

   return render(request,'myadmin/register.html',{'form':form})

@never_cache
@login_required
def upload_blog(request):
   if request.method=="POST":
      title = request.POST.get('title')
      type = request.POST.get('type')
      first = request.POST.get('first')
      second = request.POST.get('second')
      conclusion = request.POST.get('conclusion')
      image= request.FILES.get('image')
      errors = {}

      if not title:
         errors['title'] = "Title field is required"

      if type not in ['Social','Educational']:
         errors['type'] = "Select a valid Type"

      if not image:
         errors['image'] = "Upload a valid image file"

      if not conclusion:
         errors['conclusion'] = "This field is required"

      if errors:
         return JsonResponse({'status': 'error', 'errors': errors})

      Blog.objects.create(title=title, type=type, first=first, second=second, conclusion=conclusion, image=image)

      return JsonResponse({'status': 'success', 'message': "Blog Uploaded successfully!"})
   blogs=Blog.objects.all()
   return render(request,'myadmin/upload-blog.html',{'blogs':blogs})

@never_cache
@login_required(login_url="login")
def edit_blog(request,id):
   blog= Blog.objects.get(id=id)
   if request.method=="POST": 
      title = request.POST.get('title')
      type = request.POST.get('type')
      first = request.POST.get('first')
      second = request.POST.get('second')
      conclusion = request.POST.get('conclusion')
      image= request.FILES.get('image')
      errors = {}

      if not title:
         errors['title'] = "Title field is required"

      if type not in ['Social','Educational']:
         errors['type'] = "Select a valid Type"

      if not conclusion:
         errors['conclusion'] = "This field is required"

      if errors:
         return JsonResponse({'status': 'error', 'errors': errors})
      blog.title = title
      blog.first = first
      blog.second = second
      blog.conclusion = conclusion
      if 'image' in request.FILES:
         if blog.image:
            old_path = os.path.join(settings.MEDIA_ROOT, str(blog.image))  # Full path to the image file
            if os.path.exists(old_path):
               os.remove(old_path) 
         blog.image = request.FILES['image']
      blog.save()
      return JsonResponse({'status': 'success', 'message': "Blog Updated successfully!"})
   
   return render(request,'myadmin/edit-blog.html',{'blog':blog})

@never_cache
@login_required(login_url="login")
def deleteBlog(request,id):
    blog=Blog.objects.get(pk=id)
    blog.delete()
    messages.success(request, "Blog deleted Successfully")
    return redirect('upload-blog')

@never_cache
@login_required(login_url="login")
def deleteRow(request,tbl,id):
    if tbl == 'con':
        contact=Contact.objects.get(pk=id)
        contact.delete()
        messages.success(request, "Contact Message deleted Successfully")
        return redirect('contact-list')
    if tbl=='app':
        join= Join.objects.get(pk=id)
        join.delete()
        messages.success(request, "Application Message deleted Successfully")
        return redirect('application-list')




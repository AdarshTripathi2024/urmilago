from django.shortcuts import render,redirect, get_object_or_404
from .models import Contact,Join,Subscriber
from myadmin.models import Blog
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from .emails import send_otp_email,generate_otp
from django.views.decorators.http import require_POST

# Create your views here.
def home(request):
    return render(request,'urmilafoundation/home.html')

def about(request):
    return render(request,'urmilafoundation/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        if email and '@' not in email:
            messages.error(request,"Enter a valid email")
        if not phone.isdigit() or len(phone)!=10:
            messages.error(request,"Enter a valid Mobile Number")
        if messages.get_messages(request):
            return render(request,'urmilafoundation/contact.html')
        Contact.objects.create(name=name,email=email,phone=phone,message=message)
        messages.success(request,"Your Message sent successfully")
        return redirect('contact-us')
    return render(request,'urmilafoundation/contact.html')

def team(request):
    return render(request,'urmilafoundation/team.html')

def gallery(request):
    return render(request,'urmilafoundation/gallery.html')

def e_gallery(request):
    return render(request,'urmilafoundation/egallery.html')

def social_activity(request):
    return render(request,'urmilafoundation/social.html')

def educational_activity(request):
    return render(request,'urmilafoundation/educational.html')

def director(request):
    return render(request,'urmilafoundation/director.html')

def donate(request):
    return render(request,'urmilafoundation/donate.html')

def join_us(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        occupation = request.POST.get('occupation', '').strip()
        address = request.POST.get('address', '').strip()

        errors = {}

        if not email or '@' not in email:
            errors['email'] = "Enter a valid email"

        if not phone.isdigit() or len(phone) != 10:
            errors['phone'] = "Enter a valid Mobile Number"

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors})

        Join.objects.create(name=name, email=email, phone=phone, message=message, address=address, occupation=occupation)

        return JsonResponse({'status': 'success', 'message': "Your application sent successfully!"})

    return render(request,'urmilafoundation/join-us.html')

def facility(request):
    return render(request,'urmilafoundation/facility.html')

def our_blogs(request):
    blogs=Blog.objects.all()
    return render(request,'urmilafoundation/our-blogs.html',{'blogs':blogs})

def blog(request,id):
    blog= get_object_or_404(Blog, id=id)
    return render(request, 'urmilafoundation/blog_format.html', {'blog': blog})

def deleteBlog(request,id):
    blog=Blog.objects.get(pk=id)
    blog.delete()   
    return redirect('upload-blog')

def deleteRow(request,tbl,id):
    if tbl == 'con':
        contact=Contact.objects.get(pk=id)
        contact.delete()
    if tbl=='app':
        join= Join.objects.get(pk-id)
        join.delete()

def faq(request):
    return render(request,'urmilafoundation/faq.html')

def subscribe(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    email = request.POST.get('email')
    errors={}
    if '@' not in email:
        errors['email'] = 'Enter a valid email address.'
    if errors:
        return JsonResponse({'status': 'error', 'errors': errors}, status=400)
    otp = generate_otp()
    subscriber, created = Subscriber.objects.get_or_create(email=email)
    if subscriber:
        if subscriber.is_verified:
            return JsonResponse({
            'status': 'success',
            'message': 'Already subscribed.'
        })
    subscriber.otp = otp
    subscriber.verified = False
    subscriber.save()
    try:
        send_otp_email(email, otp)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Failed to send OTP email. Please try again.'}, status=500)
    message = 'OTP sent for verification.' if created else 'OTP resent for verification.'
    return JsonResponse({
        'status': 'success',
        'message': message,
        'email': email
    })

@require_POST
def verify_otp(request):
    email = request.POST.get('email')
    user_otp = request.POST.get('otp')

    if not email or not user_otp:
        return JsonResponse({'status': 'error', 'message': 'Email and OTP are required.'}, status=400)

    try:
        subscriber = Subscriber.objects.get(email=email)
        if subscriber.otp == user_otp:
            subscriber.is_verified = True
            subscriber.otp = ''
            subscriber.save()
            return JsonResponse({'status': 'success', 'message': 'Successfully subscribed to the newsletter.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'}, status=400)

    except Subscriber.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found.'}, status=404)

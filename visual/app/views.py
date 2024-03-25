from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from django.core.exceptions import ValidationError
from django.http import Http404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os
import razorpay



def indx(re):
    return render(re,'index.html')

def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            data = loguser.objects.get(username=username)
            if data.password == password:
                request.session['user'] = username
                messages.success(request, "login success")
                return redirect(event)
            else:
                messages.error(request, 'password incorrect')
                return redirect(log)
        except loguser.DoesNotExist:
            if username == 'admin' and password == 'admin':
                request.session['admin'] = username
                messages.success(request, "login success")
                return redirect(adminhome)
            else:
                messages.info(request, "username incorrect")
                return redirect(log)
    else:
        return render(request, 'login.html')

    # return render(request,'login.html')

def reg(request):
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['email']
        c = request.POST['password']
        try:
            data = loguser.objects.create(username=a,email=b, password=c)
            data.save()
            messages.success(request, "registration sucess")
            return redirect(log)
        except:
            messages.warning(request, "username already exists")
    return render(request,'register.html')

def about(request):
    return render(request,'about.html')

def comp(request):
    if request.method=='POST':
        j = loguser.objects.get(username=request.session['user'])
        k = request.POST['mail']
        l = request.POST['subject']
        m = request.POST['message']
        try:
            data = Complaint.objects.create(username=j,mail=k,subject=l,message=m)
            data.save()
            messages.success(request, "sent successfully")
            return redirect(indx)
        except:
            messages.error(request, "username incorrect")
    return redirect(indx)

def document(request):
    if request.method == 'POST':
        # Retrieve data from the request
        fname = request.POST.get('fname')
        username = request.POST.get('username')
        file_type = request.POST.get('fformat')
        doc = request.FILES.get('doc')
        inote = request.POST.get('inote')
        dates = request.POST.get('dates')

        # Check file extension
        valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        valid_audio_extensions = ['.mp3']
        valid_video_extensions = ['.mp4', '.avi', '.mov']

        _, file_extension = os.path.splitext(doc.name.lower())

        if file_extension in valid_image_extensions:
            file_type = 'image'
        elif file_extension in valid_audio_extensions:
            file_type = 'audio'
        elif file_extension in valid_video_extensions:
            file_type = 'video'
        else:
            raise ValidationError('Invalid file type. Supported file types are: JPG, JPEG, PNG, GIF, MP3, MP4, AVI, MOV.')

        data1 = documents(fname=fname, username=username, doc=doc, inote=inote, dates=dates,file_type=file_type)
        data1.save()

        return redirect(document)

    return render(request, 'docs.html')

def display_document(request):
    # Retrieve username from session
    username = request.session.get('user')

    # Get all documents for the given username
    all_files = documents.objects.filter(username=username)

    # Pass data to the template for rendering
    return render(request, 'display_document.html', {'username': username, 'all_files': all_files})

def disp_image(request):
    image_files =  documents.objects.filter(file_type='image')
    return render(request, 'images.html', {'image_files': image_files})

def view_details(request, file_type, file_id):
    try:
        if file_type == 'image':
            document = get_object_or_404(documents, pk=file_id)
        elif file_type == 'video':
            document = get_object_or_404(documents, pk=file_id)
        elif file_type == 'audio':
            document = get_object_or_404(documents, pk=file_id)
        else:
            raise Http404("Invalid file type")

        # Get the original file size
        file_path = document.doc.path
        file_size = os.path.getsize(file_path)

        url = reverse('view_details', args=[file_type, file_id])
 
        return render(request, 'viewdetails.html', {'document': document, 'file_size': file_size})

    except Http404:
        return render(request, 'error.html', {'message': 'Invalid file type.'})
    
@csrf_exempt
@require_POST
def delete_file(request, file_type, file_id):
    try:
        document = get_object_or_404(documents, pk=file_id)

        # Delete the document
        document.delete()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def disp_audio(request):
    audio_files =  documents.objects.filter(file_type='audio')
    return render(request, 'audio.html', {'audio_files': audio_files})

def disp_video(request):
    video_files = documents.objects.filter(file_type='video')
    return render(request, 'video.html', {'video_files': video_files})

def adminhome(re):
    return render(re,'adminhome.html')

def aimage(re):
    image_files = documents.objects.filter(file_type='image')
    return render(re, 'aimage.html', {'image_files': image_files})

def aaudio(request):
    audio_files =  documents.objects.filter(file_type='audio')
    return render(request, 'aaudio.html', {'audio_files': audio_files})

def avideo(request):
    video_files = documents.objects.filter(file_type='video')
    return render(request, 'avideo.html', {'video_files': video_files})

def event(request):
    return render(request,'event.html')


def logout(re):
    if 'user' in re.session:
        re.session.flush()
    return redirect(log)

def admin_file_management(request):
    # Get all uploaded documents
    all_documents = documents.objects.all()

    # Handle form submissions (edit or delete)
    if request.method == 'POST':
        # Check if the form is for editing a document
        if 'edit_document' in request.POST:
            # Handle the document edit logic
            document_id = request.POST.get('document_id')
            return redirect('edit_document', document_id=document_id)
        # Check if the form is for deleting a document
        elif 'delete_document' in request.POST:
            # Handle the document delete logic
            document_id = request.POST.get('document_id')
            document = get_object_or_404(documents, pk=document_id)
            document.delete()
            return redirect('admin_file_management')

    return render(request, 'admin_file_management.html', {'documents': all_documents})



def payment(request,id=None):
        amount = 10000
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        return render(request, "payment.html")
# Create your views here.

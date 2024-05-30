from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from . models import Record

from django.contrib import messages

# Create your views here.

def home(request):
   
    return render(request, 'webapp/index.html')



# Register a user

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect('my-login')

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


# - Login a user

# def my_login(request):

#     form = LoginForm()

#     if request.method == "POST":

#         form = LoginForm(request, data=request.POST)

#         if form.is_valid():

#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username=username, password=password)

#             if user is not None:

#                 auth.login(request, user)

#     context = {'form':form}

#     return render(request, 'webapp/my-login.html', context=context)

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                messages.success(request, "You have logged")

                return redirect('dashboard')

    context = {'form': form}

    return render(request, 'webapp/my-login.html', context=context)

#  -Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)


#  - Create a record@login_required(login_url='my-login')
def create_record(request):
    if request.method == "POST":
        # Extract form data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        country = request.POST.get('country')
        image = request.FILES.get('image')  # Get the uploaded image file
        introduction = request.POST.get('introduction')
        
        # Validate image file type
        if image:
            valid_image_extensions = ['png', 'jpeg', 'jpg', 'webp']
            image_extension = image.name.split('.')[-1].lower()
            if image_extension not in valid_image_extensions:
                messages.error(request, "Invalid image format. Please upload a PNG, JPEG, JPG, or WEBP file.")
                return render(request, 'webapp/create-record.html')
        
        # Create a new Record object with the extracted data
        new_record = Record(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            province=province,
            country=country,
            image=image,
            introduction=introduction
        )
        
        # Save the new record object to the database
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("dashboard")  # Redirect to the dashboard or any other page
    else:
        # This is for GET requests, i.e., when the user accesses the create_record page
        return render(request, 'webapp/create-record.html')

# update a record
@login_required(login_url='my-login')
def update_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            # Optionally add a success message here
            return redirect('dashboard')
    else:
        form = UpdateRecordForm(instance=record)
    
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context=context)

#  - Read / View a singular record

@login_required(login_url='my-login')
def singular_record(request, pk):

    all_record = Record.objects.get(id=pk)

    context = {'record':all_record}

    return render(request, 'webapp/view-record.html', context=context)


# Delete a record
@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")




# - User Logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout successfully!")

    return redirect('my-login')

@login_required(login_url='my-login')
def search_records(request):
    query = request.GET.get('q')
    records = Record.objects.filter(first_name=query) | Record.objects.filter(last_name=query) | Record.objects.filter(city=query)
    context = {'records': records}
    return render(request, 'webapp/dashboard.html', context=context)
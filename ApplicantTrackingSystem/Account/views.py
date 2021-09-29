from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages #import messages
#from django.contrib.auth.forms import AuthenticationForm 
from Account.models import Account
from JobPosts.models import JobPost
from Account.forms import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm

#def registration_view(request):
#	if request.method == "POST":
#		form = NewUserForm(request.POST)
#		if form.is_valid():
#			user = form.save()
#			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#			messages.success(request, "Registration successful." )
#			return redirect("home")
#		messages.error(request, "Unsuccessful registration. Invalid information.")
#	form = NewUserForm
#	return render (request=request, template_name="../Templates/registration.html", context={"register_form":form})

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('account')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

#def login_view(request):
	#context = {}

	#user = request.user
	#if user.is_authenticated: 
	#	return redirect("account")

	#if request.method == "POST":
	#	form = Account
	#	AuthenticationForm(request, data=request.POST)
	#	if form.is_valid():
	#		username = form.cleaned_data.get('username')
	#		password = form.cleaned_data.get('password')
	#		user = authenticate(username=username, password=password)
	#		if user is not None:
	#			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
	#			messages.info(request, f"You are now logged in as {username}.")
	#			return redirect("home")
	#		else:
	#			messages.error(request,"Invalid username or password.")
	#	else:
	#		messages.error(request,"Invalid username or password.")
	#form = AuthenticationForm()
	#return render(request=request, template_name="../Templates/login.html", context={"login_form":form})
def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("account")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				messages.info(request, f"You are now logged in as {user}.")
				return redirect("account")
			else:
				messages.error(request,"Invalid username or password.")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "../Templates/login.html", context)

def update_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['account_form'] = form

	job_posts = JobPost.objects.filter(author=request.user)
	context['job_posts'] = job_posts

	return render(request, "../Templates/account.html", context)


def must_authenticate_view(request):
	return render(request, '../Templates/must_authenticate.html', {})
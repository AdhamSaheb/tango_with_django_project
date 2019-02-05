
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def index(request):

	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list , 'pages':page_list  }
	return render(request,"rango/index.html" , context_dict)

def about(request) : # rango/about

	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!
	context_dict = {'Adham': " This tutorial has been put together by Adham Tamimi" }
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None

	return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            category = form.save(commit=True)
            print(category, category.slug)
            # Now that the category is saved
            # We could give a confirmation message
            # But instead since the most recent catergory added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    # Will handle the bad form (or form details), new form or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})
@login_required
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
			return show_category(request, category_name_slug)
		else:
			print(form.errors)

	context_dict = {'form':form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)


def register(request):
# A boolean value for telling the template
# whether the registration was successful.
# Set to False initially. Code changes value to
# True when registration succeeds.
	registered = False
# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
# Attempt to grab information from the raw form information.
# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
# Save the user's form data to the database.
			user = user_form.save()
# Now we hash the password with the set_password method.
			user.set_password(user.password)

# Once hashed, we can update the user object.
			user.save()
# Now sort out the UserProfile instance.
# Since we need to set the user attribute ourselves,
# we set commit=False. This delays saving the model
# until we're ready to avoid integrity problems
			profile = profile_form.save(commit=False)
			profile.user = user
# Did the user provide a profile picture?
# If so, we need to get it from the input form and
#put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
# Now we save the UserProfile model instance.
			profile.save()
# Update our variable to indicate that the template
# registration was successful.
			registered = True
		else :
# Invalid form or forms - mistakes or something else?
# Print problems to the terminal.
			print(user_form.errors, profile_form.errors)


	else:
# Not a HTTP POST, so we render our form using two ModelForm instances.
# These forms will be blank, ready for user input.
		user_form = UserForm()
		profile_form = UserProfileForm()
# Render the template depending on the context.
	return render(request,'rango/register.html',{'user_form': user_form,'profile_form': profile_form,'registered': registered})


def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):

	logout(request)

	return HttpResponseRedirect(reverse('index'))

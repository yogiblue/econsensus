from custom_organizations.forms import CustomUserSignupRegistrationForm
from registration.signals import user_registered

def user_created(sender, user, request, **kwargs):
	form = CustomUserSignupRegistrationForm(request.POST)
	#data = profile.Profile(user=user)
	#data.city_id = form.data["city"]
        user.first_name = form.data['first_name']
        user.last_name = form.data['last_name']
	user.save()

user_registered.connect(user_created)
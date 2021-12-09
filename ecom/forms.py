from django import forms
from django.contrib.auth.forms import  UserCreationForm
from .models import CustomUser, Shipping_address

class NewUserForm(UserCreationForm):
	class Meta:
		model = CustomUser
		# fields = "__all__"
		fields=["username","email","mobile","address","password1","password2"]		
		
	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

# class UserProfileForm(forms.ModelForm):
# 	class Meta:
# 		model=CustomUser
# 		fields=['mobile','address']
# 		widgets={'mobile':forms.NumberInput(attrs={'class':'form-control'}),
# 		'address':TextInput(attrs={'class':'form-control'})}


# class DeliveryForm(forms.ModelForm):
# 	class Meta:
# 		model=DeliveryAddress
# 		fields=["first_name","last_name","email","phone_number",
# 		"address","postal_code","city"]
# 		widgets={'first_name':forms.TextInput(attrs={'class':'form-control'}),
# 		'last_name':forms.TextInput(attrs={'class':'form-control'}),
# 		'email':forms.EmailInput(attrs={'class':'form-control'}),
# 		'phone_number':forms.NumberInput(attrs={'class':'form-control'}),
# 		'address':forms.TextInput(attrs={'class':'form-control'}),
# 		'postal_code':forms.NumberInput(attrs={'class':'form-control'}),
# 		'city':forms.TextInput(attrs={'class':'form-control'})}
# 		labels={
# 			"first_name":"First Name",
# 			"last_name":"Last Name",
# 			"email":"Email",
# 			"phone_number":"Phone",
# 			"address":"Address",
# 			"postal_code":"Postal Code",
# 			"city":"City",
# 		}
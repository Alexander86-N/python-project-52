from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from task_manager.users.models import ProjectUsers


class SignUpForm(UserCreationForm):

    class Meta:
        model = ProjectUsers
        fields = ['first_name', 'last_name', 'username', 'password1',
                  'password2']


class SignInForm(AuthenticationForm):

    username = ProjectUsers.username
    password = ProjectUsers.password
    fields = ['username', 'password1']

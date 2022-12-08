from authapp.forms import UserLoginForm, UserRegisterForm


def get_context_data(request):
    return {
        'register_ajax': UserRegisterForm(),
        'login_ajax': UserLoginForm(),
    }

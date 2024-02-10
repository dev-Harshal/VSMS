from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout


def user_custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page with 'next' parameter set to the original requested page
            login_url = reverse('login')  # Replace 'your_login_url_name' with your login URL name
            next_url = request.path  # Get the current path
            return redirect(f'{login_url}?next={next_url}')
        else:
            if request.user.role == "Staff":
                logout(request)
                return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page with 'next' parameter set to the original requested page
            login_url = reverse('staff-login')  # Replace 'your_login_url_name' with your login URL name
            next_url = request.path  # Get the current path
            return redirect(f'{login_url}?next={next_url}')
        else:
            if request.user.role == "User":
                logout(request)
                return redirect('staff-login')
            
        return view_func(request, *args, **kwargs)
    return wrapper
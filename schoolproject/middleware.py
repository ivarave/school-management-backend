from django.contrib.auth import login, get_user_model

User = get_user_model()

class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("✅ AutoLoginMiddleware executing...")  # DEBUG

        if request.path.startswith('/admin/') and not request.user.is_authenticated:
            user = User.objects.filter(is_superuser=True).first()
            if user:
                print(f"🔑 Logging in as: {user.username}")  # DEBUG
                login(request, user)

        return self.get_response(request)

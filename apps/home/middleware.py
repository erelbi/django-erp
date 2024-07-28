class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.current_user = None

    def __call__(self, request):
        self.current_user = request.user
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.user = self.current_user
        return None
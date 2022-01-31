from .services import Provider
import re


class Analytics:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        # Checking the view. If the name contains the identifier "__" at the end, call the Provider class.
        if re.findall(r"__$", view_func.__name__, flags=re.IGNORECASE):
            view = Provider(request, view_func, view_kwargs)
            view.add()
            return None

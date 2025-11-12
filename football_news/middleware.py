import re
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check if the request path matches any exempted URLs
        exempt_urls = getattr(settings, 'CSRF_EXEMPT_URLS', [])
        for pattern in exempt_urls:
            if re.match(pattern, request.path):
                return None  # Skip CSRF check
        
        # Otherwise, run the normal CSRF check
        return super().process_view(request, view_func, view_args, view_kwargs)

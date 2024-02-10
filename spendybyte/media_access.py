from django.http import HttpResponse
from django.http import HttpResponseForbidden


# https://stackoverflow.com/questions/45872539/django-and-nginx-x-accel-redirect
def media_access(request, filepath):
    if request.user.is_staff:
        response = HttpResponse(status=200)
        response["Content-Type"] = ""
        response["X-Accel-Redirect"] = "/media/" + filepath
        return response
    return HttpResponseForbidden("Not authorized to access this media.")

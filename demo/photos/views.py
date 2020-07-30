import os
from django.conf import settings
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
from photos.models import Photo


class Home(generic.TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["accepted_mime_types"] = ["image/*"]
        context['project_root'] = settings.PROJECT_ROOT
        return context


@require_POST
def upload(request):
    file = upload_receive(request)

    instance = Photo(file=file)
    instance.save()

    basename = os.path.basename(instance.file.path)
    full_file_path = str(instance.file)

    file_dict = {
        "name": basename,
        "size": file.size,
        "url": settings.MEDIA_URL + full_file_path,
        "thumbnailUrl": settings.MEDIA_URL + full_file_path,
        "deleteUrl": reverse("jfu_delete", kwargs={"pk": instance.pk}),
        "deleteType": "POST",
    }

    return UploadResponse(request, file_dict)


@require_POST
def upload_delete(request, pk):
    success = True
    try:
        instance = Photo.objects.get(pk=pk)
        os.unlink(instance.file.path)
        instance.delete()
    except Photo.DoesNotExist:
        success = False

    return JFUResponse(request, success)

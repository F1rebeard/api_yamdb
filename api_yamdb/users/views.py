from django.http import JsonResponse


def simpleview(request):
    return JsonResponse({'foo': 'bar'})

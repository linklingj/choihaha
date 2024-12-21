from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import logic

@csrf_exempt
def req(request):
    if request.method == 'GET':
        return JsonResponse({"position": f"{logic.get_place()}"})
    if request.method == 'POST':
        try:
            logic.set_place(request.POST.get('position'))
            return JsonResponse({"position": f"{logic.get_place()}"})
        except :
            return JsonResponse({"error":"server fail"}, status=400)
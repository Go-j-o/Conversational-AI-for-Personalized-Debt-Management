import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
print("LOADED API KEY:", TOGETHER_API_KEY)  # For debugging


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .together_ai import get_debt_advice  # Your AI helper function


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            if not user_message:
                return JsonResponse({"error": "No message provided."}, status=400)
            advice = get_debt_advice(user_message)
            return JsonResponse({"response": advice})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
    elif request.method == "GET":
        # Just return a test message
        return JsonResponse({"message": "Send a POST request with a 'message' field."})
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)



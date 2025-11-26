from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tenant
import requests
import openai, os
from django.views.decorators.csrf import csrf_exempt

openai.api_key = os.getenv("openai_api")

@csrf_exempt
@api_view(['POST'])
def chatbot_api(request):
    # ১. Tenant validate
    api_key = request.headers.get("X-API-KEY")
    print("DEBUG: Received X-API-KEY =", api_key)

    try:
        tenant = Tenant.objects.get(api_key=api_key)
    except Tenant.DoesNotExist:
        return Response({"error": "Unauthorized"}, status=401)

    user_msg = request.data.get("message", "").strip()

    # ২. Multiple API থেকে ডেটা fetch
    hospital_data = {}
    for api_url in tenant.rest_api:  # JSONField থেকে URLs নেওয়া হচ্ছে
        try:
            resp = requests.get(api_url, timeout=5)
            if resp.status_code == 200:
                hospital_data[api_url] = resp.json()
            else:
                hospital_data[api_url] = {"error": f"Status {resp.status_code}"}
        except Exception as e:
            hospital_data[api_url] = {"error": str(e)}

    # ৩. AI prompt তৈরি
    prompt = f"""
You are a hospital support AI assistant for {tenant.name}.
User asked: "{user_msg}".
Here is all available hospital data from APIs: {hospital_data}.

Reply in short, helpful sentences with proper analysis and give suggestion to user. 
Do NOT include ** in your response.  answer in english or bangla language always .
Use HTML <br> line breaks and emojis where relevant.
"""


    # ৪. OpenAI call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        print("OpenAI Error:", e)
        ai_reply = "⚠️ AI service is currently unavailable."

    return Response({"reply_html": ai_reply})


from django.shortcuts import render
from .models import Tenant

def widget_view(request, api_key):
    tenant = Tenant.objects.get(api_key=api_key)
    return render(request, "widget.html", {"api_key": tenant.api_key})

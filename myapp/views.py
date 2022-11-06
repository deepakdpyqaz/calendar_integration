from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
from googleapiclient.errors import HttpError

# Create your views here.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@api_view(["GET"])
def GoogleCalendarInitView(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        SCOPES,
        redirect_uri="http://localhost:8000/rest/v1/calendar/redirect",
    )
    creds, _ = flow.authorization_url()
    return redirect(creds)


@api_view(["GET"])
def GoogleCalendarRedirectView(request):
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    token = flow.fetch_token(code=request.GET.get("code"))
    service = build("calendar", "v3", credentials=flow.credentials)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = (
        service.events()
        .list(calendarId="primary", timeMin=now, singleEvents=True, orderBy="startTime")
        .execute()
    )
    events = events_result.get("items", [])
    return Response({"events": events})

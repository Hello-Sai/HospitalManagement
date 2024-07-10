from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from online_connect.models import Appointment
import os
# Create your views here.

from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

@csrf_exempt
def list_of_doctors(request):
    doctors = User.objects.filter(is_doctor = True)
    return render(request,'doctorspage.html',locals())
@csrf_exempt
@login_required(login_url='/')
def book_appointment(request,id):
    user = User.objects.filter(id = id)

    if request.method=="POST":
        print(request.POST['appoint_date'],request.POST['appoint_time'])
        if user:
            user = user.first()
            if user.is_doctor:
                appointment = user.appointments.create(patient = request.user,required_speciality = request.POST['required_speciality'],date = request.POST['appoint_date'],time = request.POST['appoint_time'])
                return redirect(reverse('init_event',kwargs={'id':appointment.id}))
            else:
                messages.error(request,'Not a valid Id',"danger")
                return redirect('appointments')
    return render(request,'book_appointment.html')

@csrf_exempt
def appointments(request):
    if request.user.is_doctor:
        appointments = request.user.appointments.all()
    else:
        appointments = request.user.doctor_appointments.all()
    return render(request,'appointments.html',locals())






SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')
@csrf_exempt
def create_appointment_event(request,id):



    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES,redirect_uri=settings.REDIRECT_URI)
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    request.session['state'] = state
    request.session['appointment_id'] = id
    return redirect(authorization_url)
@csrf_exempt
def google_calendar_redirect_view(request):
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    from datetime import datetime,timedelta
    try:
        print("build ",request.build_absolute_uri())
        state = request.session.get('state')
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, state=state,redirect_uri=settings.REDIRECT_URI)
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        print('executed')
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)
        # doctor = request.session['doctor']
        appointment = Appointment.objects.get(id = request.session['appointment_id'])
        # doctor = appointment.doctor

        
        
        
        start_datetime = datetime.combine(appointment.date, appointment.time)
        

    # Calculate end time (start time + 45 minutes)
        end_datetime = start_datetime + timedelta(minutes=45)

        # Format datetime objects to ISO 8601 format
        start_time_str = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        end_time_str = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        event = {
            'summary': appointment.required_speciality,
            # 'location': '800 Howard St., San Francisco, CA 94103',
            # 'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': start_time_str,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': 'Asia/Kolkata',
            },
            'attendees': [
                {'email': appointment.doctor.email},
            ],
            # 'reminders': {
            #     'useDefault': False,
            #     'overrides': [
            #         {'method': 'email', 'minutes': 24 * 60},
            #         {'method': 'popup', 'minutes': 10},
            #     ],
            # },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        # Save credentials to the user model
        messages.success(request,"Your Appointment has Booked Successfully")
    except Exception as e:
        return JsonResponse({'error':str(e)})
    return redirect("appointments")    

""" def google_calendar_create_event_view(request):
    user = request.user

    # credentials = Credentials(
    #     token=credentials.token
    #     refresh_token=credentials.refresh_token
    #     token_uri='https://oauth2.googleapis.com/token',
    #     client_id=settings.GOOGLE_CLIENT_ID,
    #     client_secret=settings.GOOGLE_CLIENT_SECRET,
    #     expiry=credentials.expiry
    # )

    
    return HttpResponse('Event created successfully!') """

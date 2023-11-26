import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from records.models import Employee


def home(request):
    return render(request, "index.html")


def ImportView(request):
    if request.method != "POST":
        return HttpResponse("Not a valid method to import file")
    print(request.FILES)
    file = request.FILES['myfile']
    # print(file)
    # path = file.file
    # print(path)
    df = pd.read_excel(file.file)
    for data in df.values:
        employee = Employee(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
        )

        employee.save()
    return render(request, "import.html",{'df':df.values})


def employee(request):
    try:
        employee = Employee.objects.get(Name=request.POST["name"])
        context = {"employee":employee}
        return render(request,"record.html",context)
    except Employee.DoesNotExist:
        messages.error(request,"Record Not Found , Please check your name once (case-sensitive)","warning")
    except Exception as e:
        messages.error(request,"Got following error --> %s"%e,"warning")
    return render(request,"index.html")

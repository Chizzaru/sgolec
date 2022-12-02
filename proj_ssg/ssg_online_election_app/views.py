from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.urls import reverse
import xlsxwriter
from .models import Category, Candidate, VoteVoucher
from re import template
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .generator import runGeneration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, GenerateVoucherForm


def index_view(request):
    arrCategory = Category.objects.all().values()
    arrCandidate=Candidate.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'arrCategory' : arrCategory,
        'arrCandidate' : arrCandidate
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='login_view')
def dashboard_view(request):
    return render(request, "dashboard.html")

@login_required(login_url='login_view')
def generate_voucher_view(request):
    form = GenerateVoucherForm(request.POST or None)
    if request.POST and form.is_valid():
        key = form.cleaned_data['voucher_key']
        count = form.cleaned_data['voucher_count']
        length = 5

        generatedvoucherlist = runGeneration(key,length,count)
        for x in generatedvoucherlist:
            obj = VoteVoucher(voucher_code = x)
            obj.save()
        messages.success(request, 'Successfully Generated Vouchers.')
        return render(request, 'generate_voucher.html', {'form': GenerateVoucherForm()})
    else:
        form = GenerateVoucherForm()
    return render(request, 'generate_voucher.html',{'form':form})



def export_page(request):
    pass

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard_view'))
    else:
        return render(request, 'login.html', {'form': form })
    return render(request, 'login.html', {'form': form })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))



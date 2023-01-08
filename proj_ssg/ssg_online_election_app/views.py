import io
import os
import xlsxwriter
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.urls import reverse
from .models import Category, Candidate, VoteVoucher, Vote
from re import template
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .generator import runGeneration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, GenerateVoucherForm, UploadImageForm


#algorithm
from .algo import findMajority


def index_view(request):
    arrCategory = Category.objects.all().values()
    arrCandidate=Candidate.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'arrCategory' : arrCategory,
        'arrCandidate' : arrCandidate
    }
    return HttpResponse(template.render(context, request))


def candidates_view(request):
    template = loader.get_template('candidates.html')
    context = {}
    data = []
    candidates = Candidate.objects.all().values().order_by('category_id')

    for x in candidates:
        f = {
            'id' : x['id'],
            'candidate_name' : x['candidate_name'],
            'category' : Category.objects.get(id = x['category_id']).category_name,
            'address' : x['address'],
            'yrsec' : x['year_and_section'],
            'self_intro' : x['brief_self_intro'],
            'img_path' : x['img_path']
        }

        data.append(f)
    
    context = {
        'data' : data
    }

    return HttpResponse(template.render(context,request))


def save_vote(request):
    if request.method == "POST":
        pres = request.POST.get('checkboxpres',None)
        ivpres = request.POST.get('checkboxivpres',None)
        evpres = request.POST.get('checkboxevpres',None)
        isec = request.POST.get('checkboxisec',None)
        esec = request.POST.get('checkboxesec',None)
        pio = request.POST.get('checkboxpio',None)
        aud = request.POST.get('checkboxaud',None)
        bus = request.POST.get('checkboxbus',None)
        treas = request.POST.get('checkboxtreas',None)
        rep = request.POST.getlist('checkboxrep',None)
        voucher = request.POST.get('votevoucher',None)

        #validate vote voucher
        obj = VoteVoucher.objects.filter(voucher_code = voucher).values()
        voucherid = ""
        isUsed = False
        if obj:
            voucherid = obj[0]['id']
            isUsed = obj[0]['isUsed']
        
        if voucherid == "" or isUsed == True:
            return render(request,"response.html",{"message":"Voucher not found or it is already used","message_type":"danger"})

        if(None in [pres,ivpres,evpres,isec, esec,pio,aud,bus,treas,rep,voucher]):
            return render(request,"response.html",{"message":"Oops! There is a category that you forgot to vote","message_type":"danger"})

        # Saving
        datas = [
            pres,
            ivpres,
            evpres,
            isec,
            esec,
            pio,
            aud,
            bus,
            treas
        ]
        
        for data in datas:
            arr = [x.strip() for x in data.split('/') if x]
            arrobj = Vote(vote_voucher_id=voucherid, category_id=arr[0], candidate_id=arr[1])
            arrobj.save()


        for x in rep:
            print(x)
            arr = [h.strip() for h in x.split('/') if h]
            arrobj = Vote(vote_voucher_id=voucherid, category_id=arr[0], candidate_id=arr[1])
            arrobj.save()

        #update voucher
        upt_obj = VoteVoucher.objects.get(id = voucherid)
        upt_obj.isUsed = True
        upt_obj.save()

        return render(request,"response.html",{"message":"Your vote successfully saved.","message_type":"success"})



@login_required(login_url='login_view')
def dashboard_view(request):
    total_voucher = VoteVoucher.objects.all().count()
    used_voucher = VoteVoucher.objects.filter(isUsed = True).count()
    unused_voucher = VoteVoucher.objects.filter(isUsed = False).count()

    # variable data will hold the results
    datas = []
    #get the category id
    categories = Category.objects.all().values()
    for num in range(len(categories)):
        categ_id = categories[num]['id']
        # get the vote by category
        arr = []
        # if the category is for representatives
        if categ_id == 10:
            arr_alg = Vote.objects.filter(category_id = categ_id).values()
            # loop 3 times for representative only
            for g in range (3):
                for i in range (len(arr_alg)):
                    item = arr_alg[i]['candidate_id']
                    if item in datas:
                        continue
                    else:
                        arr.append(item)
                lead = findMajority(arr, len(arr))
                #clearing the arr
                arr.clear()
                datas.append(lead)
        # if the category is not representatives
        else:
            arr_alg = Vote.objects.filter(category_id = categ_id).values()
            for i in range (len(arr_alg)):  
                arr.append(arr_alg[i]['candidate_id'])

            lead = findMajority(arr, len(arr))
            datas.append(lead)

    #print(datas)
    candidates = []
    for candidate in datas:
        if candidate != -1:
            obj = Candidate.objects.filter(id = candidate).values()[0]
            #print(obj['candidate_name'])
            candidates.append(obj['candidate_name'])
        else:
            #print('No Majority')
            candidates.append('< No majority candidate >')
    
    #print(candidates)

    template = loader.get_template('dashboard.html')
    context = {
        'voucher_update' : {
            'used' : str(used_voucher),
            'unused' : str(unused_voucher),
            'total' : str(total_voucher)
        },
        'candidates' : candidates
        
    }
    return HttpResponse(template.render(context, request))



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
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # Even though the final file will be in memory the module uses temp
    # files during assembly for efficiency. To avoid this on servers that
    # don't allow temp files, for example the Google APP Engine, set the
    # 'in_memory' Workbook() constructor option as shown in the docs.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Get some data to write to the spreadsheet.
    #data = get_simple_table_data()

    # Write some test data.
    #for row_num, columns in enumerate(data):
    #    for col_num, cell_data in enumerate(columns):
    #        worksheet.write(row_num, col_num, cell_data)


    worksheet.write(0,0,"Voucher Code")
    worksheet.write(0,1,"Is already used?")

    obj = VoteVoucher.objects.all().values()

    for x in range(len(obj)):
        #column
        worksheet.write(x+1,0,obj[x]['voucher_code'])
        worksheet.write(x+1,1,obj[x]['isUsed'])

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

        # Set up the Http response.
    filename = 'voucherslist.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response    





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


def updatepic_view(request):

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = Candidate.objects.get(id = request.POST['id'])
            
            # delete old image
            try:
                profile = Candidate.objects.get(id = request.POST['id']).img_path
            except Candidate.DoesNotExist:
                return False

            new_file = request.FILES['img_path']
            if not profile == new_file:
                if os.path.isfile(profile.path):
                    os.remove(profile.path)

            image.id = request.POST['id']
            image.img_path = request.FILES['img_path']
            image.save()


    return HttpResponseRedirect(reverse('candidates_view'))
    #return HttpResponse(template.render(context,request))



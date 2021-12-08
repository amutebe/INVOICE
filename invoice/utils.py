from django import forms
import datetime
from datetime import date, timedelta
import calendar
from django.utils.timesince import timeuntil
import random




############################DEFINE USER GROUPS#####################################################
now = datetime.datetime.now().date()
today = datetime.datetime.now().date()



#FUNCTIONS TO GENERATE IDs###########
def get_companyCode():
    #return 'xyz'
    #company_code=Company.objects.all().order_by('company_code')[0:1]
    #for i in company_code:
    #    if i.company_code is not None:
    #      return str(i.company_code)
    return 'BCL'

def invoice_no():
   return str(get_companyCode()+'/'+(date.today()).strftime("%d%m%Y"))+'/'+'A'+str(random.randint(0, 999))+str(random.randint(1, 99))


def is_ManagementRepresentative(user):
    return user.groups.filter(name='ManagementRepresentative').exists()

def is_TopManager(user):
    return user.groups.filter(name='TopManager').exists()

def is_Auditor(user):
    return user.groups.filter(name='Auditor').exists()


def is_Executive(user):
    return user.groups.filter(name='Executive').exists()


#########################################DEFINE DATA GROUPS FOR INDIVIDUAL RECORDS#####################################################################
def is_Operations(user):
    return user.groups.filter(name='Operations').exists()

def is_Technical(user):
    return user.groups.filter(name='Technical').exists()

def is_Accounts(user):
    return user.groups.filter(name='Accounts').exists()

def is_Administration(user):
    return user.groups.filter(name='Administration').exists()

def is_Marketing(user):
    return user.groups.filter(name='Marketing').exists()


############################################GET LOGGEDIN USER DATA GROUP#######################################################################

def my_data_group(user):
    if user.groups.filter(name='Operations').exists():
        return "4"
    elif user.groups.filter(name='Marketing').exists():
        return "005"
    elif user.groups.filter(name='Administration').exists():
        return "001"
    elif user.groups.filter(name='Technical').exists():
        return "11"
    elif user.groups.filter(name='Accounts').exists():
        return "12"
    elif user.groups.filter(name='RelationsManager').exists():
        return "13"
    else:
        return ""



###################RESTRICTS UPLOAD SIZE TO 10MBS FOR DOCUMENT MANAGER#################################
def validate_file_size(value):
    filesize= value.size
    #print("PRINT FILESIZE",filesize)
    
    if filesize > 10485760:
        #print("PRINT FILESIZE two",filesize)
        raise forms.ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value

###################RESTRICTS UPLOAD SIZE TO 10MBS FOR VERIFICATIONS#################################
def validate_file_size_verification(value):
    filesize= value.size
    #print("PRINT FILESIZE",filesize)
    
    if filesize > 5242880:
        #print("PRINT FILESIZE two",filesize)
        raise forms.ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value

###########DATE USED TO FILTER ITEMS PENDING VERIFICATION FOR PAST 7 DAYS############
def past7daysDate():
    end = (now - timedelta(days=7))
    return end


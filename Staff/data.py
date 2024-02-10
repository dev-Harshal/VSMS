from Users.models import *
from django.db.models import Q
from functools import reduce
from calendar import month_name
from django.db.models import Sum
from django.db.models.functions import ExtractMonth


def countservice(status):
    service = Service.objects.all()
    return service.filter(status=status).all().count()
def countvehicles(type):
    service = Service.objects.all()
    return service.filter(category=type).all().count()

def countpendingvehicles(type,status="Pending"):
    return Service.objects.filter(status=status).filter(category=type).count()

def countsales(type):
    return sum([x['total_amount'] for x in Service.objects.filter(payment_status=True).filter(category=type).values('total_amount')])
def staffHomeData():
    service = Service.objects.all()
    data = {
        'pending':countservice("Pending"),
        'process':Service.objects.filter(Q(status="In Process") | Q(status="Work Completed")).all().count(),
        'complete':countservice("Completed"),
        'delivered':countservice("Delivered"),
        'revenue':sum([x['total_amount'] for x in Service.objects.filter(payment_status=True).all().values('total_amount')]),
        'customer':Users.objects.filter(role="User").count(),
        'compare':[countvehicles("2 Wheeler"),countvehicles("4 Wheeler"),countvehicles("Bus"),countvehicles("Truck")],
        'pending_chart':{'two':countpendingvehicles("2 Wheeler"),'four':countpendingvehicles("4 Wheeler"),
                         'bus':countpendingvehicles("Bus"),'truck':countpendingvehicles("Truck")},
        'process_chart':{'two':countpendingvehicles("2 Wheeler","In Process"),'four':countpendingvehicles("4 Wheeler","In Process"),
                         'bus':countpendingvehicles("Bus","In Process"),'truck':countpendingvehicles("Truck","In Process")},\
        'delivered_chart':{'two':countpendingvehicles("2 Wheeler","Delivered"),'four':countpendingvehicles("4 Wheeler","Delivered"),
                         'bus':countpendingvehicles("Bus","Delivered"),'truck':countpendingvehicles("Truck","Delivered")},
        'compare_sale':[countsales("2 Wheeler"), countsales("4 Wheeler"),countsales("Bus"),countsales("Truck")]
    }
    print(data['compare'],'Revenue')
    return data


#----------------------------------------------------------------------------------------------------------------------------\
def staffExpense():
    completed_services = Service.objects.filter(status='Delivered')

# Aggregate total_amount by month
    monthly_totals = completed_services.values('complete_date__month').annotate(total_amount_sum=Sum('total_amount'))

    # Map numerical month values to month names
    month_name_mapping = {i: month_name[i] for i in range(1, 13)}

    # Extract unique months and corresponding total amounts
    unique_months = [month_name_mapping[entry['complete_date__month']] for entry in monthly_totals]
    total_amounts = [entry['total_amount_sum'] for entry in monthly_totals]

    return unique_months,total_amounts



def staffvehicleexpense(category):
    # Get completed services for the given user and category
    completed_services = Service.objects.filter(status='Delivered',category=category)

    # Aggregate total_amount by month
    monthly_totals = completed_services.values('complete_date__month').annotate(total_amount_sum=Sum('total_amount'))

    # Map numerical month values to month names
    month_name_mapping = {i: month_name[i] for i in range(1, 13)}

    # Initialize lists for unique months and corresponding total amounts
    unique_months = []
    total_amounts = []

    # Iterate over all months (1 to 12)
    for month in range(1, 13):
        # Get the month name from the mapping
        month_name_str = month_name_mapping.get(month, None)
        
        # Check if the month is present in the query result
        if any(entry['complete_date__month'] == month for entry in monthly_totals):
            # If present, append the corresponding total amount
            total_amount = next(entry['total_amount_sum'] for entry in monthly_totals if entry['complete_date__month'] == month)
            unique_months.append(month_name_str)
            total_amounts.append(total_amount)
        else:
            # If not present, append 0
            unique_months.append(month_name_str)
            total_amounts.append(0)

    return total_amounts



def StaffHomeData1():
    unique_months,total_amounts = staffExpense()
    home = {
        'unique_months':unique_months,
        'total_amounts':total_amounts,
        'two':staffvehicleexpense("2 Wheeler"),
        'four':staffvehicleexpense("4 Wheeler"),
        'bus':staffvehicleexpense("Bus"),
        'truck':staffvehicleexpense("Truck"),
        'services':Service.objects.all()[::-1],
    }
    return home





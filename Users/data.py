from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from calendar import month_name

from Users.models import Service

def expense(user):
    completed_services = Service.objects.filter(status='Delivered').filter(user_id=user).exclude(complete_date__isnull=True)

# Aggregate total_amount by month
    monthly_totals = completed_services.values('complete_date__month').annotate(total_amount_sum=Sum('total_amount'))

    # Map numerical month values to month names
    month_name_mapping = {i: month_name[i] for i in range(1, 13)}

    # Extract unique months and corresponding total amounts
    unique_months = [month_name_mapping[entry['complete_date__month']] for entry in monthly_totals]
    total_amounts = [entry['total_amount_sum'] for entry in monthly_totals]

    return unique_months,total_amounts



def vehicleexpense(user, category):
    # Get completed services for the given user and category
    completed_services = Service.objects.filter(status='Delivered', user_id=user, category=category).exclude(complete_date__isnull=True)

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



def UserHomeData(user):
    unique_months,total_amounts = expense(user)
    home = {
        'unique_months':unique_months,
        'total_amounts':total_amounts,
        'two':vehicleexpense(user,"2 Wheeler"),
        'four':vehicleexpense(user,"4 Wheeler"),
        'bus':vehicleexpense(user,"Bus"),
        'truck':vehicleexpense(user,"Truck")
    }
    print(home)
    return home
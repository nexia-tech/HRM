from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from users.services import generate_password
    
    
@receiver(post_save,sender=User)
def create_employee_account(sender,created,instance,*args,**kwargs):
    if not instance.employee_id:
        last_employee = User.objects.all().order_by('-employee_id').first()
        employee_id = int(last_employee.employee_id.split("-")[1]) + 1
        print(employee_id)
        if employee_id < 100:
            employee_id = f"NX0{str(employee_id)}"
        else:
            employee_id = f"NX{str(employee_id)}"
        
        user = User()
        user.employee_id = employee_id
        try:
            user.save()
            print("Done")
        except Exception as e:
            print(str(e))
            
from django.contrib.auth.hashers import check_password, make_password
from .models import CustomUser, HitmanProfile


def check_credentials(email, password):
    try:
        user = CustomUser.objects.get(email=email)
        hashed_password = user.password
        verify_password = check_password(password, hashed_password)
        
        if verify_password:
            print("check")
            return user
        else:
            return False
            
    except CustomUser.DoesNotExist:
        return None
    

def new_user(email, password):
    try:
        hash_password = make_password(password)
        user = CustomUser.objects.create(email=email, password=hash_password, username=email)
        hitman_profile = HitmanProfile.objects.create(user=user)
        data = user
    except:
        data = None
    return data
def admin_user_check(user):
  return user.is_staff

def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"

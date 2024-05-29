def website_data(request):
     websites=request.POST.getlist("website")
     return websites

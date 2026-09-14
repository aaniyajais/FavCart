from django.contrib import admin
from .models import *
# Register your models here.
class contactusAdmin(admin.ModelAdmin):
    list_display = ("Name","Mobile","Email","Message")

admin.site.register(contactus,contactusAdmin)

##########################################

class categoryAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Cpic')

admin.site.register(category,categoryAdmin)
##############################################
class maincateAdmin(admin.ModelAdmin):
    list_display = ('id','Name','picture','cdate')

admin.site.register(maincate,maincateAdmin)

#############################################
class myproductAdmin(admin.ModelAdmin):
    list_display = ('id','pprice','dprice','pcolor','psize','pdes','pdel','ppic','pdate','pcategory','mcategory')

admin.site.register(myproduct,myproductAdmin)
#################################################

class registerAdmin(admin.ModelAdmin):
    list_display = ('Name','Email','Mobile','Ppic','Passwd','Address')

admin.site.register(register,registerAdmin)

#####################################################
class mcartAdmin(admin.ModelAdmin):
    list_display = ('id','userid','pid','cdate','status')
admin.site.register(mcart,mcartAdmin)

class morderAdmin(admin.ModelAdmin):
    list_display = ('id','userid','pid','remarks','status','odate')
admin.site.register(morder,morderAdmin)








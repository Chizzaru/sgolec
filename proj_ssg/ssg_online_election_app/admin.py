from django.contrib import admin

from .models import User, Category, Candidate, VoteVoucher, Vote

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Candidate)
admin.site.register(VoteVoucher)
admin.site.register(Vote)
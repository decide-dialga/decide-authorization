from django.contrib import admin

from .models import Census
from voting.models import Voting
from django.contrib.auth import get_user_model


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )

    def check_user_exist(self, username):
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            return True
        else:
            return False

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.

        """

        votings = Voting.objects.all()

        voting_id = obj.voting_id

        if votings:

            for v in votings:
                 if v.id == voting_id and self.check_user_exist(
                     request.user.username):

                    obj.save()
                    break


admin.site.register(Census, CensusAdmin)

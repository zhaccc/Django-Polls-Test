from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """
    This tells Django: “Choice objects are edited 
    on the Question admin page. By default, 
    provide enough fields for 3 choices.”
    """
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    """
    By default, Django displays the str() of each object. 
    But sometimes it’d be more helpful if we could display 
    individual fields. To do that, use the list_display 
    admin option, which is a tuple of field names to display, as columns
    """
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    """
    Dodaje filter polje da mozemo pretrazivati po pub date.
    """
    list_filter = ['pub_date']
    """
    That adds a search box at the top of the change list. 
    When somebody enters search terms, Django will 
    search the question_text field. 
    """
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

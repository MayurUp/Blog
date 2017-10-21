from django.contrib import admin
from .models import Post, Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp"]
	list_display_links = ["updated"]
	list_filter = ["title", "updated", "timestamp"]
	search_fields = ["title"]
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)
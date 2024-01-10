from django.contrib import admin
from general.models import (
    User,
    Post,
    Comment,
    Reaction,
)
from django.contrib.auth.models import Group



@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_active",
        "date_joined",
    )
    search_fields = (
        "id",
        "username",
        "email",
    )
    list_filter = (
        "is_active",
    )
    # autocomplete_fields = (
    #     "author",
    #     "post",
    # )


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "body",
        "created_at",
    )
    search_fields = (
        "id",
        "title",
        "author__username",
    )

    def get_body(self, obj):
        max_length = 64
        if len(obj.body) > max_length:
            return obj.body[:61] + "..."
        return obj.body
    
    get_body.short_description = "body"

    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("comments")
    


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "body",
        "created_at",
    )
    list_display_links = (
        "id",
        "body",
    )
    search_fields = (
        "author__username",
        "post__title",
    )
    raw_id_fields = (
        "author",
    )


@admin.register(Reaction)
class ReactionModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "value",
    )


admin.site.unregister(Group)
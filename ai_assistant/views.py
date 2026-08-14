from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import AIConversation, AIMessage


@login_required
def assistant(request):

    conversations = AIConversation.objects.filter(
        user=request.user
    ).order_by("-updated_at")

    return render(
        request,
        "ai_assistant/assistant.html",
        {
            "conversations": conversations,
        }
    )


@login_required
def new_conversation(request):

    conversation = AIConversation.objects.create(
        user=request.user,
        title="New Conversation"
    )

    return redirect(
        "ai_assistant:conversation",
        conversation_id=conversation.id
    )


@login_required
def conversation(request, conversation_id):

    conversation = get_object_or_404(
        AIConversation,
        id=conversation_id,
        user=request.user
    )

    conversations = AIConversation.objects.filter(
        user=request.user
    ).order_by("-updated_at")

    messages = conversation.messages.all()

    return render(
        request,
        "ai_assistant/assistant.html",
        {
            "conversation": conversation,
            "conversations": conversations,
            "messages": messages,
        }
    )


@login_required
def send_message(request, conversation_id):

    conversation = get_object_or_404(
        AIConversation,
        id=conversation_id,
        user=request.user
    )

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method."},
            status=405
        )

    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse(
            {"error": "Message cannot be empty."},
            status=400
        )

    # Save user message
    AIMessage.objects.create(
        conversation=conversation,
        role="user",
        content=content
    )

    # Auto-generate conversation title
    if conversation.messages.count() == 1:

        title = " ".join(content.split())

        conversation.title = title[:40]

        if len(title) > 40:
            conversation.title += "..."

        conversation.save()

    # Generate AI response
    from .services import get_ai_response

    ai_reply = get_ai_response(conversation)

    # Save AI response
    AIMessage.objects.create(
        conversation=conversation,
        role="assistant",
        content=ai_reply
    )

    return JsonResponse({
        "success": True,
        "user_message": content,
        "ai_message": ai_reply,
        "conversation_title": conversation.title,
    })


@login_required
def delete_conversation(request, conversation_id):

    conversation = get_object_or_404(
        AIConversation,
        id=conversation_id,
        user=request.user
    )

    if request.method == "POST":
        conversation.delete()

    return redirect(
        "ai_assistant:assistant"
    )
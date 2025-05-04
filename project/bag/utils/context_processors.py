from project.bag.models import Bag


def bag_size(request):
    if request.user.is_authenticated:
        bag, _ = Bag.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        bag, _ = Bag.objects.get_or_create(session_key=session_key)

    bag_size = bag.items.count()
    return {'bag_size': bag_size}

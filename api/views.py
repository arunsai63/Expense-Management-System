from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from .repo.expenseRepo import ExpenseRepo


@require_GET
def get_tags(request):
    repo = ExpenseRepo()
    tags = repo.get_tags()
    return JsonResponse({"tags": [{"tagid": tagid, "tagtext": tagtext} for tagid, tagtext in tags]})


@require_POST
def add_tag(request):
    if 'tag' not in request.POST:
        return HttpResponseBadRequest()
    repo = ExpenseRepo()
    status = repo.add_tag(request.POST['tag'])
    return JsonResponse({"status": status})

@require_POST
def add_subtag(request):
    if 'tag' not in request.POST or 'subtag' not in request.POST:
        return HttpResponseBadRequest()
    repo = ExpenseRepo()
    status = repo.add_subtag(request.POST['tag'], request.POST['subtag'])
    return JsonResponse({"status": status})

@require_POST
def add_expense(request):
    if 'tagid' not in request.POST or 'subtagid' not in request.POST or 'amount' not in request.POST or 'expense_desc' not in request.POST:
        return HttpResponseBadRequest()
    repo = ExpenseRepo()
    status = repo.add_expense(request.POST.copy())
    return JsonResponse({"status": status})


@require_GET
def get_subtags(request):
    repo = ExpenseRepo()
    res = repo.get_subtags()
    subtags = {}
    for tagid, tag, subtagid, subtag in res:
        if subtag is None:
            subtags[tag] = {
                "tagid": tagid,
                "subtags": []
            }
        elif tag not in subtags:
            subtags[tag] = {
                "tagid": tagid,
                "subtags": [{
                    "subtagid": subtagid,
                    "subtagtext": subtag
                }]
            }
        else:
            subtags[tag]["subtags"].append({
                "subtagid": subtagid,
                "subtagtext": subtag
            })
    return JsonResponse(subtags)

@require_GET
def get_balance(request):
    repo = ExpenseRepo()
    balance = repo.get_balance()
    return JsonResponse({"balance": balance})

@require_GET
def get_expenses(request):
    repo = ExpenseRepo()
    expenses = repo.get_expenses()
    res = []
    for amount, desc, tag, subtag in expenses:
        res.append({
            "amount": amount,
            "desc": desc,
            "tag": tag,
            "subtag": subtag
        })
    return JsonResponse({"expenses": res})

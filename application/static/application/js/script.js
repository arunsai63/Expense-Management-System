function addTag() {
    $("#tagTxtBox").val($("#tagTxtBox").val().trim());
    $.post("/api/Tags/AddTag", {
        tag: $("#tagTxtBox").val()
    }, function (data) {
        if (!data.status)
            alert('failed to add tag');
        else
            refreshTags();
    });
    $("#addTagModal").modal('hide');
}

function addSubtag() {
    $("#subTagTxtBox").val($("#subTagTxtBox").val().trim());
    $.post("/api/Tags/AddSubTag", {
        tag: $("#tagDropdown :selected").val(),
        subtag: $("#subTagTxtBox").val()
    }, function (data) {
        if (!data.status)
            alert('failed to add subtag');
        else
            refreshTags();
    });
    $("#addSubtagModal").modal('hide');
}

$("#addSubtagModal").on("show.bs.modal", function () {
    $.get("/api/Tags/GetTags", function (data) {
        $("#tagDropdown").empty();
        $.each(data.tags, function (index, value) {
            $("#tagDropdown").append(
                `<option value=${value.tagid}>${value.tagtext}</option>`)
        });
    });
}).on('hidden.bs.modal', function () {
    $("#subTagTxtBox").val("");
});

$("#addTagModal").on('hidden.bs.modal', function () {
    $("#tagTxtBox").val("");
});

$("#addExpBtn").click(function () {
    var subtag = $("#expSubtagDD :selected").val();
    if (subtag == undefined)
        subtag = null;
    $("#expDescTxtBox").val($("#expDescTxtBox").val().trim());
    if (parseInt($("#expAmtTxtBox").val()) < 0)
        return false;

    $.post('/api/AddExpense', {
        "tagid": $("#expTagDD :selected").val(),
        "subtagid": subtag,
        "amount": parseInt($("#expAmtTxtBox").val()),
        "expense_desc": $("#expDescTxtBox").val()
    }, function (data) {
        if (!data.status) {
            alert("failed to add expense");
            return false;
        }
        $("#expAmtTxtBox").val('');
        $("#expDescTxtBox").val('');
        refreshExpenses();
        return true;
    });
    return false;
});

function refreshTags() {
    $.get("/api/Tags/GetSubTags", function (data) {
        var all_tags = {}
        $("#expTagDD").empty();
        $.each(Object.keys(data), function(index, tag){
            var tagid = data[tag].tagid;
            $("#expTagDD").append(`<option value="${tagid}">${tag}</option>`);
            all_tags[tagid] = [];
            $.each(data[tag].subtags, function(i, subtag) {
                all_tags[tagid].push(subtag);
            });
        });
        $("#expTagDD").change(function (){
            $("#expSubtagDD").empty();
            var subtags = all_tags[$("#expTagDD :selected").val()];
            $.each(subtags, function(index, subtag) {
                $("#expSubtagDD").append(`<option value="${subtag.subtagid}">${subtag.subtagtext}</option>`);
            });
        });
        $("#expTagDD").change();
    });
}
refreshTags();

function refreshBalance() {
    $.get("/api/GetBalance", function (data) {
        $("#balanceDiv").empty();
        $("#balanceDiv").append(`<label class="bg-dark pr-1 m-0">BALANCE-</label>${data.balance}`);
    });
}
refreshBalance();

function refreshExpenses() {
    $.get('/api/GetExpenses', function(data) {
        $("#expenseList").empty();
        $.each(data.expenses, function(index, exp) {
            console.log(exp);
            if (exp.subtag == null)
                exp.subtag = ""
            $("#expenseList").append(`<li>${exp.amount}$ in ${exp.desc} (${exp.tag}, ${exp.subtag})</li>`)
        });
    });
}
refreshExpenses();
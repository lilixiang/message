$(".delete-contact").click(function () {

    let contactId = $(this).data("contact-id");
    // console.info(contactId);

    // $($(this).data("target")).hide();
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/delete/contact/",
        type: "POST",
        data: {
            "contact_id": contactId,
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (response) {
            if (response && response.status == true) {
                window.location.reload();
            }

        }


    });
});


$(".delete-message").click(function () {

    let messgageId = $(this).data("message-id");
    // console.info(messgageId);

    // $($(this).data("target")).hide();
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/delete/message/",
        type: "POST",
        data: {
            "message_id": messgageId,
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (response) {
            if (response && response.status == true) {
                window.location.reload();
            }

        }

    });
});



$(document).ready(function() {
    $("#btnSubmit").click(function() {
        var formData = {
            givename: $("#givename").val(),
            surname: $("#surname").val(),
            password: $("#password").val(),
            email: $("#email").val(),
            phone: $("#phone").val(),
            birthday: $("#birthday").val(),
            goal: $("#goal").val()
        };

        // Make AJAX request
        $.ajax({
            url: "../api/customer/new/",
            type: "POST",
            data: formData,
            dataType: "json", // Specify the expected data type
            success: function(data) {
                // Handle success response
                if (data.success)
                {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: response.message
                      });
                }
                else
                {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops',
                        text: response.message
                      });
                }
                console.log(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Handle error
                console.error("Error:", textStatus, errorThrown);
            }
        });
    });
});

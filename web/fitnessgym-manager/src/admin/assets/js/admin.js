$(document).ready(function() {

    $.ajax({
        url: '../api/settings/gym/',
        type: 'GET',
        success: function(response) {
            console.log(response);
            if (response.success) {
                if (Array.isArray(response.data)) {

                    console.log(response.data[0]);
                    document.getElementById("GYMName").innerHTML = response.data[0].name;
                    setCookie("gym",response.data[0].toString(), 1);
                    
                    ///response.data[0].id;
                   
                } else {
                    console.log("No data found in response");
                }

            } else {
                
                console.error(response.message);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error:', textStatus, errorThrown);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong!'
            });
        }
    });

    $('#btnAdminLogin').click(function() {
  
        // Serialize form data into a JSON object
        var formData = {
            username: $('input[name="username"]').val(),
            password: $('input[name="password"]').val()
        };
        var json = JSON.stringify(formData);
        console.log(json);
        // Send JSON data in the request body
        $.ajax({
            url: '../api/authentication/',
            type: 'POST',
            contentType: 'application/json', // Set content type to JSON
            data: json, // Convert JSON object to string 
            dataType: 'json',
            success: function(response) {
                console.log(response);
                if (response.success) {
                    if (Array.isArray(response.data)) {

                        console.log(response.data[0]);
                        Swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: response.message
                        });    
                        setCookie("account",response.data[0].toString(), 1);
                        window.location.href = "dashboard/";
                        ///response.data[0].id;
                       
                    } else {
                        console.log("No data found in response");
                    }

                    
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message
                    });
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error:', textStatus, errorThrown);
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!'
                });
            }
        });
    });
});

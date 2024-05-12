$(document).ready(function() {
        const calculatorKeys = document.querySelector('.calculator__keys');
        calculatorKeys.addEventListener('click', function(event) {

            if (event.target.classList.contains('calculator__key')) {

                if(event.target.innerHTML == "1" || event.target.innerHTML == "2" || event.target.innerHTML == "3" || event.target.innerHTML == "4" || 
                event.target.innerHTML == "5" || event.target.innerHTML == "6" || event.target.innerHTML == "7" || event.target.innerHTML == "8" || 
                event.target.innerHTML == "9" || event.target.innerHTML == "0") 
                {
                    if(document.getElementById("calculatorOutput").innerHTML == "0" && document.getElementById("calculatorOutput").innerHTML.length == 1)
                    {
                        document.getElementById("calculatorOutput").innerHTML = event.target.innerHTML;
                    }
                    else
                    {                        
                        document.getElementById("calculatorOutput").innerHTML += event.target.innerHTML;
                    }
                }

            }
        });    

        document.getElementById("calculatorEraser").addEventListener('click', function(event) {
            document.getElementById("calculatorOutput").innerHTML = "0";
        });

        document.getElementById("calculatorBackspace").addEventListener('click', function(event) {
            if(document.getElementById("calculatorOutput").innerHTML != "0")
            {
                if(document.getElementById("calculatorOutput").innerHTML.length == 1)
                {
                    document.getElementById("calculatorOutput").innerHTML = "0";
                }
                else
                {
                    document.getElementById("calculatorOutput").innerHTML = document.getElementById("calculatorOutput").innerHTML.slice(0, -1);
                }
                
            }
        });

        document.addEventListener('keydown', function(event) {
            // Log the key code of the pressed key
            if(event.key.toString() == "1" || event.key.toString() == "2" || event.key.toString()== "3" || event.key.toString() == "4" || 
            event.key.toString() == "5" || event.key.toString() == "6" || event.key.toString() == "7" || event.key.toString() == "8" || 
            event.key.toString() == "9" || event.key.toString() == "0")
            {
                if(document.getElementById("calculatorOutput").innerHTML == "0" && document.getElementById("calculatorOutput").innerHTML.length == 1)
                    {
                        document.getElementById("calculatorOutput").innerHTML = event.key.toString();
                    }
                    else
                    {                        
                        document.getElementById("calculatorOutput").innerHTML += event.key.toString();
                    }
            }
            
            if(event.keyCode == 8)
            {
                if(document.getElementById("calculatorOutput").innerHTML != "0")
                    {
                        if(document.getElementById("calculatorOutput").innerHTML.length == 1)
                        {
                            document.getElementById("calculatorOutput").innerHTML = "0";
                        }
                        else
                        {
                            document.getElementById("calculatorOutput").innerHTML = document.getElementById("calculatorOutput").innerHTML.slice(0, -1);
                        }
                        
                    }
            }

            if(event.keyCode == 46)
            {
                document.getElementById("calculatorOutput").innerHTML = "0";
            }
        });

        document.getElementById("calculatorSend").addEventListener('click', function(event) {
            $.ajax({
                url: '../../api/customer/find/?code='+document.getElementById("calculatorOutput").innerHTML+'&fields=subscription',
                type: 'GET',
                success: function(response) {
                    
                    if(response.success)
                    {
                        var customer = response.data[0];
                        var regtype = 0;
                        var subscriptionArray = response.data[0].subscription

                            console.log(subscriptionArray.length);
                            if (subscriptionArray.length === 0) {
                                regtype = 2;
                            } else {
                                regtype = 1;
                            }

                        if (response.success) {
                            var postData = {
                                code: customer.id,
                                type: regtype
                            };
                
                            $.ajax({
                                type: 'POST',
                                url: '../../api/attendance/register/',
                                data: postData,
                                success: function(response) {
                                    console.log(response);
                                    // Display the response
                                    if(response.success)
                                    {
                                        document.getElementById("calculatorOutput").innerHTML = "0";
                                        Swal.fire({
                                            icon: 'success',
                                            title: 'Attendance recorded',
                                            text: customer.givename + ' now you come in'
                                        });
                                    }
                                    else
                                    {
                                        Swal.fire({
                                            icon: 'warning',
                                            title: customer.givename,
                                            text: response.message
                                        });
                                    }
                                },
                                error: function(xhr, status, error) {
                                    // Handle errors
                                    console.error(xhr.responseText);
                                }
                            });                        
                        } else {
                            Swal.fire({
                                icon: 'info',
                                title: 'Validation',
                                text: response.message
                            });
                        }
                    }
                    else
                    {
                        Swal.fire({
                            icon: 'error',
                            title: 'Hey!',
                            text: 'Something went wrong: insert a valid customer code'
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
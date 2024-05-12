$(document).ready(function() {

    $.ajax({
        url: '../../api/settings/gym/',
        type: 'GET',
        success: function(response) {
            console.log(response);
            if (response.success) {
                if (Array.isArray(response.data)) {

                    console.log(response.data[0]);
                    document.getElementById("gymName").innerHTML = response.data[0].name;
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

       loadAttendance();

        $.ajax({
            url: '../../api/summary/today/sales/',
            type: 'GET',
            success: function(response) {
                console.log(response);
                if (response.success) {
                    
                    var amount = 0;
                    if (Array.isArray(response.data)) {
                       ///PLOT
                        response.data.forEach(function(item) {
                            // Access properties of each objecy
                            amount = parseInt(amount) + parseInt(item.price);
                        });

                    } else {
                        console.log("No data found in response");
                    }
                    
                    document.getElementById("todaySales").innerHTML = response.count;
                    document.getElementById("todayRevenue").innerHTML = "$ " + amount;

                } else {
                    Swal.fire({
                        icon: 'Info',
                        title: 'Sales',
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

        $('#regAttendance').click(function() {
            document.getElementById("myForm").style.display = "block";
        });


        $('#closeAttendance').click(function() {
            document.getElementById("myForm").style.display = "none";
        });

        $('#closeConfirmAttendanceForm').click(function() {
            document.getElementById("confirmAttendanceForm").style.display = "none";
        });

        
        $('#btnRegAttendence').click(function() {

            var link="";

            if (document.getElementById("codeInput1").value != "")
            {
                var code = document.getElementById("codeInput1").value;
                link =  '../../api/customer/find/?code='+code;
            }
            else
            {
                if (document.getElementById("nameInput1").value != "")
                {
                    var name = "%"+document.getElementById("nameInput1").value.replace(" ", "%")+"%";
                    link =  '../../api/customer/find/?name='+name;
                }
            }

                $.ajax({
                    url: link,
                    type: 'GET',
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                title: "Some users were found, do you wanna see them?",
                                showDenyButton: true,
                                showCancelButton: false,
                                confirmButtonText: "Yes",
                                denyButtonText: `No`
                              }).then((result) => {
                                /* Read more about isConfirmed, isDenied below */
                                if (result.isConfirmed) {
                                    document.getElementById("myForm").style.display = "none";

                                    document.getElementById("attendanceName").innerHTML = response.data[0].givename +" "+ response.data[0].surname;
                                    document.getElementById("attendanceUsername").innerHTML = "@"+response.data[0].username;
                                    document.getElementById("attendanceGoal").innerHTML = response.data[0].goal;
                                    document.getElementById("attendanceBirthday").innerHTML = "<h5>"+formatDate(response.data[0].birthday)+"<br><small>Bithday</small></h5";
                                    document.getElementById("attendanceRegistered").innerHTML = "<h5>"+response.data[0].created_at+"<br><small>Registered</small></h5>";

                                    document.getElementById("inputAttCode").value = response.data[0].id;
                                    document.getElementById("inputAttUsername").value = response.data[0].username;
                                    document.getElementById("inputAttEmail").value = response.data[0].email;
                                    document.getElementById("inputAttgivename").value =response.data[0].givename ;
                                    document.getElementById("inputAttSurname").value = response.data[0].surname;
                                    document.getElementById("inputAttAddress").value = response.data[0].address;
                                    document.getElementById("inputAttCity").value = response.data[0].city;
                                    document.getElementById("inputAttCountry").value = response.data[0].country;
                                    document.getElementById("inputAttZipcode").value = response.data[0].zipcode;

                                    document.getElementById("confirmAttendanceForm").style.display = "block";
                                    document.getElementById("nameInput1").value = "";
                                    document.getElementById("codeInput1").value = "";
                                } else if (result.isDenied) {
                                  Swal.fire("Changes are not saved", "", "info");
                                }
                              });
                        } else {
                            Swal.fire({
                                icon: 'info',
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

        
        $('#submitAttendance').click(function() {

            $.ajax({
                url: '../../api/customer/find/?code='+document.getElementById("inputAttCode").value+'&fields=subscription',
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

function formatDate(inputDate) {
    // Parse the input date string
    var dateParts = inputDate.split('-');
    var year = dateParts[0];
    var month = dateParts[1];
    var day = dateParts[2];
  
    // Create a Date object with the parsed date
    var date = new Date(inputDate);
  
    // Array of month names
    var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  
    // Get the month name
    var monthName = monthNames[date.getMonth()];
  
    // Get the day number with suffix
    var dayNumber = date.getDate()+1    ;
    var daySuffix = getDaySuffix(dayNumber);
    var formattedDay = dayNumber + daySuffix;
  
    // Construct the formatted date string
    var formattedDate = monthName + ' ' + formattedDay;
  
    return formattedDate;
  }
  
  // Function to get the suffix for the day number (e.g., 1st, 2nd, 3rd)
  function getDaySuffix(day) {
    switch (day % 10) {
      case 1: return "st";
      case 2: return "nd";
      case 3: return "rd";
      default: return "th";
    }
  }

  function loadAttendance()
  {
     // Send JSON data in the request body
     $.ajax({
        url: '../../api/summary/today/attendance/',
        type: 'GET',
        success: function(response) {
            console.log(response);
            if (response.success) {
                if (Array.isArray(response.data)) {
                   ///PLOT
                   document.getElementById("cntAttendance").innerHTML = response.count;
                   var html = "";
                   response.data.forEach(function(item) {
                    // Access properties of each object
                    var strtype = "";
                    switch(item.type)
                    {
                        case 0:
                            strtype = "";
                            break;
                        case 1:
                            strtype = "Membership";
                            break;
                        case 2:
                            strtype = "Daily";
                            break;
                    }
                    html +="<tr>"+
                        "<td><center>"+item.id +"</center></td>"+
                        "<td><center>"+item.givename +" "+ item.surname+"</center></td>"+
                        "<td><center>"+item.registered_at +"</center></td>"+
                        "<td><center>"+strtype+"</center></td>"+
                        "<td><center><btn class='btn btn-sm btn-outline-success btn-round btn-icon'><i class='fa fa-eye'></i></btn></center></td>"+
                        "</tr>";
                    });
                 
                   document.getElementById("tableAttendanceBody").innerHTML+=html;
                   let table = new DataTable('#attendanceTable');

                } else {
                    console.log("No data found in response");
                }

                
            } else {
                Swal.fire({
                    icon: 'Info',
                    title: 'Attendance',
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
  }
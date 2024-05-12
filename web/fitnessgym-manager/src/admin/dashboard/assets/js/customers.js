$(document).ready(function() {

    $.ajax({
        url: '../../../api/settings/gym/',
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

    
    loadCustomers();

    $('#newCustomerOp').click(function() {
        document.getElementById("newCustomerForm").style.display = "block";
    });

    $('#newCustomerClose').click(function() {
        document.getElementById("newCustomerForm").style.display = "none";
    });
    
    $('#btnNewCustomer').click(function() {

        var postData = {
            givename: document.getElementById("givenameInput1").value,
            surname: document.getElementById("surnameInput1").value,
            email: document.getElementById("emailInput1").value,
            phone: document.getElementById("phoneInput1").value,
            birthday: document.getElementById("birthdayInput1").value,
            goal: document.getElementById("goalInput1").value
        };
        $.ajax({
            type: 'POST',
            url: '../../../api/customer/new/',
            data: postData,
            success: function(response) {
                console.log(response);
                // Display the response
                if(response.success)
                {
                    loadCustomers();
                    Swal.fire({
                        icon: 'success',
                        title: 'Done',
                        text: response.message +", your customer code is: " + response.new_id
                    });
                }
                else
                {
                    Swal.fire({
                        icon: 'warning',
                        title: 'Attendance',
                        text: response.message
                    });
                }
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.error(xhr.responseText);
            }
        });

        document.getElementById("newCustomerForm").style.display = "none";
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

  function loadCustomers()
  {
    document.getElementById("tableAttendanceBody").innerHTML="";
     // Send JSON data in the request body
     $.ajax({
        url: '../../../api/customer/list/',
        type: 'GET',
        success: function(response) {
            console.log(response);
            if (response.success) {
                if (Array.isArray(response.data)) {
                   ///PLOT
                   document.getElementById("cntCustomers").innerHTML = response.count;
                   document.getElementById("cntMembers").innerHTML = response.members;
                   var html = "";
                   response.data.forEach(function(item) {
                    // Access properties of each object
                    var stravailable = "";
                    switch(item.status)
                    {
                        case 0:
                            stravailable = "Inactive";
                            break;
                        case 1:
                            stravailable = "Active";
                            break;
                    }

                    html +="<tr>"+
                        "<td><center>"+item.id +"</center></td>"+
                        "<td><center>"+item.givename +" "+ item.surname+"</center></td>"+
                        "<td><center>"+stravailable +"</center></td>"+
                        "<td><center>"+item.created_at+"</center></td>"+
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
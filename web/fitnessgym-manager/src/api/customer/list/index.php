<?php
    // Access the received data
    date_default_timezone_set('America/Santo_Domingo');
    require "../../conn.php";
    $response = array(); 
    $cdatetime = date('Y-m-d H:i:s');
    // Prepare and execute the SQL statement
    $stmt = $mysqli->prepare("SELECT COUNT(*) FROM customers");
    $stmt->execute();
    $stmt->bind_result($attendanceCount);
    $stmt->fetch();
    $stmt->close();

    // Prepare and execute the SQL statement
    $stmt = $mysqli->prepare("SELECT COUNT(*) FROM subscription WHERE starts_at <= '$cdatetime' AND ends_at >= '$cdatetime'");
    $stmt->execute();
    $stmt->bind_result($membersCount);
    $stmt->fetch();
    $stmt->close();
  
    // Prepare and execute the SQL statement
    $stmt = $mysqli->prepare("SELECT * FROM customers");
    $stmt->execute();
    $result = $stmt->get_result();
    $results = array();

    
    $sresults = array();
    while ($row = $result->fetch_assoc()) {
        // Add the row to the results array
        if(isset($_GET['fields']) && !empty($_GET['fields']))
        {
            $filter2 = "";
            $fields = $_GET["fields"];  
            if(strpos($fields, "subscription") !== false) // Make sure to check if the field contains "subscription"
            {
                if($filter2 == "")
                {
                    $filter2.=" AND s.starts_at <= '$cdatetime' AND s.ends_at >= '$cdatetime'";
                }
    
                $sql2 = "SELECT * FROM subscription s WHERE s.customer = ".$row['id']." AND status = 1";  
                
                $response = array(); 
                $stmt = $mysqli->prepare($sql2.$filter2);
                $stmt->execute();
                $result = $stmt->get_result();
                $sresults = array(); // Initialize sresults array
                while ($row2 = $result->fetch_assoc()) {
                    // Add the row to the sresults array
                    $sresults[] = $row2;
                }
    
                // Assign sresults to the subscription key in the row
                $row['subscription'] = $sresults;
            }
        }
        // Add the row to the results array along with subscription data
        $row['subscription'] = $sresults;
        $results[] = $row;
    }

    // Check if any rows were found
    if (!empty($results)) {
        // User exists
        $response['success'] = true;
        $response['count'] = $attendanceCount;
        $response['members'] =$membersCount;
        $response['data'] = $results;

        header('Content-Type: application/json');
        echo json_encode($response);

    } else {
        $stmt->close();

        $response['success'] = false;
        $response['message'] = "Couldn't get any result";
        $response['data'] = "[]";
        // Encode the response array as JSON and echo it
        header('Content-Type: application/json');
        echo json_encode($response);
    }
?>

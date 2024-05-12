<?php    
    date_default_timezone_set('America/Santo_Domingo');
    $filter="";
    $sql = "SELECT c.id, c.givename, c.surname, c.phone, c.email, c.username, c.birthday, c.status, c.goal, c.country, c.state, c.city, c.address, c.zipcode, c.created_at FROM customers c WHERE";

    $cdatetime = date('Y-m-d H:i:s');

    if(isset($_GET['code']) && !empty($_GET['code']))
    {
        $code = $_GET["code"];  
        $filter.=" c.id = ".$code;
    }

    if(isset($_GET['name']) && !empty($_GET['name']))
    {
        $name = $_GET["name"];  
        if($filter == "")
        {
            $filter.=" c.givename LIKE '".$name."' OR c.surname LIKE '".$name."'";
        }
        else
        {
            $filter.=" AND c.givename LIKE '".$name."' OR c.surname LIKE '".$name."'";
        }
    }

    require "../../conn.php";

    $sql2 = "";
    $sresults = array();

    $response = array(); 
    $stmt = $mysqli->prepare($sql.$filter);
    $stmt->execute();
    $result = $stmt->get_result();
    $results = array();
    // Fetch the result in a loop
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
        $response['message'] = "success";
        $response['data'] = $results;
        //$response['suscription'] = $sresults;

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
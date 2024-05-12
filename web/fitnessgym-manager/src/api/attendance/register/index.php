<?php
date_default_timezone_set('America/Santo_Domingo');

// Check if 'code' parameter is set
if(isset($_POST["code"])) {
    $code = $_POST["code"];  
    if(isset($_POST["type"])) 
    {
        $type = $_POST["type"];  
        $sod = date('Y-m-d H:i:s', strtotime('today'));
        $eod = date('Y-m-d H:i:s', strtotime('tomorrow') - 1);
    
        require "../../conn.php";
        $response = array(); 
        $stmt = $mysqli->prepare("SELECT COUNT(*) FROM attendance WHERE customer = ? AND status = 1 AND registered_at BETWEEN ? AND ?");
        $stmt->bind_param("sss", $code, $sod, $eod);
        $stmt->execute();
        $stmt->bind_result($count);
        $stmt->fetch();
        if($count > 0) {
            // User already exists
            $response['success'] = false;
            $response['message'] = "You already have been here!";
        } else {
            // User does not exist, perform insertion or other operations here
            // Close the statement
            $stmt->close();
            if($type == 2)
            {
                $stmt = $mysqli->prepare("INSERT INTO sales (product, customer) VALUES (?, ?)");
                $stmt->bind_param("ss", $type, $code);
                if($stmt->execute()) {
                    $stmt->close();
                    $response['success'] = true;
                    $response['message'] = "Insertion successful!";
                } else {
                    $response['success'] = false;
                    $response['message'] = "Error: " . $mysqli->error;
                }
            }
            $stmt = $mysqli->prepare("INSERT INTO attendance (customer, type) VALUES (?, ?)");
            $stmt->bind_param("ss", $code, $type);
            if($stmt->execute()) {
                $response['success'] = true;
                $response['message'] = "Insertion successful!";
            } else {
                $response['success'] = false;
                $response['message'] = "Error: " . $mysqli->error;
            }
        }
    
        // Close the statement
        $stmt->close();
    } else {
        // 'code' parameter is not set
        $response['success'] = false;
        $response['message'] = "'type' parameter is missing in the POST request";
    }
} else {
    // 'code' parameter is not set
    $response['success'] = false;
    $response['message'] = "'code' parameter is missing in the POST request";
}

// Encode the response array as JSON and echo it
header('Content-Type: application/json');
echo json_encode($response);
?>

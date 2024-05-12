<?php
    // Access the received data
    date_default_timezone_set('America/Santo_Domingo');
    require "../../conn.php";
    $response = array(); 

    // Prepare and execute the SQL statement
    $stmt = $mysqli->prepare("SELECT COUNT(*) FROM products");
    $stmt->execute();
    $stmt->bind_result($attendanceCount);
    $stmt->fetch();
    $stmt->close();
  
    // Prepare and execute the SQL statement
    $stmt = $mysqli->prepare("SELECT * FROM products");
    $stmt->execute();
    $result = $stmt->get_result();
    $results = array();

    // Fetch the result in a loop
    while ($row = $result->fetch_assoc()) {
        // Add the row to the results array
        $results[] = $row;
    }

    // Check if any rows were found
    if (!empty($results)) {
        // User exists
        $response['success'] = true;
        $response['count'] = $attendanceCount;
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

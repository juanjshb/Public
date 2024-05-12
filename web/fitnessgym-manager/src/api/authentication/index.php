<?php

    // Retrieve the JSON data from the request body
    $inputJSON = file_get_contents('php://input');
    $inputData = json_decode($inputJSON, true);

    // Access the received data
    $username = $inputData["username"];
    $password = md5($inputData["password"]);
    
    require "../conn.php";
    $response = array(); 

    // Prepare and execute the SQL statement
    $stmt = $mysqli->prepare("SELECT id, givename, surname, email, phone, created_at FROM accounts WHERE username=? AND password=?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();

    // Fetch the result
    $result = $stmt->get_result();

    // Initialize an empty array to store the results
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
        $response['message'] = "Authorized";
        $response['data'] = $results;

        header('Content-Type: application/json');
        echo json_encode($response);

    } else {
        $stmt->close();

        $response['success'] = false;
        $response['message'] = "Couldn't authenticate";
        $response['data'] = "[]";
        // Encode the response array as JSON and echo it
        header('Content-Type: application/json');
        echo json_encode($response);
    }
?>

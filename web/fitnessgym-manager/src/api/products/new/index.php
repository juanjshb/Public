<?php  
// Set the default timezone
date_default_timezone_set('America/Santo_Domingo');

// Retrieve form data
$name = $_POST["name"];    
$descripton = $_POST["descripton"];    
$price = $_POST["price"];   
$type = $_POST["type"];     
// Include database connection
require "../../conn.php";

// Initialize response array
$response = array(); 

    // Insert new user into the database
    $stmt = $mysqli->prepare("INSERT INTO products (name, description, price, type) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $name, $descripton, $price, $type);
    
    if ($stmt->execute()) {
        // Retrieve the ID of the newly added record
        $newId = $mysqli->insert_id;

        $response['success'] = true;
        $response['message'] = "Insertion successful!";
        $response['new_id'] = $newId;
    } else {
        $response['success'] = false;
        $response['message'] = "Error: " . $mysqli->error;
    }

    // Close the statement
    $stmt->close();

// Encode the response array as JSON and echo it
header('Content-Type: application/json');
echo json_encode($response);

?>

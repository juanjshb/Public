<?php  
// Set the default timezone
date_default_timezone_set('America/Santo_Domingo');

// Retrieve form data
$givename = $_POST["givename"];    
$surname = $_POST["surname"];    
$email = $_POST["email"];     
$phone = $_POST["phone"];       
$birthday = $_POST["birthday"];    
$goal = $_POST["goal"];    

// Include database connection
require "../../conn.php";

// Initialize response array
$response = array(); 
$customerExist = 0;
// Check if the user already exists in the database
$stmt = $mysqli->prepare("SELECT COUNT(*) FROM customers WHERE email=?");
$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->bind_result($customerExist);
$stmt->fetch();
$stmt->close();

if ($customerExist > 0) {
    // User already exists
    $response['success'] = false;
    $response['message'] = "User already exists";
} else {
    // Insert new user into the database
    $stmt = $mysqli->prepare("INSERT INTO customers (givename, surname, phone, email, birthday, goal) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssss", $givename, $surname, $phone, $email, $birthday, $goal);
    
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
}

// Encode the response array as JSON and echo it
header('Content-Type: application/json');
echo json_encode($response);

?>

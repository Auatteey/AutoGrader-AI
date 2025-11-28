<?php

session_start();
if($_SESSION['role']!="etudiant"){ header("Location:index.php"); exit(); }

$ch = curl_init("http://127.0.0.1:8000/api/reviews/send");

$data = [
    "student" => $_POST['student_name'],
    "exam" => $_POST['exam_name'],
    "problem" => $_POST['problem_type'],
    "details" => $_POST['details']
];

curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

header("Location: dashboard_etud.php?sent=1");
exit();


?>

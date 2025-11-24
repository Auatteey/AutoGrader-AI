<?php
session_start();
if(!isset($_SESSION['role']) || $_SESSION['role'] != "etudiant") {
    header("Location: index.php");
    exit();
}
$username = $_SESSION['username'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $exam_name = $_POST['exam_name'] ?? '';
    if(empty($exam_name) || !isset($_FILES['copy_file'])) {
        echo "❌ Veuillez choisir un examen et uploader votre copie.";
        exit();
    }

    $ch = curl_init("http://127.0.0.1:8000/api/grade_student");
    $data = [
        'exam_name'    => $exam_name,
        'student_name' => $username,
        'copy'         => new CURLFile($_FILES['copy_file']['tmp_name'], $_FILES['copy_file']['type'], $_FILES['copy_file']['name'])
    ];

    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    echo "✔ Résultat backend : " . $response;
}
?>

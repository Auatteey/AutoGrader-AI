<?php
session_start();
if(!isset($_SESSION['role']) || $_SESSION['role'] != "prof") {
    header("Location: index.php");
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $exam_name = $_POST['exam_name'] ?? '';
    if(empty($exam_name) || !isset($_FILES['exam_file'], $_FILES['correction_file'], $_FILES['bareme_file'])) {
        echo "❌ Veuillez remplir tous les champs et choisir tous les fichiers.";
        exit();
    }

    $ch = curl_init("http://127.0.0.1:8000/api/upload_exam");
    $data = [
        'exam_name' => $exam_name,
        'questions' => new CURLFile($_FILES['exam_file']['tmp_name'], $_FILES['exam_file']['type'], $_FILES['exam_file']['name']),
        'correction'=> new CURLFile($_FILES['correction_file']['tmp_name'], $_FILES['correction_file']['type'], $_FILES['correction_file']['name']),
        'bareme'    => new CURLFile($_FILES['bareme_file']['tmp_name'], $_FILES['bareme_file']['type'], $_FILES['bareme_file']['name'])
    ];

    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    echo "✔ Résultat backend : " . $response;
}
?>

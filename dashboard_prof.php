<?php
session_start();
if(!isset($_SESSION['role']) || $_SESSION['role'] != "prof") {
    header("Location: index.php");
    exit();
}
$username = $_SESSION['username'];
$exam_dir = __DIR__ . "/app/uploads/exams/";
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Professeur</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
    <h2>Bienvenue, <?php echo htmlspecialchars($username); ?> (Professeur)</h2>
    <a href="logout.php">Déconnexion</a>

    <h3>Uploader un examen avec correction et barème</h3>
    <form action="upload_exam.php" method="post" enctype="multipart/form-data">
        <label>Nom de l'examen :</label>
        <input type="text" name="exam_name" required><br><br>

        <label>Fichier Questions (PDF) :</label>
        <input type="file" name="exam_file" accept="application/pdf" required><br><br>

        <label>Fichier Correction (PDF) :</label>
        <input type="file" name="correction_file" accept="application/pdf" required><br><br>

        <label>Fichier Barème (PDF) :</label>
        <input type="file" name="bareme_file" accept="application/pdf" required><br><br>

        <button type="submit">Uploader</button>
    </form>

    <h3>Vos examens déjà uploadés</h3>
    <table>
        <tr>
            <th>Nom</th>
            <th>Examen</th>
            <th>Correction</th>
            <th>Barème</th>
        </tr>
        <?php
        if(is_dir($exam_dir)){
            foreach(scandir($exam_dir) as $exam){
                $exam_path = $exam_dir . $exam . "/";
                if($exam != "." && $exam != ".." && is_dir($exam_path)){
                    $questions_file  = $exam_path . "questions.pdf";
                    $correction_file = $exam_path . "correction.pdf";
                    $bareme_file     = $exam_path . "bareme.pdf";

                    $questions_link  = file_exists($questions_file)  ? "<a href='".str_replace(__DIR__, ".", $questions_file)."' target='_blank'>Voir examen</a>" : "-";
                    $correction_link = file_exists($correction_file) ? "<a href='".str_replace(__DIR__, ".", $correction_file)."' target='_blank'>Voir correction</a>" : "-";
                    $bareme_link     = file_exists($bareme_file)     ? "<a href='".str_replace(__DIR__, ".", $bareme_file)."' target='_blank'>Voir barème</a>" : "-";

                    echo "<tr>
                        <td>".htmlspecialchars($exam)."</td>
                        <td>$questions_link</td>
                        <td>$correction_link</td>
                        <td>$bareme_link</td>
                    </tr>";
                }
            }
        }
        ?>
    </table>
</div>
</body>
</html>

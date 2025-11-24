<?php
session_start();
if(!isset($_SESSION['role']) || $_SESSION['role'] != "etudiant") {
    header("Location: index.php");
    exit();
}
$username = $_SESSION['username'];
$exam_dir = __DIR__ . "/uploads/exams/";
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Étudiant</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
    <h2>Bienvenue, <?php echo htmlspecialchars($username); ?> (Étudiant)</h2>
    <a href="logout.php">Déconnexion</a>

    <h3>Uploader votre copie</h3>
    <form action="upload_copy.php" method="post" enctype="multipart/form-data">
        <label>Choisir l'examen :</label>
        <select name="exam_name" required>
            <option value="">-- Sélectionner un examen --</option>
            <?php
            if(is_dir($exam_dir)){
                foreach(scandir($exam_dir) as $exam){
                    if($exam != "." && $exam != ".." && is_dir($exam_dir.$exam)){
                        echo "<option value='".htmlspecialchars($exam)."'>".htmlspecialchars($exam)."</option>";
                    }
                }
            }
            ?>
        </select>

        <label>Fichier copie (PDF/DOCX/TXT)</label>
        <input type="file" name="copy_file" accept=".pdf,.docx,.txt" required>

        <button type="submit">Uploader</button>
    </form>

    <h3>Voir vos résultats</h3>
    <table>
        <tr><th>Examen</th><th>Note</th><th>Feedback</th></tr>
        <?php
        $student_dir = __DIR__ . "/app/uploads/students/";
        if(is_dir($student_dir)){
            foreach(scandir($student_dir) as $exam){
                $exam_path = $student_dir . $exam . "/";
                if($exam != "." && $exam != ".." && is_dir($exam_path)){
                    $json_file = $exam_path . $username . ".json";
                    if(file_exists($json_file)){
                        $data = json_decode(file_get_contents($json_file), true);
                        echo "<tr>
                            <td>".htmlspecialchars($exam)."</td>
                            <td>".htmlspecialchars($data['grade'])."</td>
                            <td>".htmlspecialchars($data['feedback'])."</td>
                        </tr>";
                    }
                }
            }
        }
        ?>
    </table>
</div>
</body>
</html>

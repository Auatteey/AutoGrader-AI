<?php
session_start();
if (!isset($_SESSION["role"]) || $_SESSION["role"] !== "prof") {
    header("Location: index.php");
    exit();
}

$exam_dir = __DIR__ . "/uploads/exams/";
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Prof – AutoGrader AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="card">
        <h2>📥 Upload d'un Examen</h2>

        <form action="upload_exam.php" method="post" enctype="multipart/form-data">

            <label>Nom de l'examen :</label>
            <input type="text" name="exam_name" required>

            <label>Questions (PDF)</label>
            <input type="file" name="exam_file" accept="application/pdf" required>

            <label>Correction (PDF)</label>
            <input type="file" name="correction_file" accept="application/pdf" required>

            <label>Barème (PDF)</label>
            <input type="file" name="bareme_file" accept="application/pdf" required>

            <button type="submit">Uploader</button>

        </form>
    </div>

    <div class="card">
        <h2>📂 Examens Uploadés</h2>

        <table>
            <tr>
                <th>Examen</th>
                <th>Questions</th>
                <th>Correction</th>
                <th>Barème</th>
            </tr>

            <?php
            foreach (scandir($exam_dir) as $exam) {
                if ($exam === "." || $exam === "..") continue;

                $path = $exam_dir . $exam . "/";

                if (!is_dir($path)) continue;

                echo "<tr>
                    <td>$exam</td>
                    <td><a href='$path/questions.pdf' target='_blank'>Voir</a></td>
                    <td><a href='$path/correction.pdf' target='_blank'>Voir</a></td>
                    <td><a href='$path/bareme.pdf' target='_blank'>Voir</a></td>
                </tr>";
            }
            ?>
        </table>
    </div>

</div>

<?php include "components/footer.php"; ?>

</body>
</html>

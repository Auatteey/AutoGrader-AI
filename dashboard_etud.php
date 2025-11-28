<?php
session_start();
if (!isset($_SESSION["role"]) || $_SESSION["role"] !== "etudiant") {
    header("Location: index.php");
    exit();
}

$username = $_SESSION["username"];
$exam_dir = __DIR__ . "/uploads/exams/";
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Étudiant – AutoGrader AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="card">
        <h2>📤 Soumettre une copie</h2>

        <form method="post" action="upload_copy.php" enctype="multipart/form-data">

            <label>Choisir l'examen :</label>
            <select name="exam_name" required>
                <option value="">-- Sélectionner un examen --</option>
                <?php
                foreach (scandir($exam_dir) as $exam) {
                    if ($exam !== "." && $exam !== ".." && is_dir($exam_dir . $exam)) {
                        echo "<option value='$exam'>$exam</option>";
                    }
                }
                ?>
            </select>

            <label>Votre copie (PDF uniquement)</label>
            <input type="file" name="copy_file" accept="application/pdf" required>

            <button type="submit">Envoyer la copie</button>

        </form>
    </div>

    <div class="card">
        <h2>📊 Mes Résultats</h2>

        <table>
            <tr>
                <th>Examen</th>
                <th>Note</th>
                <th>Similarité</th>
                <th>Feedback</th>
            </tr>

            <?php
            $results_path = __DIR__ . "/results/";

            foreach (scandir($results_path) as $exam) {

                $csv = $results_path . $exam . "/grades.csv";
                if (!file_exists($csv)) continue;

                $file = fopen($csv, "r");
                $header = fgetcsv($file);

                while (($row = fgetcsv($file)) !== false) {

                    list($student, $grade, $sim, $feedback) = $row;

                    if ($student === $username) {
                        echo "<tr>
                            <td>$exam</td>
                            <td>$grade</td>
                            <td>$sim</td>
                            <td>$feedback</td>
                        </tr>";
                    }
                }

                fclose($file);
            }
            ?>
        </table>

    </div>
</div>

<?php include "components/footer.php"; ?>

</body>
</html>

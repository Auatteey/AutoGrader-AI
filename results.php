<?php
session_start();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Résultats – AutoGrader AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">
    <div class="card">
        <h2>📊 Résultats des Examens</h2>

        <?php
        $results_path = __DIR__ . "/results/";

        foreach (scandir($results_path) as $exam) {
            if ($exam === "." || $exam === "..") continue;

            $csv = $results_path . $exam . "/grades.csv";
            if (!file_exists($csv)) continue;

            echo "<h3 style='margin-top:25px;color:#a580ff;'>Examen : $exam</h3>";

            echo "<table>";
            echo "<tr>
                <th>Étudiant</th>
                <th>Note</th>
                <th>Similarité</th>
                <th>Feedback</th>
            </tr>";

            $file = fopen($csv, "r");
            $header = fgetcsv($file);

            while (($row = fgetcsv($file)) !== false) {
                list($student, $grade, $sim, $feedback) = $row;

                echo "<tr>
                    <td>$student</td>
                    <td>$grade</td>
                    <td>$sim</td>
                    <td>$feedback</td>
                </tr>";
            }
            fclose($file);

            echo "</table>";
        }
        ?>
    </div>
</div>

<?php include "components/footer.php"; ?>

</body>
</html>

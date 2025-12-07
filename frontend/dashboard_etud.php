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
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Étudiant – AutoGrader AI</title>
    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>

<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <!-- ============================
         UPLOAD COPY AREA
    ===============================-->
    <div class="card">
        <h2 style="color: var(--accent); margin-bottom: 20px;">
            📤 Soumettre ma copie
        </h2>

        <form method="post" action="upload_copy.php" enctype="multipart/form-data">

            <label>Choisir un examen :</label>
            <select name="exam_name" required>
                <option value="">-- Sélectionner --</option>
                <?php
                foreach (scandir($exam_dir) as $exam) {
                    if ($exam !== "." && $exam !== ".." && is_dir($exam_dir . $exam)) {
                        echo "<option value='$exam'>$exam</option>";
                    }
                }
                ?>
            </select>

            <!-- MODERN DRAG & DROP FILE INPUT -->
            <label class="ai-file-upload" style="
                border: 2px dashed #30363d;
                padding: 25px;
                text-align: center;
                display: block;
                border-radius: var(--radius);
                cursor: pointer;
                transition: .2s;
                background: var(--bg-secondary);
            ">
                <i class="fa-solid fa-cloud-arrow-up" style="font-size: 40px; color: var(--accent);"></i>
                <p style="margin-top: 10px; color: var(--text-secondary);">Glisser-déposer votre PDF</p>
                <span class="browse" style="color: var(--accent); font-weight: 600;">Choisir un fichier</span>
                <input type="file" name="copy" accept="application/pdf" required
                    style="opacity: 0; position: absolute; width: 100%; height: 100%; cursor: pointer;">
            </label>

            <button type="submit">Envoyer ma copie</button>
        </form>
    </div>

    <!-- ============================
         RESULTS AREA
    ===============================-->
    <div class="card">
        <h2 style="color: var(--accent); margin-bottom: 20px;">
            📊 Mes résultats
        </h2>

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

                    list($student, $question, $score, $sim, $feedback, $total) = $row;

                    if ($student === $username) {
                        echo "
                        <tr>
                            <td>$exam</td>
                            <td><strong style='color:var(--accent)'>$total</strong></td>
                            <td>" . round($sim * 100, 1) . "%</td>
                            <td>
                                <details>
                                    <summary style='cursor:pointer;color:var(--accent)'>Voir détail</summary>
                                    <p style='margin-top:10px;color:var(--text-secondary);white-space:pre-wrap;'>$feedback</p>
                                </details>
                            </td>
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

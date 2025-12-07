<?php
session_start();
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Résultats – AutoGrader AI</title>
    <link rel="stylesheet" href="assets/css/theme.css">
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>

<body>

<?php include "components/header.php"; ?>
<?php include "components/sidebar.php"; ?>

<div class="main-content">

    <div class="card">
        <h2 style="color: var(--accent); margin-bottom: 25px;">
            📊 Résultats des Examens
        </h2>

        <?php
        $results_path = __DIR__ . "/results/";

        foreach (scandir($results_path) as $exam) {

            if ($exam === "." || $exam === "..") continue;

            $csv = $results_path . $exam . "/grades.csv";
            if (!file_exists($csv)) continue;
        ?>

            <!-- TITRE DE L’EXAMEN -->
            <h3 class="exam-title">
                <i class="fa-solid fa-file-lines"></i> 
                Examen : <?= htmlspecialchars($exam) ?>
            </h3>

            <table class="table-results">
                <tr>
                    <th>Étudiant</th>
                    <th>Note</th>
                    <th>Similarité</th>
                    <th>Feedback</th>
                    <th>Actions</th>
                </tr>

                <?php
                $file = fopen($csv, "r");
                $header = fgetcsv($file); // ignore first line

                while (($row = fgetcsv($file)) !== false) {
                    list($student, $grade, $sim, $feedback) = $row;
                ?>

                    <tr>
                        <td><strong><?= htmlspecialchars($student) ?></strong></td>
                        <td><?= htmlspecialchars($grade) ?></td>
                        <td><?= htmlspecialchars($sim) ?></td>
                        <td class="feedback-cell">
                            <span class="feedback-preview">
                                <?= substr(htmlspecialchars($feedback), 0, 60) . "..." ?>
                            </span>

                            <!-- Popup -->
                            <div class="feedback-popup">
                                <?= nl2br(htmlspecialchars($feedback)) ?>
                            </div>
                        </td>

                        <td class="actions">
                            <button class="mini-btn" onclick="alert('🔍 Cette action arrive après DB integration')">
                                <i class="fa-solid fa-eye"></i>
                            </button>

                            <button class="mini-btn danger" onclick="alert('❌ Disponible après migration SQL')">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </td>
                    </tr>

                <?php } fclose($file); ?>

            </table>

        <?php } ?>

    </div>

</div>

<?php include "components/footer.php"; ?>

</body>
</html>
